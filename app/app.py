import gradio as gr
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
import threading
from datetime import datetime
import types

MODEL_ID = os.environ.get("MODEL_ID", "huseyincavus/gemma-3-270m-finance-merged")
LOCAL_MODEL_PATH = os.environ.get("LOCAL_MODEL_PATH")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.bfloat16 if torch.cuda.is_available() else torch.float32

def _resolve_model_path():
    if LOCAL_MODEL_PATH and os.path.isdir(LOCAL_MODEL_PATH):
        return LOCAL_MODEL_PATH, True
    if os.path.isdir(MODEL_ID):
        return MODEL_ID, True
    return MODEL_ID, False

resolved_path, is_local = _resolve_model_path()
load_kwargs = {"torch_dtype": DTYPE, "device_map": "auto"}
if is_local:
    load_kwargs["local_files_only"] = True

try:
    tokenizer = AutoTokenizer.from_pretrained(resolved_path, local_files_only=is_local)
    model = AutoModelForCausalLM.from_pretrained(resolved_path, **load_kwargs)
except Exception as e:
    raise RuntimeError(f"Failed to load model from '{resolved_path}' (local={is_local}). Set LOCAL_MODEL_PATH env if needed. Original error: {e}")

DEFAULT_SYSTEM = (
    "You are a helpful finance assistant. Provide clear, concise answers about financial concepts. "
    "Give direct explanations and avoid repetitive questioning. When discussing investments, "
    "include appropriate risk disclaimers but focus on educational content."
)

def build_prompt(system_prompt: str, history, user_msg: str):
    # Simpler prompt format to avoid confusion
    messages = []
    if system_prompt.strip():
        messages.append(f"System: {system_prompt.strip()}\n\n")
    
    # Add conversation history
    for h_user, h_assistant in history:
        messages.append(f"Human: {h_user}\nAssistant: {h_assistant}\n\n")
    
    # Add current user message
    messages.append(f"Human: {user_msg}\nAssistant:")
    
    return "".join(messages)

def complete(prompt_text: str, temperature: float, top_p: float, max_new_tokens: int):
    inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)
    output_ids = model.generate(
        **inputs,
        max_new_tokens=int(max_new_tokens),
        temperature=temperature,
        top_p=top_p,
        repetition_penalty=1.15,
        do_sample=temperature > 0,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    full = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    response = full[len(prompt_text):].strip()
    
    # Clean up response - remove any leftover conversation formatting
    response = response.replace("[USER]", "").replace("[ASSISTANT]", "")
    response = response.replace("Human:", "").replace("Assistant:", "")
    
    # Stop at first newline that starts a new conversation turn
    if "\nHuman:" in response:
        response = response.split("\nHuman:")[0]
    if "\n[USER]" in response:
        response = response.split("\n[USER]")[0]
        
    return response.strip()

def stream_completion(prompt_text: str, temperature: float, top_p: float, max_new_tokens: int):
    inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    gen_kwargs = dict(
        **inputs,
        max_new_tokens=int(max_new_tokens),
        temperature=temperature,
        top_p=top_p,
        repetition_penalty=1.15,
        do_sample=temperature > 0,
        streamer=streamer,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    thread = threading.Thread(target=model.generate, kwargs=gen_kwargs)
    thread.start()
    partial = ""
    for token in streamer:
        partial += token
        # Stop streaming if we hit conversation markers
        if any(marker in partial for marker in ["\nHuman:", "\n[USER]", "[USER]"]):
            break
        yield partial.strip()

def chat_submit(user_msg, system_prompt, temperature, top_p, repetition_penalty, max_new_tokens, history):
    history = history or []
    if not user_msg.strip():
        return gr.update(value=""), history
    prompt_text = build_prompt(system_prompt, history, user_msg)
    answer = complete(prompt_text, temperature, top_p, max_new_tokens)
    history.append((user_msg, answer))
    return "", history

def chat_stream(user_msg, system_prompt, temperature, top_p, repetition_penalty, max_new_tokens, history):
    import time
    history = history or []
    if not user_msg.strip():
        yield "", history, 0, 0.0
        return
    
    prompt_text = build_prompt(system_prompt, history, user_msg)
    streamed = ""
    start_time = time.time()
    token_count = 0
    
    for partial in stream_completion(prompt_text, temperature, top_p, max_new_tokens):
        streamed = partial
        token_count = len(tokenizer.encode(streamed))
        elapsed_time = time.time() - start_time
        tokens_per_sec = token_count / elapsed_time if elapsed_time > 0 else 0.0
        yield "", history + [(user_msg, streamed)], token_count, tokens_per_sec
    
    # finalize history
    history.append((user_msg, streamed))
    final_token_count = len(tokenizer.encode(streamed))
    final_elapsed = time.time() - start_time
    final_tokens_per_sec = final_token_count / final_elapsed if final_elapsed > 0 else 0.0
    yield "", history, final_token_count, final_tokens_per_sec

def clear_chat():
    return [], []  # Return empty list for both state and chat

SAMPLE_PROMPTS = [
    "What is EBITDA and how is it calculated?",
    "Explain the difference between stocks and bonds",
    "What are the main risks of investing in emerging markets?",
    "How does diversification reduce investment risk?",
    "What is compound interest and why is it important?",
]

with gr.Blocks(title="FinGemma", analytics_enabled=False, theme=gr.themes.Soft()) as demo:
    # Header
    gr.Markdown("# FinGemma")
    gr.Markdown(f"**Model:** `{resolved_path.split('/')[-1] if '/' in resolved_path else resolved_path}` | **Device:** {DEVICE}")
    
    # System prompt at the top
    with gr.Row():
        with gr.Column():
            system_prompt = gr.Textbox(
                label="System Instructions", 
                value=DEFAULT_SYSTEM, 
                lines=3,
                placeholder="Define how the AI should behave and respond..."
            )
    
    # Main conversation area
    with gr.Row():
        with gr.Column(scale=8):
            chat = gr.Chatbot(
                height=500, 
                label="Conversation",
                show_label=True,
                container=True,
                bubble_full_width=False
            )
        
        with gr.Column(scale=4):
            # Input area
            user_msg = gr.Textbox(
                label="Your Question", 
                placeholder="Ask about finance concepts, investments, markets...",
                lines=3
            )
            
            # Action buttons
            with gr.Row():
                send_btn = gr.Button("Send", variant="primary", scale=3)
                clear_btn = gr.Button("Clear", scale=1)
            
            # Sample prompts
            sample = gr.Dropdown(
                SAMPLE_PROMPTS, 
                label="Quick Examples", 
                interactive=True,
                container=True
            )
            
            # Generation parameters (collapsed by default)
            with gr.Accordion("Generation Settings", open=False):
                temperature = gr.Slider(0.0, 1.5, value=0.7, step=0.05, label="Temperature")
                top_p = gr.Slider(0.1, 1.0, value=0.9, step=0.05, label="Top-p")
                repetition_penalty = gr.Slider(1.0, 2.0, value=1.15, step=0.05, label="Repetition Penalty")
                max_new_tokens = gr.Slider(16, 512, value=128, step=8, label="Max Tokens")
                
                # Generation stats
                with gr.Row():
                    tokens_generated = gr.Number(label="Tokens Generated", value=0, interactive=False, scale=1)
                    tokens_per_second = gr.Number(label="Tokens/s", value=0.0, interactive=False, scale=1)
    state = gr.State([])
    
    # Event handlers
    def apply_sample(choice):
        return choice if choice else ""
    
    sample.change(apply_sample, inputs=sample, outputs=user_msg)
    
    # Make streaming the default action (Enter key + Send button)
    user_msg.submit(chat_stream, inputs=[user_msg, system_prompt, temperature, top_p, repetition_penalty, max_new_tokens, state], outputs=[user_msg, chat, tokens_generated, tokens_per_second])
    send_btn.click(chat_stream, inputs=[user_msg, system_prompt, temperature, top_p, repetition_penalty, max_new_tokens, state], outputs=[user_msg, chat, tokens_generated, tokens_per_second])
    
    # Clear chat
    clear_btn.click(clear_chat, None, [state, chat])
    demo.load(lambda: None, None, None)

if __name__ == "__main__":
    # More comprehensive API disabling to prevent "No API found" errors
    try:
        # Override API info with proper structure
        empty_api = {
            "named_endpoints": {}, 
            "unnamed_endpoints": {},
            "paths": {},
            "definitions": {},
            "info": {"title": "FinGemma", "version": "1.0.0"}
        }
        demo.get_api_info = types.MethodType(lambda self: empty_api, demo)
        demo.api_info = empty_api
        
        # Disable API at the app level if possible
        if hasattr(demo, 'enable_api'):
            demo.enable_api = False
    except Exception as e:
        print(f"Warning: Could not disable API: {e}")
    
    # For Docker, default to 0.0.0.0 so Gradio is accessible from outside the container
    share = os.environ.get("GRADIO_SHARE", "false").lower() == "true"
    server_name = os.environ.get("SERVER_NAME", "0.0.0.0")
    port = int(os.environ.get("PORT", 7860))
    
    print(f"Starting Gradio UI on {server_name}:{port} with LOCAL_MODEL_PATH support...")
    
    try:
        demo.launch(
            server_name=server_name, 
            server_port=port, 
            share=share, 
            show_api=False,
            show_error=True,
            prevent_thread_lock=False
        )
    except ValueError as e:
        if "shareable link" in str(e).lower():
            print("Falling back to share=True due to localhost access issue...")
            demo.launch(
                server_name="0.0.0.0", 
                server_port=port, 
                share=True, 
                show_api=False,
                show_error=True,
                prevent_thread_lock=False
            )
        else:
            raise

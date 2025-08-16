import os
import torch
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
import threading
from peft import PeftModel
from fastapi.responses import StreamingResponse, JSONResponse

MODEL_ID = os.environ.get("MODEL_ID", "huseyincavus/gemma-3-270m-finance-merged")
LOCAL_MODEL_PATH = os.environ.get("LOCAL_MODEL_PATH")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.bfloat16 if torch.cuda.is_available() else torch.float32

app = FastAPI(title="Finance Fine-tuned LLM API", version="0.1.0")

def _resolve_model_path():
    # precedence: explicit LOCAL_MODEL_PATH env, then if MODEL_ID is a local dir, else hub id
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
    base_model = AutoModelForCausalLM.from_pretrained(resolved_path, **load_kwargs)
except Exception as e:
    raise RuntimeError(f"Failed to load model from '{resolved_path}' (local={is_local}). Set LOCAL_MODEL_PATH env if needed. Original error: {e}")
model = base_model

class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9
    stream: bool = False

@app.post("/generate")
async def generate(req: GenerateRequest):
    inputs = tokenizer(req.prompt, return_tensors="pt").to(model.device)
    if req.stream:
        streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
        gen_kwargs = dict(**inputs, max_new_tokens=req.max_new_tokens, temperature=req.temperature, top_p=req.top_p, do_sample=req.temperature>0, streamer=streamer)
        thread = threading.Thread(target=model.generate, kwargs=gen_kwargs)
        thread.start()
        def token_stream():
            for token in streamer:
                yield token
        return StreamingResponse(token_stream(), media_type="text/plain")
    else:
        output_ids = model.generate(**inputs, max_new_tokens=req.max_new_tokens, temperature=req.temperature, top_p=req.top_p, do_sample=req.temperature>0)
        text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        completion = text[len(req.prompt):]
        return {"completion": completion}

@app.get("/health")
async def health():
    return {"status": "ok", "device": DEVICE, "model_path": resolved_path, "local": is_local}

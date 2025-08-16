import os, torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = os.environ.get("MODEL_ID", "huseyincavus/gemma-3-270m-finance-merged")
print(f"Loading model {MODEL_ID} ...")

device = 'cuda' if torch.cuda.is_available() else 'cpu'

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, device_map='auto', torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32)

prompt = "Explain the difference between revenue and net income in one sentence."
inputs = tokenizer(prompt, return_tensors='pt').to(model.device)
with torch.no_grad():
    output_ids = model.generate(**inputs, max_new_tokens=64, temperature=0.7, top_p=0.9, do_sample=True)
text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
print('\nFull output:\n', text)
print('\nCompletion:\n', text[len(prompt):])

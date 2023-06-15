from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
device = "mps"
import os
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'opus')

def opus(sources: List[str], lang='zh') -> List[str]:
    assert(lang != 'ko')
    tokenizer = AutoTokenizer.from_pretrained(os.path.join(PATH, lang), local_files_only=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(os.path.join(PATH, lang), local_files_only=True)
    model = model.to(device)  # Move model to GPU if available
    encoded_inputs = tokenizer(sources, return_tensors="pt", padding=True)
    encoded_inputs = {name: tensor.to(device) for name, tensor in encoded_inputs.items()}  # Move input tensors to GPU if available
    translated = model.generate(**encoded_inputs)
    return [tokenizer.decode(t, skip_special_tokens=True) for t in translated]

if __name__ == "__main__":
    print(opus(["hi hi! my name is Julia!"], lang='es'))
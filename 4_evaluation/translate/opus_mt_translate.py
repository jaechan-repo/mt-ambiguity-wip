from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
device = "cuda:0" if torch.cuda.is_available() else "cpu"
import os
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'opus')

def opus(sources: List[str], lang='zh') -> List[str]:
    print(os.path.join(PATH, lang))
    tokenizer = AutoTokenizer.from_pretrained(os.path.join(PATH, lang), local_files_only=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(os.path.join(PATH, lang), local_files_only=True)
    translated = model.generate(**tokenizer(sources, return_tensors="pt", padding=True))
    return [tokenizer.decode(t, skip_special_tokens=True) for t in translated]

if __name__ == "__main__":
    
    print(opus(["안녕, 내 이름은 줄리아야"], lang='ko'))
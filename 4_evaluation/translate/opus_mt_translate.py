from typing import List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import warnings
import os
warnings.filterwarnings("ignore")
device = "mps"
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'opus')

from torch.utils.data import DataLoader

def batch_generator(data, batch_size=4):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

def opus(sources: List[str], lang='zh', batch_size=16) -> List[str]:
    assert(lang != 'ko')
    # tokenizer = AutoTokenizer.from_pretrained(os.path.join(PATH, lang), local_files_only=True)
    # model = AutoModelForSeq2SeqLM.from_pretrained(os.path.join(PATH, lang), local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
    model = model.to(device)  # Move model to GPU if available

    translated = []
    for batch in batch_generator(sources, batch_size):
        encoded_inputs = tokenizer(batch, return_tensors="pt", padding=True)
        encoded_inputs = {name: tensor.to(device) for name, tensor in encoded_inputs.items()}  # Move input tensors to GPU if available
        generated = model.generate(**encoded_inputs)
        translated.extend([tokenizer.decode(t, skip_special_tokens=True) for t in generated])

    return translated


if __name__ == "__main__":
    print(opus(["hi hi! my name is Julia!"], lang='es'))
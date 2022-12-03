from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from tqdm import tqdm
import warnings
import pandas as pd
import torch
import time
import argparse
import os
warnings.filterwarnings("ignore")
device = "cuda:0" if torch.cuda.is_available() else "cpu"

parser = argparse.ArgumentParser(description='\
Generates a dataset given line-separated list of idioms. \
Requires prompt.txt to be in local directory.')

parser.add_argument('-f','--file', 
    help='".csv" file created by "gpt3_generation.py"', 
    required=True
)
parser.add_argument('-l', '--lang', nargs='+', 
    help='list of NLLB language codes for target translations',
    default=["kor_Hang", "fra_Latn", "heb_Hebr", "zho_Hans", "yor_Latn"]
)
parser.add_argument('-b', '--batch', 
    help='batch size',
    default=32
)
args = parser.parse_args()

if not os.path.isfile(args.file):
    raise Exception('The specified file does not exist.')

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M").to(device)

subdf = pd.read_csv(args.file)
project = args.file.split('.')[0]

def translate_batch(x, lang_code):
    inputs = tokenizer(x, return_tensors='pt', padding=True).to(device)
    translated_tokens = model.generate(
        **inputs, forced_bos_token_id=tokenizer.lang_code_to_id[lang_code]
    )
    res = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)
    return res

start = time.time()
print("Translation begins.")

for lang_code in args.lang:
    subdf[lang_code + "_idiom"] = ""
    subdf[lang_code + "_phrase"] = ""
    subdf[lang_code + "_sentence"] = ""

for i in tqdm(range(0, len(subdf), args.batch)):
    i_end = min(len(subdf), i + args.batch)
    for lang_code in args.lang:
        subdf[lang_code + "_idiom"][i: i_end] = translate_batch(subdf['idiom'][i: i_end].tolist(), lang_code)
        subdf[lang_code + "_phrase"][i: i_end] = translate_batch(subdf['phrase'][i: i_end].tolist(), lang_code)
        subdf[lang_code + "_sentence"][i: i_end] = translate_batch(subdf['sentence'][i: i_end].tolist(), lang_code)

end = time.time()
print(f"\nCompletion in {(end - start)} seconds")

subdf.to_csv(project + f'_{len(args.lang)}lang.csv', index=False)

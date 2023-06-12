from typing import List
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from transformers import AutoTokenizer, M2M100ForConditionalGeneration
import torch
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# def opus_mt_zh(sources: List[str]):
#     tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
#     model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
#     input_tokens = tokenizer(sources, return_tensors="pt", padding="longest", truncation=True)
#     translations = model.generate(**input_tokens)
#     predictions = [tokenizer.decode(t, skip_special_tokens=True) for t in translations]
#     return predictions

def nllb_translate(sources: List[str], lang: str):
    tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M").to(device)
    lang_to_lang_code = {
        'zh': 'zho_Hans',
        'ko': 'kor_Hang',
        'yo': 'yor_Latn',
        'he': 'heb_Hebr',
    }
    lang_code = lang_to_lang_code[lang]
    inputs = tokenizer(sources, return_tensors='pt', padding=True).to(device)
    translated_tokens = model.generate(
        **inputs, forced_bos_token_id=tokenizer.lang_code_to_id[lang_code]
    )
    res = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)
    return res

def m2m_translate(sources: List[str], lang: str):

    model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
    tokenizer = AutoTokenizer.from_pretrained("facebook/m2m100_418M")
    inputs = tokenizer(sources, return_tensors='pt', padding=True).to(device)

    # translate to French
    translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.get_lang_id(lang))
    res = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)
    return res
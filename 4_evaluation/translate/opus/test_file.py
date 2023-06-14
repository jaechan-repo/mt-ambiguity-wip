from transformers import MarianMTModel, MarianTokenizer

src_text = [
    "2, 4, 6 etc. are even numbers.",
    "Yes."
]

model_name = "Helsinki-NLP/opus-mt-tc-big-en-ko"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)
translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))

for t in translated:
    print( tokenizer.decode(t, skip_special_tokens=True) )

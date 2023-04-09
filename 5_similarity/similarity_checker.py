import evaluate

chrf = evaluate.load("chrf")
bertscore = evaluate.load("bertscore")

def get_chrf_precision(prediction, reference):
    prediction = [prediction]
    reference = [[reference]]
    results = chrf.compute(
        predictions=prediction, 
        references=reference,
        beta=0,
        word_order=2,
    )
    return results['score']

def get_bertscore_precision(prediction, reference):
    prediction = [prediction]
    reference = [reference]
    results = bertscore.compute(
        predictions=prediction,
        references=reference,
        lang=''
    )

print(get_chrf_precision("my name is Jaechan Lee", "my name"))
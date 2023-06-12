from evaluate import load
import numpy as np

bertscore = load("bertscore")

def compute(subsentences: np.ndarray, 
        sentences: np.ndarray,
        lang: str = 'en') -> np.ndarray:
    assert(len(subsentences) == len(sentences))
    # Replace 'xlm-mlm-100-1280' with the name of the model you're using
    results = bertscore.compute(predictions=subsentences, references=sentences, 
                                lang=lang, model_type="xlm-roberta-base")
    return results['precision'], results['recall'], results['f1']

def contained_in(subsentences: np.ndarray, 
        sentences: np.ndarray,
        lang: str = 'en') -> np.ndarray:
    p, _, _ = compute(subsentences, sentences, lang)
    return p

def sim(subsentences: np.ndarray, 
        sentences: np.ndarray,
        lang: str = 'en') -> np.ndarray:
    _, _, f = compute(subsentences, sentences, lang)
    return f

if __name__ == "__main__":
    print(contained_in(['hello', 'hello, my name is roy batty.'], 
                       ['hello, my name is roy batty', 'hello, my name is roy batty.']))
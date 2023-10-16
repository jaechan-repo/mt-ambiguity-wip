from evaluate import load
import numpy as np
from typing import Tuple

bertscore = load("bertscore")

def generate_batches(array: np.ndarray, batch_size: int):
    for i in range(0, len(array), batch_size):
        yield array[i:i + batch_size]

def compute(
        subsentences: np.ndarray, 
        sentences: np.ndarray, 
        lang: str = 'en', 
        batch_size: int = 32) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

    assert(len(subsentences) == len(sentences))

    precision_list, recall_list, f1_list = [], [], []

    subsentences_batches = generate_batches(subsentences, batch_size)
    sentences_batches = generate_batches(sentences, batch_size)

    for subsentences_batch, sentences_batch in zip(subsentences_batches, sentences_batches):
        results = bertscore.compute(predictions=subsentences_batch, references=sentences_batch, 
                                    lang=lang, model_type="xlm-roberta-base", device='mps')
        precision_list.append(results['precision'])
        recall_list.append(results['recall'])
        f1_list.append(results['f1'])

    precision = np.concatenate(precision_list, axis=0)
    recall = np.concatenate(recall_list, axis=0)
    f1 = np.concatenate(f1_list, axis=0)

    return precision, recall, f1

# def compute(subsentences: np.ndarray, 
#         sentences: np.ndarray,
#         lang: str = 'en') -> np.ndarray:
#     assert(len(subsentences) == len(sentences))
#     results = bertscore.compute(predictions=subsentences, references=sentences, 
#                                 lang=lang, model_type="xlm-roberta-base")
#     return results['precision'], results['recall'], results['f1']

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
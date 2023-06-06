import bert_score.score as score
import logging
import transformers
from transformers import AutoTokenizer
import numpy as np

transformers.tokenization_utils.logger.setLevel(logging.ERROR)
transformers.configuration_utils.logger.setLevel(logging.ERROR)
transformers.modeling_utils.logger.setLevel(logging.ERROR)

def compute(subsentences: np.ndarray, 
        sentences: np.ndarray,
        lang: str = 'en') -> np.ndarray:
    assert(len(subsentences) == len(sentences))
    # Replace 'xlm-mlm-100-1280' with the name of the model you're using
    tokenizer = AutoTokenizer.from_pretrained('xlm-mlm-100-1280')

    # Tokenize your sentences
    subsentences = [' '.join(tokenizer.tokenize(sentence)) for sentence in subsentences]
    sentences = [' '.join(tokenizer.tokenize(sentence)) for sentence in sentences]
    p, r, f = score(subsentences, sentences, lang=lang, verbose=True, model_type='xlm-mlm-100-1280')
    return p, r, f

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

def weighted_contained_in(subsentences: np.ndarray, 
        sentences: np.ndarray,
        lang: str = 'en') -> np.ndarray:
    p = contained_in(subsentences, sentences, lang)
    length_ratios = (np.array([len(s.split()) for s in subsentences]) / 
                     np.array([len(s.split()) for s in sentences]))
    length_weight = np.clip(length_ratios, 0, 1)
    adjusted_p = length_weight * p.numpy() + (1 - length_weight) * length_ratios
    return adjusted_p

if __name__ == "__main__":
    print(contained_in(['hello', 'hello, my name is roy batty.'], 
                       ['hello, my name is roy batty', 'hello']))
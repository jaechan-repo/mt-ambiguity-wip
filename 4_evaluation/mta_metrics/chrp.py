from collections import defaultdict
from nltk.translate.chrf_score import chrf_precision_recall_fscore_support
import numpy as np
import re

def _preprocess(sent, ignore_whitespace):
    if type(sent) != str:
        # turn list of tokens into a string
        sent = " ".join(sent)

    if ignore_whitespace:
        sent = re.sub(r"\s+", "", sent)
    return sent

def corpus_chrp(
    hypotheses, references, min_len=1, max_len=6, beta=3.0, ignore_whitespace=True
):

    assert len(references) == len(
        hypotheses
    ), "The number of hypotheses and their references should be the same"
    num_sents = len(hypotheses)

    # Keep f-scores for each n-gram order separate
    ngram_precs = defaultdict(lambda: list())

    # Iterate through each hypothesis and their corresponding references.
    for reference, hypothesis in zip(references, hypotheses):

        # preprocess both reference and hypothesis
        reference = _preprocess(reference, ignore_whitespace)
        hypothesis = _preprocess(hypothesis, ignore_whitespace)

        # Calculate f-scores for each sentence and for each n-gram order
        # separately.
        for n in range(min_len, max_len + 1):
            # Compute the precision, recall, fscore and support.
            prec, rec, fscore, tp = chrf_precision_recall_fscore_support(
                reference, hypothesis, n, beta=beta
            )
            ngram_precs[n].append(prec)

    # how many n-gram sizes
    num_ngram_sizes = len(ngram_precs)

    # sum of f-scores over all sentences for each n-gram order
    total_scores = [sum(precs) for _, precs in ngram_precs.items()]

    # macro-average over n-gram orders and over all sentences
    return (sum(total_scores) / num_ngram_sizes) / num_sents

def sentence_chrp(
    hypothesis, reference, min_len=1, max_len=6, beta=3.0, ignore_whitespace=True
):
    return corpus_chrp(
        [hypothesis],
        [reference],
        min_len,
        max_len,
        beta=beta,
        ignore_whitespace=ignore_whitespace,
    )

def compute_contains_batch(subsentences: np.ndarray, sentences: np.ndarray) -> np.ndarray:
    assert(len(subsentences) == len(sentences))
    percentages = [sentence_chrp(subsentence, sentence) 
                             for subsentence, sentence in zip(subsentences, sentences)]
    return np.asarray(percentages, dtype=np.float32)

if __name__ == "__main__":
    print(sentence_chrp("hello my name is Roy Batty, the Replicant.", "hello my name is"))
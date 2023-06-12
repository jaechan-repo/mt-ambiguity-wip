from collections import Counter, defaultdict
from nltk.translate.chrf_score import chrf_precision_recall_fscore_support
import numpy as np
import re
from nltk.util import ngrams

def sentence_chrf(
    reference, hypothesis, min_len=1, max_len=6, beta=3.0, ignore_whitespace=True
):
    f, p, r = corpus_chrf(
        [reference],
        [hypothesis],
        min_len,
        max_len,
        beta=beta,
        ignore_whitespace=ignore_whitespace,
    )
    return f

def sentence_chrp(
    reference, hypothesis, min_len=1, max_len=6, beta=3.0, ignore_whitespace=True
):
    f, p, r = corpus_chrf(
        [reference],
        [hypothesis],
        min_len,
        max_len,
        beta=beta,
        ignore_whitespace=ignore_whitespace,
    )
    return p

def _preprocess(sent, ignore_whitespace):
    if type(sent) != str:
        # turn list of tokens into a string
        sent = " ".join(sent)

    if ignore_whitespace:
        sent = re.sub(r"\s+", "", sent)
    return sent


def chrf_precision_recall_fscore_support(
    reference, hypothesis, n, beta=3.0, epsilon=1e-16
):
    ref_ngrams = Counter(ngrams(reference, n))
    hyp_ngrams = Counter(ngrams(hypothesis, n))

    # calculate the number of ngram matches
    overlap_ngrams = ref_ngrams & hyp_ngrams
    tp = sum(overlap_ngrams.values())  # True positives.
    tpfp = sum(hyp_ngrams.values())  # True positives + False positives.
    tpfn = sum(ref_ngrams.values())  # True positives + False negatives.

    try:
        prec = tp / tpfp  # precision
        rec = tp / tpfn  # recall
        factor = beta**2
        fscore = (1 + factor) * (prec * rec) / (factor * prec + rec)
    except ZeroDivisionError:
        prec = rec = fscore = epsilon
    return prec, rec, fscore, tp

def corpus_chrf(
    references, hypotheses, min_len=1, max_len=6, beta=3.0, ignore_whitespace=True
):

    assert len(references) == len(
        hypotheses
    ), "The number of hypotheses and their references should be the same"
    num_sents = len(hypotheses)

    # Keep f-scores for each n-gram order separate
    ngram_fscores = defaultdict(lambda: list())
    ngram_precs = defaultdict(lambda: list())
    ngram_recs = defaultdict(lambda: list())

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
            ngram_fscores[n].append(fscore)
            ngram_precs[n].append(prec)
            ngram_recs[n].append(rec)

    # how many n-gram sizes
    num_ngram_sizes = len(ngram_fscores)

    # sum of f-scores over all sentences for each n-gram order
    total_fscores = [sum(fscores) for n, fscores in ngram_fscores.items()]
    total_precs = [sum(precs) for n, precs in ngram_precs.items()]
    total_recs = [sum(recs) for n, recs in ngram_recs.items()]

    # macro-average over n-gram orders and over all sentences
    return (sum(total_fscores) / num_ngram_sizes) / num_sents, \
        (sum(total_precs) / num_ngram_sizes) / num_sents, \
        (sum(total_recs) / num_ngram_sizes) / num_sents,

def contained_in(subsentences: np.ndarray, sentences: np.ndarray) -> np.ndarray:
    assert(len(subsentences) == len(sentences))
    percentages = [sentence_chrp(sentence, subsentence) 
                             for subsentence, sentence in zip(subsentences, sentences)]
    return np.asarray(percentages, dtype=np.float32)

def sim(predictions: np.ndarray, references: np.ndarray) -> np.ndarray:
    assert(len(predictions) == len(references))
    percentages = [sentence_chrf(reference, prediction) 
                             for prediction, reference in zip(predictions, references)]
    return np.asarray(percentages, dtype=np.float32)

if __name__ == "__main__":
    print(contained_in(['hello my'], ['hello my name is']))
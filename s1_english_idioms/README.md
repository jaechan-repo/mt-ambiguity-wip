# S1. English Idioms

This section deals with constructing a dataset of English idioms, their frequencies in literature usage, and their figurative definitions. The scripts used are `get_idioms_EPIE_gpt3.py` and `get_frequencies.py`.

## T1. English idioms and their number of occurrences

To obtain English idioms and their number occurrences, we used [EPIE Corpus](https://github.com/prateeksaxena2809/EPIE_Corpus) dataset, which involves 25206 sentences labelled with lexical instances of 717 idiomatic expressions. The only data of our interest is the 717 idiomatic expressions.

> Why EPIE Corpus? One advantage of this corpus is all the idiomas here are grammar-agnostic—that is, pronouns and determiners are masked with tokens such as `[pron]` or `(det)`, which ensures their uniqueness in their meanings and convenience in processing.

## T2. Definitions of Idioms

The figurative definitions of the idioms were obtained thorugh GPT-3. The prompt, accessible in `PROMPT.txt`, is:
```
Write the idiomatic definitions of the following.

idiom: burn the bridge with [pron]
completely sever a relationship with someone, making it impossible to rekindle the relationship.

idiom: 
```

## T3. Frequencies of Idioms
We used the script `get_frequencies.py` for obtaining the number of occurrences of each idiom in `bookcorpus`.

> Why bookcorpus? More established forms of corpus, such as Wikipedia, lacks the amount of idiom usage because they try to minimize semantic ambiguity in their content as much as possible. Since idiom is fundamentally a literary element, we decided that dialogues and monologues presented in books will be fairly representative of the real-life usage of the idioms.

## Result

The result of this section is a dataset `idioms.csv` comprised of the following information:

- `idiom`: idiomatic expressions
- `meaning`: AI-generated definitions of the idiomatic expressions.
- `freq`: frequencies of the idiomatic expressions. To be used as weights of evaluation.

The rows are in the descending order of `freq` (the most frequent appearing first).

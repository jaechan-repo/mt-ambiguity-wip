# S1. English Idioms

This section deals with constructing a dataset of English idioms, their frequencies in real life usage, and their figurative definitions. The script used is `get_idioms_EPIE_gpt3.py`.

## T1. English idioms and their number of occurrences

To obtain English idioms and their number occurrences, we used [EPIE Corpus](https://github.com/prateeksaxena2809/EPIE_Corpus) dataset, which involves 25206 sentences labelled with lexical instances of 717 idiomatic expressions. The only data of our interest is the 717 idiomatic expressions and the number of instances that correspond to each idiom (i.e., "frequency"). 

> Why EPIE Corpus? One advantage of this corpus is all the idiomas here are grammar-agnostic—that is, pronouns and determiners are masked with tokens such as `[pron]` or `(det)`, which ensures their uniqueness in their meanings and convenience in processing. Another advantage is that they are not just a list of idioms but provide instances that use the idioms within a larger dataset. How many instances correspond to an idiomatic expression is fairly representative of how frequent the idiom is used in real life, which tells us how important being correct with that one idiom is during the process of evaluation. 

## T2. Definitions of Idioms

The figurative definitions of the idioms were obtained thorugh GPT-3. The prompt, accessible in `PROMPT.txt`, is:
```
Write the idiomatic definitions of the following.

idiom: burn the bridge with [pron]
completely sever a relationship with someone, making it impossible to rekindle the relationship.

idiom: 
```

## Result

The result of this section is a dataset `idioms.csv` comprised of the following information:

- `idiom`: idiomatic expressions
- `freq`: frequencies of the idiomatic expressions. To be used as weights of evaluation.
- `meaning`: AI-generated definitions of the idiomatic expressions.

The rows are in the descending order of `freq` (the most frequent appearing first).

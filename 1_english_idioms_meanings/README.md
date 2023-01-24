# 1. English Idioms and Meanings

This section deals with constructing a dataset of **English idioms**, **figurative definitions**, and **instances**. The products of this section are the following two `.csv` files.

- [1_1_dict/idioms.csv](1_1_dict/idioms.csv)
- [1_2_pfbt/idioms.csv](1_2_pfbt/idioms.csv)

## 1-1. TheIdioms.com Dictionary 

`TheIdioms.com` web dictionary is an educational organization that provides a list of idioms, definitions, and their usages. We used `BeautifulSoup` webscraping to collect and produce the [1_2_dictionary/idioms.csv](1_2_dictionary/idioms.csv) file with 1409 rows and the following columns:

- `idiom`: 1409 idiomatic expressions
- `meaning`: meanings of the idioms
- `example`: example sentences of the idioms (figurative)

## 1-2. Corpus from [this paper](https://github.com/ellarabi/gender-idiomatic-language)

Deduplicated by hand. 291 rows and the following columns:

- `idiom`: 291 idiomatic expressions
- `meaning`: meanings of the idioms
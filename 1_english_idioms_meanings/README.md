# 1. English Idioms and Meanings

This section deals with constructing a dataset of **English idioms**, **figurative definitions**, and **instances**. The products of this section are the following two `.csv` files, as their collection processes are detailed below:

- [1_1_EPIE/idioms.csv](1_1_EPIE/idioms.csv)
- [1_2_dictionary/idioms.csv](1_2_dictionary/idioms.csv)

## 1-1. EPIE Dataset

To obtain English idioms, we used [EPIE Corpus](https://github.com/prateeksaxena2809/EPIE_Corpus) dataset, which involves 25206 sentences labelled with lexical instances of 717 idiomatic expressions. The portion of the linked repository that is of our interest is also included within this folder with the name `EPIE_Corpus`. We converted the data of this whole repository to a single `.csv` file: [1_1_EPIE/idioms_EPIE.csv](1_1_EPIE/idioms_EPIE.csv).

One advantage of this corpus is the idioms are grammar-agnostic: that is, pronouns and determiners are masked with arbitrary tokens such as `[pron]` or `(det)`, which ensures their uniqueness in their meanings and convenience in processing. We gathered those **717 idioms** and ran GPT-3 on each idiom to generate their **meanings**, which are to be verified by human annotators for later use. These pairs of 717 idioms and their figurative definitions are to be found in [1_1_EPIE/idiom_meanings.csv](1_1_EPIE/idiom_meanings.csv).

Along with the idioms, we also sampled some **instances (example sentences) of idioms** that are also offered in the EPIE Corpus. The methodology of sampling is simple: for each idiom, select the longest instance that uses the idiom. The justification of this methodology is that we want the instances of the idioms to be as disambiguating as possible. Yet, the instances provided by the EPIE Corpus are naturally occurring (i.e. written by humans) sentences that are not specifically designed for a dataset generation purpose as this but for literary purposes, such as dialogues in books. Short idiomatic sentences found in literary texts are not as disambiguating as long ones: they usually rely on contexts from sentences that come before and after, which we do not have access to. Thus, the longer a sentence, the more disambiguating context we obtain.

Lastly, the tags such as `O O O O O O O O O O O O O O O O O O O O O O B-IDIOM I-IDIOM I-IDIOM I-IDIOM O O O O` that denotes where the idiom starts and ends were also collected for each instance. 

**After these steps, we acquired [1_1_EPIE/idioms.csv](1_1_EPIE/idioms.csv) with 717 rows and the following columns:**
- `idiom`: the 717 idioms of EPIE Corpus
- `meaning`: AI-generated figurative definitions of the idioms
- `example`: a collection of the longest instances for each idiom
- `tag`: a tag that corresponds to `example`

## 1-2. TheIdioms.com Dictionary 

For larger corpus, we turned to `TheIdioms.com` web dictionary, which is an educational organization that provides a list of idioms, definitions, and usages. We used `BeautifulSoup` webscraping to __collect and produce the [1_2_dictionary/idioms.csv](1_2_dictionary/idioms.csv) file with 1409 rows and the following columns:__
- `idiom`: the 1409 idioms of `TheIdioms.com`
- `meaning`: the meanings of the idioms provided by `TheIdioms.com`
- `example`: the example sentences of the idioms provided by `TheIdioms.com`

import pandas as pd
import datasets
from datasets import load_dataset
from tqdm import tqdm
import re

dataset = load_dataset("bookcorpus")['train']
df = pd.read_csv('idioms.csv')

import warnings
warnings.filterwarnings("ignore")

df['pattern'] = df['idiom'].apply(lambda x: x.replace('[pron]', '[a-zA-Z+#\-.0-9]{1,4}(\s[a-zA-Z+#\-.0-9]{1,4}){0,3}'))
datasets.disable_progress_bar()
def get_freq(pattern, dataset):
    return len(dataset.filter(
        lambda data: bool(re.search(pattern, data['text'])), num_proc=8
    )) + 1

tqdm.pandas()
df['freq'] = df['pattern'].progress_apply(
    lambda pattern: get_freq(pattern, dataset)
)

df = df.sort_values('freq', ascending=False).reset_index(drop=True)
df = df[['idiom', 'meaning', 'freq']]
df.to_csv('idioms.csv', index=False)
import pandas as pd
import os
import openai
from tqdm import tqdm
import config
import warnings
warnings.filterwarnings("ignore")

if not os.path.isdir('../EPIE_Corpus'):
    raise Exception('The EPIE Corpus directory (a dependency of this project) does not exist.')
if not os.path.isfile('PROMPT.txt'):
    raise Exception('"PROMPT.txt" must exist in local directory.')

with open('PROMPT.txt', 'r') as file:
    general_prompt = file.read()
    print()
    print()
    print("CURRENT PROMPT:")
    print()
    print(general_prompt + '[queried idiom]\n')
    print()

openai.organization = config.openai_organization
openai.api_key = config.openai_api_key

def generate(row):
    idiom = row['idiom']
    text = openai.Completion.create(
        model="text-davinci-003",
        prompt = general_prompt + f"\"{idiom}\"\n",
        max_tokens=400,
        temperature=0, # the higher this value, the less deterministic
        top_p=1, # the higher this value, the wider range of vocab is used
    ).choices[0].text.strip()
    row['meaning'] = text
    return row

print('INFERENCE IN PROGRESS...')
tqdm.pandas()

# Read formal idiom candidates and build frequency list
df1 = pd.read_csv('EPIE_Corpus/Formal_Idioms_Corpus/Formal_Idioms_Candidates.txt', header=None, names=["idiom"])['idiom'].value_counts().reset_index().rename(columns={'index': 'idiom', 'idiom': 'freq'})

# Read static idiom candidates and build frequency list
df2 = pd.read_csv('EPIE_Corpus/Static_Idioms_Corpus/Static_Idioms_Candidates.txt', header=None, names=["idiom"])['idiom'].value_counts().reset_index().rename(columns={'index': 'idiom', 'idiom': 'freq'})

# Merge two idiom datasets and sort rows by frequency
df = pd.concat([df1, df2]).sort_values(by='freq', ascending=False).reset_index(drop=True)

# Generate meaning with GPT-3
df['meaning'] = df.progress_apply(generate, axis=1)
df.to_csv('idioms.csv', index=False)
print('COMPLETED.')
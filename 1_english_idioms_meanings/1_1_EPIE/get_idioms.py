import pandas as pd
import os
import openai
from tqdm import tqdm
import config
import warnings
warnings.filterwarnings("ignore")

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

files1 = [
    './EPIE_Corpus/Formal_Idioms_Corpus/Formal_Idioms_Candidates.txt',
    './EPIE_Corpus/Formal_Idioms_Corpus/Formal_Idioms_Words.txt',
    './EPIE_Corpus/Formal_Idioms_Corpus/Formal_Idioms_Tags.txt'
]
files2 = [
    './EPIE_Corpus/Static_Idioms_Corpus/Static_Idioms_Candidates.txt',
    './EPIE_Corpus/Static_Idioms_Corpus/Static_Idioms_Words.txt',
    './EPIE_Corpus/Static_Idioms_Corpus/Static_Idioms_Tags.txt'
]
cols = ['idiom', 'example', 'tag']

df1 = pd.concat(
    [pd.read_csv(files1[i], header=None, sep='delimiter', names=[cols[i]], engine='python') for i in range(3)], axis=1
)

df2 = pd.concat(
    [pd.read_csv(files2[i], header=None, sep='delimiter', names=[cols[i]], engine='python') for i in range(3)], axis=1
)

df = pd.concat([df1, df2])
df.to_csv('EPIE.csv', index=False)

df = df[['idiom']].drop_duplicates().reset_index(drop=True)
print(df)

# Generate meaning with GPT-3
df['meaning'] = df.progress_apply(generate, axis=1)
df.to_csv('idiom_meanings.csv', index=False)

df1 = pd.read_csv('idiom_meanings.csv')
df2 = pd.read_csv('EPIE.csv') 

df2 = pd.concat([
    df2.groupby('idiom')['example'].apply(list),
    df2.groupby('idiom')['tag'].apply(list)
], axis=1, join='inner').reset_index()

def func(row):
    def argmax(seq):
        m = max(seq, key=len)
        return seq.index(m)
    i = argmax(row['example'])
    row['example'] = row['example'][i]
    row['tag'] = row['tag'][i]
    return row

df2 = df2.apply(func, axis=1)

df = pd.concat([
    df2.set_index('idiom'), df1.set_index('idiom')
], axis=1).reset_index()[['idiom', 'meaning', 'example', 'tag']]
df.to_csv('idioms.csv', index=False)
print('COMPLETED.')
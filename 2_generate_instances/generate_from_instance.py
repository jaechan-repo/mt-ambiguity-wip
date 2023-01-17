import pandas as pd
import os
import openai
import re
from tqdm import tqdm
import numpy as np
import argparse
import config
import warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(description='\
Generates a dataset given line-separated list of idioms. \
Requires prompt.txt to be in local directory.')

parser.add_argument('-f','--file', 
    help='Comma-separated list, having a list of idioms as one of its columns',
    required=True
)
parser.add_argument('-s','--sample', 
    help='Number of samples. Samples all if not specified.', 
    type=int, default=-1
)
parser.add_argument('-r', '--random', 
    help='Random seed. Does not randomize rows if not specified.', 
    type=int, default=-1
)
parser.add_argument('-o', '--output',
    help='Output file name. Must use the extension ".csv".',
    default='output_instance.csv'
)

args = parser.parse_args()

if not os.path.isfile(args.file):
    raise Exception('The specified idiom file does not exist.')
if not os.path.isfile('PROMPT_instance.txt'):
    raise Exception('"PROMPT_instance.txt" must exist in local directory.')
if args.output.split('.')[-1] != 'csv':
    raise Exception('Use ".csv" extension for your output file name.')

with open('PROMPT_instance.txt', 'r') as file:
    general_prompt = file.read()
    print()
    print()
    print("CURRENT PROMPT:")
    print()
    print(general_prompt)
    print()

df = pd.read_csv(args.file)
subdf = df.drop_duplicates(subset=['idiom']).reset_index(drop=True)
if args.random >= 0:
    subdf = subdf.sample(frac=1, random_state=args.random).reset_index(drop=True)
    print("RANDOMIZED!!")
if args.sample >= 0:
    subdf = subdf[:args.sample]

openai.organization = config.openai_organization
openai.api_key = config.openai_api_key

def generate(row):
    idiom = row['idiom']
    figurative = row['example']
    print(general_prompt.replace("[IDIOM]", idiom).replace("[FIGURATIVE]", figurative))
    text = openai.Completion.create(
        model="text-davinci-003",
        prompt = general_prompt.replace("[IDIOM]", idiom).replace("[FIGURATIVE]", figurative),
        max_tokens=400,
        temperature=0, # the higher this value, the less deterministic
        top_p=1, # the higher this value, the wider range of vocab is used
    ).choices[0].text.strip()

    phrase = re.search('phrase: (.+?)\n', text)
    if phrase: row['subsentence'] = phrase.group(1).strip('\"')

    label = [0]
    sentence = [figurative]
    
    B = re.search('literal text: (.+?)$', text)
    if B: 
        B = B.group(1).strip('\"')
        sentence.append(B)
        label.append(1)

    label += [np.nan] * (2 - len(label))
    sentence += [np.nan] * (2 - len(sentence))
    
    row['label'] = label
    row['sentence'] = sentence
    return row

print('INFERENCE IN PROGRESS...')
tqdm.pandas()
subdf = subdf.progress_apply(generate, axis=1).explode(['label', 'sentence']).reset_index(drop=True)
subdf = subdf[['idiom', 'subsentence', 'sentence', 'label']]
subdf.to_csv(args.output, index=False)

print('COMPLETED.')

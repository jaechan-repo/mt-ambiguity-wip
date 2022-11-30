import pandas as pd
import os
import openai
import re
from tqdm import tqdm
import numpy as np
import argparse
import config

parser = argparse.ArgumentParser(description='\
Generates a dataset given line-separated list of idioms. \
Requires prompt.txt to be in local directory.')

parser.add_argument('-f','--file', 
    help='Line-separated list of idioms in txt format', 
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
    default='output.csv'
)

args = parser.parse_args()

if not os.path.isfile(args.file):
    raise Exception('The specified idiom file does not exist.')
if not os.path.isfile('prompt.txt'):
    raise Exception('"prompt.txt" must exist in local directory.')
if args.output.split('.')[-1] != 'csv':
    raise Exception('Use ".csv" extension for your output file name.')

with open('PROMPT.txt', 'r') as file:
    general_prompt = file.read()
    print()
    print()
    print("CURRENT PROMPT:")
    print()
    print(general_prompt + '[queried idiom]\n')
    print()

df = pd.read_csv(args.file, header=None, names=["idiom"])
subdf = df.drop_duplicates(subset=['idiom']).reset_index(drop=True)
if args.random >= 0:
    subdf = subdf.sample(frac=1, axis=1, random_state=args.random).reset_index(drop=True)
if args.sample >= 0:
    subdf = subdf[:args.sample]

openai.organization = config.openai_organization
openai.api_key = config.openai_api_key

def generate(row):
    idiom = row['idiom']
    text = openai.Completion.create(
        model="text-davinci-003",
        prompt = general_prompt + f"\"{idiom}\"\n",
        max_tokens=400,
        temperature=0,
    ).choices[0].text.strip()

    phrase = re.search('ambiguous phrase: (.+?)\n', text)
    if phrase: row['phrase'] = phrase.group(1).strip('\"')

    label = []
    sentence = []
    reason = []

    A = re.search('figurative: (.+?)\n', text)
    if A: 
        A = A.group(1)
        A = A.split(' Here, ')
        sentence.append(A[0].strip('\"'))
        label.append(0)
        if len(A) > 1:
            reason.append('Here, ' + A[1])

    label += [np.nan] * (1 - len(label))
    sentence += [np.nan] * (1 - len(sentence))
    reason += [np.nan] * (1 - len(reason))
    
    B = re.search('literal: (.+?)$', text)
    if B: 
        B = B.group(1)
        B = B.split(' Here, ')
        sentence.append(B[0].strip('\"'))
        label.append(1)
        if len(B) > 1:
            reason.append('Here, ' + B[1])

    label += [np.nan] * (2 - len(label))
    sentence += [np.nan] * (2 - len(sentence))
    reason += [np.nan] * (2 - len(reason))
    
    row['label'] = label
    row['sentence'] = sentence
    row['reason'] = reason
    return row

print('INFERENCE IN PROGRESS...')
tqdm.pandas()
subdf = subdf.progress_apply(generate, axis=1)
subdf = subdf.explode(['label', 'sentence', 'reason']).reset_index(drop=True)
subdf = subdf[['idiom', 'phrase', 'sentence', 'label', 'reason']]
subdf.to_csv(args.output, index=False)
print('COMPLETED.')

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
    default='output_idiom.csv'
)
parser.add_argument('-i', '--iter',
    help='The number of iteration',
    type=int, default=1
)

args = parser.parse_args()

if not os.path.isfile(args.file):
    raise Exception('The specified idiom file does not exist.')
if not os.path.isfile('PROMPT_generate_pairs.txt'):
    raise Exception('"PROMPT_generate_pairs.txt" must exist in local directory.')
if args.output.split('.')[-1] != 'csv':
    raise Exception('Use ".csv" extension for your output file name.')

with open('PROMPT_generate_pairs.txt', 'r') as file:
    general_prompt = file.read()
    print()
    print()
    print("CURRENT PROMPT:")
    print()
    print(general_prompt + '[queried idiom]\n')
    print()

df = pd.read_csv(args.file)
subdf = df.drop_duplicates(subset=['idiom']).reset_index(drop=True)
if args.random >= 0:
    subdf = subdf.sample(frac=1, random_state=args.random).reset_index(drop=True)
if args.sample >= 0:
    subdf = subdf[:args.sample]

openai.organization = config.openai_organization
openai.api_key = config.openai_api_key

def generate(row):
    try:
        return generate_helper(row)
    except:
        return generate_helper(row)

def generate_helper(row):
    idiom = row['idiom']
    text = openai.Completion.create(
        model="text-davinci-003",
        prompt = general_prompt + f"\"{idiom}\"\n",
        max_tokens=400,
        temperature=1, # the higher this value, the less deterministic
        top_p=1, # the higher this value, the wider range of vocab is used
    ).choices[0].text.strip()

    phrase = re.search('ambiguous phrase: (.+?)\n', text)
    if phrase: row['subsentence'] = phrase.group(1).strip('\"')

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
subdf_gpt = pd.DataFrame(columns=['idx', 'idiom', 'meaning', 'subsentence', 'sentence', 'label', 'reason'])
for i in range(args.iter):
    subdf_gpt_local = subdf.progress_apply(generate, axis=1)
    subdf_gpt_local = subdf_gpt_local.explode(['label', 'sentence', 'reason']).reset_index(drop=True)
    print(subdf_gpt_local)
    subdf_gpt_local = subdf_gpt_local[['idiom', 'meaning', 'subsentence', 'sentence', 'label', 'reason']]
    subdf_gpt_local['idx'] = 0
    subdf_gpt_local['idx'][::2] = subdf_gpt_local.index[::2] * args.iter + 2 * i
    subdf_gpt_local['idx'][1::2] = subdf_gpt_local.index[::2] * args.iter + 2 * i + 1
    subdf_gpt = pd.concat([subdf_gpt, subdf_gpt_local])
subdf_gpt = subdf_gpt.set_index('idx').sort_index(ascending=True)
subdf_gpt.to_csv(args.output, index=False)
print('COMPLETED.')

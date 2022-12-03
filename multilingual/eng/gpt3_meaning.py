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
    help='Line-separated list of idioms in txt format', 
    required=True
)
parser.add_argument('-o', '--output',
    help='Output file name. Must use the extension ".csv".',
    default='meaning.csv'
)

args = parser.parse_args()

if not os.path.isfile(args.file):
    raise Exception('The specified idiom file does not exist.')
if args.output.split('.')[-1] != 'csv':
    raise Exception('Use ".csv" extension for your output file name.')
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
df = pd.read_csv(args.file, header=None, names=["idiom"])

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
df = df.progress_apply(generate, axis=1)
df.to_csv(args.output, index=False)
print('COMPLETED.')

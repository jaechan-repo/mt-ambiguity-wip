import argparse
import random
import itertools
import os
import tempfile
import warnings
warnings.filterwarnings("ignore")

from awesome_align.tokenization_bert import BasicTokenizer

def main():
  parser = argparse.ArgumentParser()
  
  parser.add_argument(
        "--data_file", default=None, type=str, required=True, help="The input data file (a text file)."
    )

  parser.add_argument(
        "--output_file", default=None, type=str, required=False, help="The output data file to write (a text file)."
    )
  
  args = parser.parse_args()
  file_path=args.data_file

  write_path=args.output_file
  if write_path == None:
      stdout = True
  else:
      w_f = open(write_path, "w")
      stdout=False
  
  # Default Arguments for Cased Multlingual
  tokenizer = BasicTokenizer()

  assert os.path.isfile(file_path)
  examples = []
  with open(file_path, encoding="utf-8") as f:
      for idx, line in enumerate(f.readlines()):
          if len(line) == 0 or line.isspace() or not len(line.split(' ||| ')) == 2:
              raise ValueError(f'Line {idx+1} is not in the correct format!')

          src, tgt = line.split(' ||| ')
          if src.rstrip() == '' or tgt.rstrip() == '':
              raise ValueError(f'Line {idx+1} is not in the correct format!')

          sent_src, sent_tgt = src.strip() , tgt.strip()
          token_src, token_tgt = tokenizer.tokenize(sent_src) , tokenizer.tokenize(sent_tgt)
          token_src_string, token_tgt_string = ' '.join([t for t in token_src]) , ' '.join([t for t in token_tgt])

          if stdout:
              print(token_src_string + ' ||| ' + token_tgt_string)
          else:
              w_f.write(token_src_string + ' ||| ' + token_tgt_string + '\n')

  if stdout==False:
      w_f.close()

if __name__ == "__main__":
    main()

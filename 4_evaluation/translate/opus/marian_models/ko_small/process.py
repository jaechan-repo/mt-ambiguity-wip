src = "/Users/chany/research/mt-ambiguity/4_evaluation/translate/opus/marian_models/ko_small/opusTCv20210807+bt.spm32k-spm32k.src.vocab"
trg = "/Users/chany/research/mt-ambiguity/4_evaluation/translate/opus/marian_models/ko_small/opusTCv20210807+bt.spm32k-spm32k.trg.vocab"
output = "/Users/chany/research/mt-ambiguity/4_evaluation/translate/opus/marian_models/ko_small/merged_vocab.yml"
num = 33187

from ruamel.yaml import YAML

def create_vocab_file(src_path, trg_path, output_path, vocab_size):
    # Initialize YAML
    yaml = YAML()
    yaml.default_flow_style = False

    with open(src_path, 'r', encoding='utf-8') as f_src, open(trg_path, 'r', encoding='utf-8') as f_trg:
        # Read files
        src_vocab = f_src.read().split('\n')
        trg_vocab = f_trg.read().split('\n')

    # Append lists 
    merged_vocab = src_vocab + trg_vocab

    # Remove duplicates while preserving order
    seen = set()
    merged_vocab = [x for x in merged_vocab if not (x in seen or seen.add(x))]

    # Create vocab dict
    vocab_dict = {word: i for i, word in enumerate(merged_vocab[:vocab_size])}

    with open(output_path, 'w', encoding='utf-8') as f_out:
        # Write the dict to YAML file
        yaml.dump(vocab_dict, f_out)


create_vocab_file(src, trg, output, num - 1)
from typing import List
import evaluate
import statistics
from comet import download_model, load_from_checkpoint
import pandas as pd

bleu = evaluate.load('bleu')
meteor = evaluate.load('meteor')
chrf = evaluate.load('chrf')
bertscore = evaluate.load('bertscore')
comet_da = load_from_checkpoint(download_model("Unbabel/wmt22-comet-da"))
comet_qe_da = load_from_checkpoint(download_model("Unbabel/wmt20-comet-qe-da"))

def bleu_sim(predictions: List[str], 
        references: List[str]) -> float:
    return bleu.compute(predictions=predictions, 
                           references=[[reference] for reference in references])['bleu']

def meteor_sim(predictions: List[str], 
        references: List[str]) -> float:
    return meteor.compute(predictions=predictions, references=references)['meteor'] 

def chrf_sim(predictions: List[str], 
        references: List[str]) -> float:
    return chrf.compute(predictions=predictions, 
                           references=[[reference] for reference in references])['score'] / 100

def bertscore_sim(predictions: List[str], 
        references: List[str]) -> float:
    return statistics.mean(bertscore.compute(predictions=predictions, 
                                             references=references,
                                             model_type='xlm-roberta-base')['f1'])

def comet_sim(predictions: List[str], 
        references: List[str], sources: List[str],
        gpus: int=0, accelerator="auto", devices=None) -> float:
    params = { 'src': sources, 'mt': predictions, 'ref': references }
    data = []
    for i in range(len(params['src'])):
        map_dict = {key: params[key][i] for key in params}
        data.append(map_dict)
    return comet_da.predict(data, 
                            gpus=gpus, 
                            accelerator=accelerator,
                            devices=devices)

def comet_qe(predictions: List[str], 
        sources: List[str],
        gpus: int = 0,
        accelerator = "auto",
        devices = None) -> float:
    params = { 'src': sources, 'mt': predictions }
    data = []
    for i in range(len(params['src'])):
        map_dict = {key: params[key][i] for key in params}
        data.append(map_dict)
    return comet_qe_da.predict(data, 
                               gpus=gpus, 
                               accelerator=accelerator, 
                               devices=devices)

if __name__ == "__main__":
    predictions = ["Good monring, how are you?"]
    references = ["Good morning, how have you been lately?"]
    sources = ["좋은 아침이예요, 그동안 어떻게 지내셨어요?"]
    # print("BLUE: ", bleu_sim(predictions, references))
    print("METEOR: ", meteor_sim(predictions, references))
    print("chrF: ", chrf_sim(predictions, references))
    print("BERTScore: ", bertscore_sim(predictions, references))
    print("COMET: ", comet_sim(predictions, references, sources))
    print("COMET-QE: ", comet_qe(predictions, sources))


    
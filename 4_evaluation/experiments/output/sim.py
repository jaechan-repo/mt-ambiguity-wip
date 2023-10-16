from typing import List
import evaluate
import statistics
from comet import download_model, load_from_checkpoint

def bleu_sim(predictions: List[str], 
        references: List[str], lang='en') -> float:
    bleu = evaluate.load('sacrebleu')
    if lang == 'zh':
        tokenize = 'zh'
    elif lang == 'ko':
        from mecab import MeCab
        mecab = MeCab()
        tokenize = 'none'
        predictions = [' '.join(mecab.morphs(prediction)) for prediction in predictions]
        references= [' '.join(mecab.morphs(reference)) for reference in references]
    else:
        tokenize = 'intl'
    return bleu.compute(predictions=predictions, 
                references=[[reference] for reference in references],
                tokenize=tokenize,
                lowercase=True)['score']

def meteor_sim(predictions: List[str], 
        references: List[str]) -> float:
    meteor = evaluate.load('meteor')
    return meteor.compute(predictions=predictions, references=references)['meteor'] 

def chrf_sim(predictions: List[str], 
        references: List[str]) -> float:
    chrf = evaluate.load('chrf')
    return chrf.compute(predictions=predictions, 
                           references=[[reference] for reference in references])['score'] / 100

def bertscore_sim(predictions: List[str], 
        references: List[str]) -> float:
    bertscore = evaluate.load('bertscore')
    return statistics.mean(bertscore.compute(predictions=predictions, 
                                             references=references,
                                             model_type='xlm-roberta-base')['f1'])

def comet_sim(predictions: List[str], 
        references: List[str], sources: List[str],
        gpus: int=0, accelerator="auto", devices=None) -> float:
    comet_da = load_from_checkpoint(download_model("Unbabel/wmt22-comet-da"))
    params = { 'src': sources, 'mt': predictions, 'ref': references }
    data = []
    for i in range(len(params['src'])):
        map_dict = {key: params[key][i] for key in params}
        data.append(map_dict)
    return comet_da.predict(data, 
                            gpus=gpus, 
                            accelerator=accelerator,
                            devices=devices)

if __name__ == "__main__":

    predictions = ["좋은 아침이예요, 그동안 어떻게 지내셨나요?"]
    references = ["좋은 아침이예요, 그동안 어떻게 지내셨어요?"]
    sources = ["좋은 아침이예요, 그동안 어떻게 지내셨어요?"]
    print("BLUE: ", bleu_sim(predictions, references, lang='ko'))
    print("METEOR: ", meteor_sim(predictions, references))
    print("chrF: ", chrf_sim(predictions, references))
    print("BERTScore: ", bertscore_sim(predictions, references))
    print("COMET: ", comet_sim(predictions, references, sources))


    
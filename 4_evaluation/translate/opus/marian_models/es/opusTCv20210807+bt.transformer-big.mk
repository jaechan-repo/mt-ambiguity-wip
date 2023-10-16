# eng-spa training data bigger than 10000000
GPUJOB_HPC_MEM = 16g
GPUJOB_SUBMIT  = -gpu01
SUBWORD_VOCAB_SIZE    = 32000
DEVSIZE    = 5000
TESTSIZE   = 10000
DEVMINSIZE = 200
SUBWORD_SRCVOCAB_SIZE  = 32000
SUBWORD_TRGVOCAB_SIZE  = 32000
SRCLANGS    = eng
TRGLANGS    = spa
SKIPLANGS   = 
LANGPAIRSTR = eng-spa
DATASET     = opusTCv20210807+bt
TRAINSET    = Tatoeba-train-v2021-08-07
DEVSET      = Tatoeba-dev-v2021-08-07
TESTSET     = Tatoeba-test-v2021-08-07
PRE         = simple
SUBWORDS    = spm
SHUFFLE_DATA      = 0
MAX_OVER_SAMPLING = 50
USE_REST_DEVDATA  = 0
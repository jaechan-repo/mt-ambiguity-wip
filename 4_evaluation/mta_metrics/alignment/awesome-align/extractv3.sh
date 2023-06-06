SRC="${1##*/}"
TRG="${2##*/}"

COMBINE="$SRC.$TRG"
python combine.py $1 $2 $COMBINE

ALIGN_INPUT_FILE=$COMBINE
MODEL_NAME_OR_PATH=bert-base-multilingual-cased
ALIGN_OUTPUT_FILE="$COMBINE".aligned
BATCH_SIZE=4
CACHE_DIR="./hf_models"

CUDA_VISIBLE_DEVICES=1 awesome-align \
    --output_file=$ALIGN_OUTPUT_FILE \
    --model_name_or_path=$MODEL_NAME_OR_PATH \
    --data_file=$ALIGN_INPUT_FILE \
    --extraction 'softmax' \
    --batch_size $BATCH_SIZE \
    --cache_dir $CACHE_DIR

python split.py $COMBINE $SRC $TRG
python read_alignments.py $1 $2 "$COMBINE".aligned

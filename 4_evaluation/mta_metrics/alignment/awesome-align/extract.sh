DATA_FILE=./ende.txt
MODEL_NAME_OR_PATH=bert-base-multilingual-cased
OUTPUT_FILE=./deen.out

python run_align.py \
    --output_file=$OUTPUT_FILE \
    --model_name_or_path=$MODEL_NAME_OR_PATH \
    --data_file=$DATA_FILE \
    --extraction 'softmax' \
    --batch_size 4 \

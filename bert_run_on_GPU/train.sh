export BERT_TINY_DIR=./uncased_L-2_H-128_A-2/uncased_L-2_H-128_A-2
export DATA_DIR=./MRPC/MRPC

python classifier_onGPU.py \
	--task_name=MRPC \
	--do_train=true \
	--do_eval=true \
	--data_dir=$DATA_DIR/MRPC \
	--vocab_file=$BERT_TINY_DIR/vocab.txt \
	--bert_config_file=$BERT_TINY_DIR/bert_config_file \
	--init_checkpoint=$BERT_TINY_DIR/bert_model.ckpt \
	--max_seq_length=128 \
	--train_batch_size=32 \
	--learning_rate=2e-5 \
	--num_train_epoches=3.0 \
	--output_dir=./tmp/output/
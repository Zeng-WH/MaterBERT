export BERT_TINY_DIR=./uncased_L-2_H-128_A-2/uncased_L-2_H-128_A-2
python run_pretraining.py \
	--input_file=Yourcorpus/tf_examples.tfrecord \
	--output_dir=/tmp/pretraining_output \
  	--do_train=True \
  	--do_eval=True \
  	--bert_config_file=$BERT_TINY_DIR/bert_config.json \
  	--init_checkpoint=$BERT_TINY_DIR/bert_model.ckpt \
  	--train_batch_size=32 \
  	--max_seq_length=128 \
  	--max_predictions_per_seq=20 \
  	--num_train_steps=20 \
  	--num_warmup_steps=10 \
  	--learning_rate=2e-5
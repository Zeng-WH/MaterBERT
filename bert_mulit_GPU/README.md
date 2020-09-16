# BERT MULITI GPU ON ONE MACHINE

We use MirroerdStrategy to train BERT on muliti GPU on one machine.

## Requirements

python==3

tensorflow==1.14.0

## Training

代码示例：

```shell
python run_pretraining.py \
  --input_file=*.tfrecord \
  --output_dir=test \
  --do_train=True \
  --do_eval=True \
  --n_gpus=2 \
  --bert_config_file=bert_config.json \
  --init_checkpoint=bert_model.ckpt \
  --train_batch_size=32 \
  --max_seq_length=128 \
  --max_predictions_per_seq=20 \
  --num_train_steps=1000 \
  --num_warmup_steps=10 \
  --learning_rate=2e-5
```

## Notice

在`run_pretraining.py`设置`n_gpus`的数目来设置GPU的数目。

在参数中设置的`batch_size`为每一个GPU的`batch_size`, 不是`global_batch_size`, `global_batch_size`的大小为每一个GPU的`batch_size`之和 。


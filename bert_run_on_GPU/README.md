## BERT Run on GPU

#### 概述

将bert模型通过Estimator实现，并且能将相应的指标变化显示在tensorboard上。目前只改下了run_classifier与run_pretraing这两部分，后续会继续改写其他部分。

#### 环境要求

`python==3.5`

`tensorflow==1.15.2`

（其他配置没有尝试过）

#### 运行

`bash train.sh`  （运行文件run_classifier.py）

`bash runpretraining.sh`  (运行run_pretraing.py)

#### 后续

敬请期待
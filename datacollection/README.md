# Data Collection

## 概述

利用`dois.txt`中提供的`doi`爬取文献，提取文献的摘要，如果是`openaccess`的文章，同时提取全文。

## 环境要求

`python==3.7+`

`requests==2.22.0`

## 运行

### 从爱斯维尔（Elsevier）按照doi爬取文献

`python collect_data_elsevier.py <dois file> <output file> <start> <end> <APIkey>`

`<dois file>` 待爬取的doi列表文件

`<output file>` 输出文件

`<start>` 开始爬取doi位置

`<end>` 结束爬取doi位置

`<APIkey>`你的APIkey (请从爱斯维尔官网获取)

### 从斯普林格（Springer）按照学科爬取文献

`python SpringInput.py <output file> <start_loc> <end_loc> <interval> <subject> <APIkey>`

`<output file>`输出文件

`<start_loc>`开始爬取的文件的位置

`<enc_loc>` 终止爬取的位置

`<interval>` 在一个进程中爬取的文献数，设置为0-100（建议设置为20左右）
`<subject>` 爬取的文献的科目

`<APIkey>`你的APIkey (请从斯普林格官网获取)
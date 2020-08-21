# Data Collection

## 概述

利用`dois.txt`中提供的`doi`爬取文献，提取文献的摘要，如果是`openaccess`的文章，同时提取全文。

## 环境要求

`python==3.7+`

`requests==2.22.0`

## 运行

`python collect_data_elsevier.py <dois file> <output file> <start> <end> <APIkey>`

`<dois file>` 待爬取的doi列表文件

`<output file>` 输出文件

`<start>` 开始爬取doi位置

`<end>` 结束爬取doi位置

`<APIkey>`你的APIkey (请从爱斯维尔官网获取)


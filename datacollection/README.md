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

### 基于ftp协议从云服务器上下载语料库

#### 环境要求

`python==3.5 +`

`paramiko==2.7.2`

#### 运行

`python aliyun_to_colab.py <host> <port> <username> <password> <local_dir> <remote_dir> <start_loc> <end_loc>`

`<host>`主机地址

`<port>`端口号

`<username>`username

`<password>`密码

`<local_dir>`本地文件夹

`<remote_dir>`远程主机对应的文件夹

`<start_loc>`开始下载文件的位置

`<end_loc>`终止下载文件的位置

### 句子分割

#### 运行

`python segment_sentence.py <start_loc> <end_loc> <input_dir> <output_dir>`


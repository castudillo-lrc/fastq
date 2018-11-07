# fastq文件操作脚本集合

## 统计fastq序列长度文件

包括不完整fastq文件，因为有seq判定的过程，不以四行为操作

`fq_len_stat.py`

useage:
```sh
python3 fq_len_stat.py [fastq file]
``` 

output:
```
四列分别为：
"reads_length","num_reads","percent","cum_percent"
序列长度	数目	比例	累积比例
```

## fastq 转化为fasta

包括不完整fastq文件，因为有seq判定的过程，不以四行为操作

`fq_to_fa.py`

useage:
```sh
python3 fq_to_fa.py [fastq file]
```

output:
```
序列文件
```

## fastq序列截取

指定截取的长度，选择截取的起始位置

useage:
```sh
usage: fq_truncate.py [-h] [-f FILE] [--f1 F1] [--f2 F2]
                      [--get_base_from GET_BASE_FROM] [--truncate TRUNCATE] -o
                      OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  fastq file; single end #单端数据输入文件
  --f1 F1               fastq file; R1 file  #双端R1文件
  --f2 F2               fastq file; R2 file #双端R2文件
  --get_base_from GET_BASE_FROM #从第几个序列开始截取，起始index=0
                        skip the first 'get_base_from - 1' base, default=0,
                        index starts from 0,not 1
  --truncate TRUNCATE   the read of length you what,default=75 #想要截取的序列长度
  -o OUTPUT, --output OUTPUT #输出文件的前缀
                        output file name prefix

```

output:
```
fastq file with compress gzip
```

## 获取指定前缀的fastq文件

`get_samples_fq_list.py`

useage:
```sh
python3 get_samples_fq_list.py [fq.gz path] [filenames]
```

output:
```
屏幕输出为文本格式：
filename	filename_L001_R1.fastq.gz,filename_L002_R1.fastq.gz	filename_L001_R2.fastq.gz,filename_L002_R2.fastq.gz
```

#!/usr/bin/env python3
import sys
import os
import re
import pandas as pd

def is_sample(i,ss):
    img = re.compile( ss + "_S\d_L(\d\d\d)_R(\d)_001.fastq.gz")
    x = img.findall(i)
    return ss,x

def GetFiles(f=None,ss=None):
    fs = os.listdir(f)
    ii = 0

    for  i in fs:
        ss,x = is_sample(i,ss)
        if x:
            ii += 1
            dff = pd.DataFrame({'full_name':[i],"sample":[ss],"line":[int(x[0][0])],"read":[int(x[0][1])]})
            if ii == 1 :
                df = dff
            else:
                df = pd.concat([df,dff])
    df = df.sort_values(by=['read','line'],ascending=True)

    R1 = list(df.query("read == 1").full_name)
    R2 = list(df.query("read == 2").full_name)
    if len(R1) != len(R2):
        print("{ss} the number of read1 is unequal read2,please check!!!!",file=sys.stderr)
        exit(1)
    else:
        print(ss,','.join([os.path.join(f,i) for i in R1]),','.join([os.path.join(f,i) for i in R2]),sep="\t")
    #return 1

if __name__ == "__main__":
    try:
        f = sys.argv[1]
        samples = sys.argv[2:]
        for ss in samples:
            GetFiles(f=f, ss=ss)
    except:
        print("python3 script [fq.gz path] [filenames]",file=sys.stderr)
        exit(1)


#f = "/data/NextSeq500/181023_NB502022_0073_AHKHNMBGX5/Intensities/BaseCalls"
#GetFiles(f=f,ss="JAERA20180010-3")

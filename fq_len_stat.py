#!/usr/bin/env python3
import sys
import gzip
import os

def Id(l_set):
    bases = ['A','T','G','C',"N"]
    if len(l_set) > 5:
        return False
    logi = [i in bases for i in l_set]
    if False in logi:
        return False
    else:
        return True

def Xopen2(path):
    if os.path.exists(path):
        with gzip.open(path, 'rt') as pf:
            for line in pf:
                yield line
    else:
        print('the path [{}] is not exist!'.format(path))

def Xopen(f):
    seq_len = {}
    if f.endswith(".gz"):
        handle = Xopen2(f)
    else:
        handle = open(f)
    for line in handle:
        line = line.strip()
        if not line:continue
        if line == "+":continue
        if line[0] in ['A','T','G','C',"N"]:
            l_set = set(list(line))
            if Id(l_set):
                #print(line)
                ln = len(line)
                seq_len[ln] = seq_len.get(ln,0)
                seq_len[ln] += 1

    all_reads = sum(seq_len.values())
    #print(seq_len)
    print("reads_length","num_reads","percent","cum_percent",sep="\t")
    cum = 0
    for length in sorted(seq_len.keys()):
        p = (seq_len[length]/all_reads)*100
        cum += p
        print(length,seq_len[length],p,cum,sep= "\t")

if __name__ == "__main__":
    info = """
    #the length of reads statistic#

    input file can be gzip file(endswith .gz) or txt file which contains sequences

    """

    if len(sys.argv[1:]) == 1:
        try:
            Xopen(sys.argv[1])
        except:
            #print("python3 script [fastq file or fasta file]",file=sys.stderr)
            sys.exit(1)
    else:
        print(info,file=sys.stderr)
        print("\tpython3 script [fastq file]\n", file=sys.stderr)
# f = "/project/Genetic/Z1810ADNGS_RNA/20181029/c23/JAERA20180010-2/Unmapped.out.mate1"
# Xopen(f)
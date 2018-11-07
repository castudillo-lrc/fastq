#!/usr/bin/env python3
import sys
import gzip
import os
import argparse
import subprocess
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

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

def Truncate(seq,skip_base,truncate):
    if len(seq) < truncate + skip_base:
        return None
    return seq[skip_base:truncate+skip_base]


def Xopen(f=None,skip_base=None,truncate=None,out=None):
    out = out+".fastq"

    if f.endswith(".gz"):
        handle = Xopen2(f)
    else:
        handle = open(f)
    out_th = open(out,'w')
    i = 0
    reads = []
    truncate_seq = None
    for line in handle:
        line = line.strip()
        if not line:continue

        i += 1
        if i == 1:
            reads.append(line)
        elif i == 2:
            truncate_seq =Truncate(seq=line,skip_base=skip_base,truncate=truncate)
            if truncate_seq:
                reads.append(truncate_seq)
            else:
                reads = []
        elif i == 3:
            if truncate_seq:
                reads.append(line)
        elif i == 4:
            if truncate_seq:
                reads.append(line[skip_base:truncate+skip_base])
            i = 0
            if reads:
                print("\n".join(reads),file=out_th)
                reads = []
    out_th.close()

def Xopen_two(f1=None,f2=None,skip_base=None,truncate=None,out=None):
    R1 = out + "_R1.fastq"
    R2 = out + "_R2.fastq"

    if f1.endswith(".gz"):
        handle1 = Xopen2(f1)
    else:
        handle1 = open(f1)

    if f2.endswith(".gz"):
        handle2 = Xopen2(f2)
    else:
        handle2 = open(f2)

    out_th1 = open(R1,'w')
    out_th2 = open(R2,'w')
    i = 0
    reads_1 = [];reads_2 = []
    truncate_seq1 = None
    truncate_seq2 = None

    for line1,line2 in zip(handle1,handle2):
        line2 = line2.strip()
        line1 = line1.strip()
        if not line1 or not line2:continue

        i += 1
        if i == 1:
            reads_1.append(line1)
            reads_2.append(line2)
        elif i == 2:
            truncate_seq1 =Truncate(seq=line1,skip_base=skip_base,truncate=truncate)
            truncate_seq2 =Truncate(seq=line2,skip_base=skip_base,truncate=truncate)

            if truncate_seq1 and truncate_seq2:
                reads_1.append(truncate_seq1)
                reads_2.append(truncate_seq2)
            else:
                reads_1 = []
                reads_2 = []
        elif i == 3:
            if truncate_seq1 and truncate_seq2:
                reads_1.append(line1)
                reads_2.append(line2)
        elif i == 4:
            if truncate_seq1 and truncate_seq2:
                reads_1.append(line1[skip_base:truncate+skip_base])
                reads_2.append(line2[skip_base:truncate+skip_base])
            i = 0
            if reads_1 and reads_2:
                print("\n".join(reads_1),file=out_th1)
                print("\n".join(reads_2),file=out_th2)
                reads_1 = [];reads_2 = []
    out_th1.close()
    out_th2.close()


def Get_par():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file",default=None,help="fastq file; single end")
    parser.add_argument("--f1",default=None,help="fastq file; R1 file")
    parser.add_argument("--f2",default=None,help="fastq file; R2 file")
    parser.add_argument("--get_base_from",default=0,type=int,help="skip the first 'get_base_from - 1' base, default=0, index starts from 0,not 1 ")
    parser.add_argument("--truncate",default=75,type=int,help="the read of length you what,default=75")
    parser.add_argument("-o","--output",help="output file name prefix",required=True)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    par = Get_par()
    logging.info('input parameters: {}'.format(str(par)))
    if par.file:
        logging.info("start to truncate single end reads")
        Xopen(f=par.file,skip_base=par.get_base_from,truncate=par.truncate,out=par.output)
        logging.info("end with truncating single end reads")
        out = par.output + ".fastq"
        logging.info("start to compress with truncated reads")
        try:
            subprocess.check_call('gzip -f {}'.format(out), shell=True)
            logging.info("compressing successfully finished")
        except:
            logging.error("compressing err: {}".format(out))

    elif par.f1 and par.f2:
        logging.info("start to truncate pair end reads")
        Xopen_two(f1=par.f1,f2=par.f2,skip_base=par.get_base_from,truncate=par.truncate,out=par.output)
        logging.info("end with truncating pair end reads")
        R1 = par.output + "_R1.fastq"
        R2 = par.output + "_R2.fastq"
        #try:
        logging.info("start to compress with R1 and R2 files")
        child = subprocess.Popen("gzip -f {}".format(R1),shell=True)
        child1 = subprocess.Popen("gzip -f {}".format(R2),shell=True)
        child.wait()
        child1.wait()
        logging.info("compressing successfully finished ")


        #except:
        #    logging.error("compressing err: {}".format(R1+","+R2))
    else:
        #print("'-h' for seeking help",file=sys.stderr)
        logging.error("'-h' for seeking help information")
        exit(1)


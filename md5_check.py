#!/usr/bin/env python3
import os
import logging
import sys


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    filename='md5.log',
                    datefmt='%a, %d %b %Y %H:%M:%S')
def File_check(f):
    if not os.path.isfile(f):
        logging.error("{} is not exits".format(f))
        return False
    else:
        return True


def Get_raw_md5(f):
    md5_F = os.path.abspath(f) + ".md5"
    if File_check(md5_F):
        with open(md5_F) as handle:
            md5 = handle.read().strip().split(None)[0]
    else:
        md5 = "NA"
        logging.warn("{} raw md5 file is not exists".format(md5_F))
    return md5

def Get_now_md5(f):
    md5 = list(os.popen("md5sum {}".format(f)))[0].strip().split(None)[0]
    return md5

def main(f):
    if File_check(f):
        logging.info("handle {}".format(f))
        rawmd5 = Get_raw_md5(f)
        nowmd5 = Get_now_md5(f)
        logging.info("raw:{raw} now:{now}".format(raw=rawmd5,now=nowmd5))
        if rawmd5 == nowmd5:
            logging.info("{} md5 check is done".format(os.path.basename(f)))
        else:
            logging.error("{} file is not complete".format(f))

if __name__ == "__main__":
    fs = sys.argv[1:]
    if fs:
        fs = sys.argv[1:]
        [main(f) for f in fs]
    else:
        print("\nfile and their md5 file must be at the same directory\npython3 script [files]\n")

# f = "/data/Customer/CancerCells/20181114/Sample_R18063688LU01-YC001/R18063688LU01-YC001_combined_R1.fastq.gz"
# main(f)

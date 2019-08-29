import time
import sys


def follow(arq):
    arq.seek(0,2)
    while True:
        line = arq.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line


if __name__ == '__main__':
    
    print("SAIDA:",sys.argv[0])
    # logfile = open('log.txt')
    # for line in follow(logfile):
    #     print (line)





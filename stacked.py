#!/usr/bin/python3
import subprocess
import os

if __name__ == '__main__':
    src='/home/zkx/data/tag/ctb5.training.tag'
    #src='/home/zkx/data/tag/ctb5.test.tag'
    train=[]
    for line in open(src):
        line=line.strip()
        train.append(line)
    N=10
    for i in range(N):
        subprocess.Popen(r"""awk '(((NR-NR%%30)/30)%%10) != %(ind)i' %(src)s > train.tag"""%{
            'ind':i,
            'src':src,
            },
                shell=True).wait()
        subprocess.Popen(r"""awk '(((NR-NR%%30)/30)%%10) == %(ind)i' %(src)s > test.tag"""%{
            'ind':i,
            'src':src,
            },
                shell=True).wait()
        os.system('wc train.tag')
        os.system('wc test.tag')

        sp=subprocess.Popen(r'./char_based.py --model _model --iteration=10 --train train.tag',shell=True).wait()
        sp=subprocess.Popen(r'./char_based.py --model _model --test test.tag --threshold=15 > test_%i.lattice'%(i),
                shell=True).wait()
    sp=subprocess.Popen(r"""cat test_*.lattice > train.lattice""",shell=True)
    sp.wait()

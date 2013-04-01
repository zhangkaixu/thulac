#!/usr/bin/python3
import subprocess

class Folds :
    def __init__(self,train,N=10,block_size=30):
        blocks=[]
        block=[]
        for i in range(len(train)):
            if i%block_size ==0 and block :
                blocks.append(block)
                block=[]
            block.append(train[i])
        if block :
            blocks.append(block)

        self.N=N
        self.blocks=blocks

    def train_and_test(self,res,mode=None):
        if mode is None : mode=self.N
        train=[]
        test=[]
        for i in range(len(self.blocks)) :
            (test if (i%self.N==res)else train).extend(self.blocks[i])
        return train,test

if __name__ == '__main__':
    src='/home/zkx/data/tag/ctb5.training.tag'
    train=[]
    for line in open(src):
        line=line.strip()
        train.append(line)
    N=10
    folds=Folds(train,N=N)
    for i in range(N):
        train,test=folds.train_and_test(i)

        outf=open('train.tag','w')
        for x in train : print(x,file=outf)
        outf.close()

        outf=open('test.tag','w')
        for x in test : print(x,file=outf)
        outf.close()

        sp=subprocess.Popen(r'./char_based.py --model _model --iteration=10 --train train.tag',shell=True)
        sp.wait()
        sp=subprocess.Popen(r"""cat test.tag | sed 's/_[^\ ]*\ \{0,1\}//g' | ./char_based.py --model _model --threshold=15 --result test.cb""",shell=True)
        sp.wait()
        sp=subprocess.Popen(r"""./make_lattice.py t test.tag test.cb test_%s.lattice"""%(i),shell=True)
        sp.wait()
    sp=subprocess.Popen(r"""cat test_*.lattice > train.lattice""",shell=True)
    sp.wait()

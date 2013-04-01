#!/usr/bin/python3
import argparse
import sys
import json
import time
from collections import Counter
import subprocess

class Evaluator : # 评价
    def __init__(self):
        self.std,self.rst,self.cor_tags=0,0,0
        self.cor_words=0
        self.start_time=time.time()
    def _gen_set(self,words):
        offset=0
        word_set=set()
        tag_set=set()
        for it in words:
            if type(it) is not tuple : 
                it=(it,it)
            tag_set.add((offset,it))
            word_set.add((offset,it[0]))
            offset+=len(it[0])
        return tag_set,word_set
    def __call__(self,std,rst): # 根据答案std和结果rst进行统计
        std_tags,std_words=self._gen_set(std)
        rst_tags,rst_words=self._gen_set(rst)
        self.std+=len(std_tags)
        self.rst+=len(rst_tags)
        self.cor_tags+=len(std_tags&rst_tags)
        self.cor_words+=len(std_words&rst_words)
    def report(self):
        precision=self.cor_tags/self.rst if self.rst else 0
        recall=self.cor_tags/self.std if self.std else 0
        f1_tags=2*precision*recall/(precision+recall) if precision+recall!=0 else 0
        precision=self.cor_words/self.rst if self.rst else 0
        recall=self.cor_words/self.std if self.std else 0
        f1_words=2*precision*recall/(precision+recall) if precision+recall!=0 else 0
        print("历时: %.2f秒 答案: %i 结果: %i 词性标注正确: %i F值: %.4f 分词正确: %i F值: %.4f"
                %(time.time()-self.start_time,self.std,self.rst,
                    self.cor_tags,f1_tags,
                    self.cor_words,f1_words,
                    ))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--iteration',type=int,default=5, help='')
    parser.add_argument('--separator',type=str,default='_', help='')
    parser.add_argument('--train',type=str, help='')
    parser.add_argument('--seg_only',action='store_true')
    parser.add_argument('--model',type=str, help='')
    parser.add_argument('--test',type=str, help='')
    parser.add_argument('--predict',type=str, help='')
    parser.add_argument('--result',type=str, help='')
    parser.add_argument('--threshold',type=int, default=0, help='')
    parser.add_argument('--show_input',action='store_true',default=False)
    args = parser.parse_args()
    
    # 训练
    if args.train : 
        sp=subprocess.Popen(r'bin/train_c --separator %s --iteration %i %s %s %s '%(
            args.separator,
            args.iteration,
            '--seg_only' if args.seg_only else '',
            args.train,args.model,)
                ,shell=True)
        sp.wait()

    # 使用有正确答案的语料测试
    if args.test :
        sp=subprocess.Popen(r'bin/predict_c %s '%(
            args.model,),
                stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                shell=True)
        ev=Evaluator()
        has_tags=None
        for line in open(args.test):
            std=line.split()
            if has_tags is None :
                has_tags=all('_' in it for it in std)
            if has_tags :
                std=[it.rpartition('_') for it in std]
                std=[(w,t) for w,_,t in std]
                line=''.join(w for w,t in std)
            else :
                line=''.join(std)
            sp.stdin.write((line+'\n').encode())
            sp.stdin.flush()
            output=sp.stdout.readline().decode().split()
            if has_tags :
                output=[it.rpartition('_') for it in output]
                output=[(w,t) for w,_,t in output]
            ev(std,output)
        ev.report()
        
    # 对未分词的句子输出分词结果
    if not args.test and not args.train :
        sp=subprocess.Popen(r'bin/predict_c %s %s '%(
            '--threshold %i'%(args.threshold) if args.threshold!=0 else '',
            args.model,),
                stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                shell=True)
        instream=open(args.predict) if args.predict else sys.stdin
        outstream=open(args.result,'w') if args.result else sys.stdout
        has_tags=None
        for input in instream:
            input=input.strip()
            sp.stdin.write((input+'\n').encode())
            sp.stdin.flush()
            output=sp.stdout.readline().decode().strip()
            if args.show_input :
                output=input+' '+output
            print(output,file=outstream)
            outstream.flush()

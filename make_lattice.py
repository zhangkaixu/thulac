#!/usr/bin/python3
import os
import sys
import tagging_eval

def make_oracle(tagged,lattice,oracle,mode="t"):
    file=open(oracle,"w")
    for tagged,lattice in zip(
            open(tagged),
            open(lattice)):
        raw=''.join(x.partition('_')[0] for x in tagged.split())
        gold={tuple(x) for x in (tagging_eval.str_to_list(tagged))}
        gold={(b,b+len(w),t)for b,w,t in gold}

        lattice=[x.split(',') for x in lattice.split()]
        lattice=[[int(x[0]),int(x[1]),x[2],int(x[3])]for x in lattice]
        lattice={tuple(x[:-1]):[x[-1],0] for x in lattice}
        
        if mode=="t":
            for i in lattice:
                if i in gold:
                    gold.remove(i)
                    lattice[i][1]=1
            for i in gold:
                lattice[i]=[-1,1]
        
        lattice=[[v[1],k[0],v[0],k[2],raw[k[0]:k[1]]] for k,v in lattice.items()]
        lattice=sorted(lattice,key=lambda x:x[1])
        lattice=' '.join(','.join(map(str,x)) for x in lattice)
        
        print(lattice,file=file)

if __name__=="__main__":
    if len(sys.argv)!=5:
        print("4 arguments needed")
        exit()
    
    make_oracle(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[1])

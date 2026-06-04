from itertools import product
from copy import deepcopy
m,n,p=map(int,input().split())
def comb_line(board,reverse=False,verdical=False):
    result=[]
    for line in zip(*board) if verdical else board:
        if reverse:
            line=line[::-1]
        n=len(line)
        line=[l for l in line if l!=0]
        i=0
        k=len(line)
        while i<k-1:
            if line[i]==0:
                i+=1
                continue
            elif line[i]==line[i+1]:
                line[i+1]=line[i]*2
                line[i]=0
            i+=1
        new=[l for l in line if l!=0]
        new_line=[0]*(n-len(new))+new
        result.append(new_line[::-1] if reverse else new_line)
    return result if not verdical else list(zip(*result))
def max_score(board):
    ans=0
    for i in board:
        for j in i:
            ans=max(ans,j)
    return ans
def steps_max_score(board,steps):
    max_scor=0
    if steps==0:
        return max_score(board)
    else:
        for i in product(range(4),repeat=steps):
            bor=deepcopy(board)
            for j in i:
                if j==0:
                    bor=comb_line(bor)
                elif j==1:
                    bor=comb_line(bor,reverse=True)
                elif j==2:
                    bor=comb_line(bor,verdical=True)
                else:
                    bor=comb_line(bor,verdical=True,reverse=True)
            cur_score=max_score(bor)
            max_scor=max(max_scor,cur_score)
    return max_scor
board=[list(map(int,input().split())) for _ in range(m)]
print(steps_max_score(board,p))

    
                
        

    


            
         
                                                    
        




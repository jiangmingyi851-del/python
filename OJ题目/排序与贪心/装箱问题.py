import sys
orders=[]
while True:
    line=sys.stdin.readline().strip().split()
    if len(line)!=6:
        continue
    line=list(map(int,line))
    if not line:
        continue
    if line == [0,0,0,0,0,0]:
        break
    orders.append(line)

def min_boxes(order):
    num=0
    if order[5]>0:
        num+=order[5]
        order[5]=0
    if order[4]>0:
        num+=order[4]
        order[0]-=order[4]*11
        if order[0]<0:
            order[0]=0
        order[4]=0
    if order[3]>0:
        num+=order[3]
        if order[1]<order[3]*5:
            if order[0]>0:
                order[0]-=(order[3]*5-order[1])*4
                if order[0]<0:
                    order[0]=0
                order[1]=0
            else:
                order[1]-=order[3]*5
                if order[1]<0:
                    order[1]=0
        order[3]=0
    if order[2]>0:
        num+=order[2]//4
        if order[2]%4>0:
            num+=1
            if order[2]%4==1:
                if order[1]>5:
                    order[1]-=5
                    order[0]-=7
                else:
                    order[0]-=(27-order[1]*4)
                    order[1]=0
                if order[0]<0:
                    order[0]=0
            elif order[2]%4==2:
                if order[1]>3:
                    order[1]-=3
                    order[0]-=6
                else:
                    order[0]-=(18-order[1]*4)
                    order[1]=0
                if order[0]<0:
                    order[0]=0
            elif order[2]%4==3:
                if order[1]>1:
                    order[1]-=1
                    order[0]-=5
                else:
                    order[0]-=(9-order[1]*4)
                    order[1]=0
                if order[0]<0:
                    order[0]=0
        order[2]=0
    if order[1]>0:
        num+=order[1]//9
        if order[1]%9>0:
            num+=1
            order[0]-=(36-order[1]%9*4)
            if order[0]<0:
                order[0]=0
        order[1]=0
    if order[0]>0:
        num+=order[0]//36
        if order[0]%36>0:
            num+=1
        order[0]=0
    return num
for order in orders:
    print(min_boxes(order))
    print("\n")
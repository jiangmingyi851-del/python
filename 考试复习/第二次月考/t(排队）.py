import bisect
n,d=map(int,input().split())
li=[]
for i in range(n):
    li.append(int(input()))
heights=sorted(list(set(li)))
dic={}
l = len(heights)
#尝试用线段树来写
tree_max = [-1] * (4*l)   # 线段树的最大值数组
def update(index,val):
    node=index+l
    tree_max[node]=val
    while node>1:
        node//=2
        tree_max[node]=max(tree_max[node*2],tree_max[node*2+1])
def query(start,end):
    start_node=bisect.bisect_left(heights,start,1,l)
    end_node=bisect.bisect_right(heights,end,1,l)
    start_node+=l
    end_node+=l
    max_val=float('-inf')
    while start_node<end_node:
        if start_node%2==1:
            max_val=max(max_val,tree_max[start_node])
            start_node+=1
        if end_node%2==1:
            end_node-=1
            max_val=max(max_val,tree_max[end_node])
        start_node//=2
        end_node//=2
    return max_val
for i in li:
    node=dic[i]
    stoery=1+max(query(0,i-d),query(i+d,heights[-1]))
    update(node,stoery)
for i in range(d):
    op,x,y=map(int,input().split())
    if op==1:
        update(dic[x],y)
    else:
        print(query(x,y))




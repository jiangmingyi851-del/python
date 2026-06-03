import sys
def can_sticks(current,sticks,length,done,target_count,visited,start):
    if done==target_count:
        return True
    if length==total:
        return True
    pre=-1
    for j,i in enumerate(sticks[start:]):
        if visited[j+start] or i>current or i==pre:
            continue
        visited[j+start]=True
        if current-i==0:
            if can_sticks(length,sticks,length,done+1,target_count,visited,0):
                return True
        elif current-i>0:
            if can_sticks(current-i,sticks,length,done,target_count,visited,j+start+1):
                return True
        visited[j+start]=False
        pre=i
        if current==length:
            return False
    return False   
while True:
    n=int(sys.stdin.readline().strip())
    if n==0:
        break
    sticks=list(map(int,sys.stdin.readline().strip().split()))
    visited=[False]*n
    total=sum(sticks)
    sticks.sort(reverse=True)
    j=max(sticks)
    while j<=total:
        if total%j==0:
            visited=[False]*n
            if can_sticks(j,sticks,j,0,total//j,visited,0):
                print(j)
                break
        j+=1
    


            
            


            





    

def remove_parentheses(line):
    length=len(line)
    slow=0
    stack=[]
    pre=0
    delete=[False]*len(line)
    dic={}
    for slow in range(length):
        if line[slow]=='(':
            stack.append(slow)
        elif line[slow]==')':
            if not stack:
                return None
            start=stack.pop()
            end=slow
            dic[start]=end
            can1=1
            s1=start
            t1=end
            if end-start==1 :
                delete[start]=True
                delete[end]=True
                continue
            while s1<t1:
                if line[s1+1]=='(' and line[t1-1]==')' and dic[s1+1]==t1-1:
                    s1+=1
                    t1-=1
                else:
                    break

            if (start>0 and line[start-1]=='*') or (end<length-1 and line[end+1]=='*'):
                    s=s1+1
                    while s<t1:
                        if line[s]=='+':
                            can1=0
                            break
                        elif line[s]=='*':
                            if start>0 and line[start-1]=='*':
                                can1=0
                                break
                        elif line[s]=='(':
                            s=dic[s]
                        s+=1
            elif (start>0 and line[start-1]=='+'):
                s=s1+1
                while s<t1:
                        if line[s]=='+':
                            can1=0
                            break
                        elif line[s]=='(':
                            s=dic[s]
                        s+=1
            if can1!=0:
                delete[start]=True
                delete[end]=True
                continue
    result=[]
    for i in range(length):
        if not delete[i]:
            result.append(line[i])
    return ''.join(result)
            

import sys
n=sys.stdin.readlines()
for line in n:
    line=line.strip()
    print(remove_parentheses(line))
    
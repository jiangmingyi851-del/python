import sys
tar=input()
k=len(tar)
dic={tar[i]:i for i in range(len(tar))}
while True:
    try:
        s=input()
        if len(s)!=k:
            state='NO'
            print(f'{state}')
            continue
        state='YES'
        stack=[]
        start=[]
        for c in s[::-1]:
            if c not in dic:
                state='NO'
                break
            while  stack and dic[c]<dic[stack[-1]]:
                start.append(stack.pop())
                if dic[start[-1]]!=k-len(start):
                    state='NO'
                    break
            stack.append(c)
        while stack:
            start.append(stack.pop())
        print(f'{state}')
    except EOFError:
        break
        




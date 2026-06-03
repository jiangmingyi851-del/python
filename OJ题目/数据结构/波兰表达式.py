def poland_notation(e):
    opraters={
        '+': lambda x,y: x+y
        ,'-': lambda x,y: x-y
        ,'*': lambda x,y: x*y   
        ,'/': lambda x,y: x/y
    }
    stack=[]
    e=reversed(e)
    for i in e:
        if i in opraters:
            y=stack.pop()
            x=stack.pop()
            stack.append(opraters[i](y,x))
        else:
            stack.append(float(i))
    return stack[0]
e=input().split()
v=poland_notation(e)
print(f"{v:.6f}")



import sys
l=sys.stdin.readlines()
can=[]
wait=[]
for i in l:
    name,age,weight,inheat,nofood,stray,immuned=i.split()
    if float(age)>=6 and float(weight)>=2.5 and inheat=='no' and float(nofood)>=4 and(stray=='yes' or immuned=='yes'):
        can.append(name)
    elif float(age)>=6 and float(weight)>=2.5 and inheat=='no' and float(nofood)<4 and(stray=='yes' or immuned=='yes'):
        t=4-float(nofood)
        t1=f"{t:.2f}"
        wait.append((t1,name))
can.sort()
wait.sort()
print(len(can))
print(' '.join(can))
print(len(wait))
print('\n'.join([f"{i[1]} {i[0]}" for i in wait])) 
matrix1=[]
matrix2=[]
matrix3=[]
n,m=map(int,input().split())
for i in range(n):
    a=list(map(int,input().strip().split()))
    matrix1.append(a)
n,m=map(int,input().split())
for i in range(n):
    a=list(map(int,input().strip().split()))
    matrix2.append(a)
n,m=map(int,input().split())
for i in range(n):
    a=list(map(int,input().strip().split()))
    matrix3.append(a)
if len(matrix1[0])!=len(matrix2):
    print('Error!')
elif len(matrix2[0])!=len(matrix3[0]) or len(matrix1)!=len(matrix3):
    print('Error!')
else:
    ans=[[0]*len(matrix3[0]) for i in range(len(matrix3))]
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                ans[i][j]+=matrix1[i][k]*matrix2[k][j]
    for i in range(len(ans)):
        for j in range(len(ans[0])):
            ans[i][j]+=matrix3[i][j]
    for row in ans:
        print(' '.join(map(str,row)))
        

        


    
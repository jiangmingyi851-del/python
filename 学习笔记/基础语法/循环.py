# use while to write
i=1
while i<=10:
    print('no')
    i*=2



# calculate from one to one hundred
a=0
sum=0
# while a<100:
#     a+=1
#     sum=sum+a
# else:
#     print(f'sum={sum}')
while a<=100:
    a+=1
    if a==56:
        continue
    if a%2==0:
        sum+=a
else:
    print(f'sum={sum}')
# 可以if  break终止循环 if continue中断本次循环，开启下次循环

# 使用while打印杨辉三角前6行？
b=0
j=6
while b<=5:
    b+=1
    j-=1
    print(j,b,j)
    print(b+j+b)

# while True 无限循环





#for遍历
#[0,1,2,3,4,5,6,7,8,9]
for i in range(10):
    print(i)

string='ABCDEFG'
for i in string:
    print(i)

for i in range(12):
    print('hello')

for i in range(1,6):
    print(i)
    print('hello')

for s in 'ASDFF':
    if s=='D':
        continue #跳过此次 继续循环
    print(s)
for i in range(0,10):
    print('i=%d'%(i))


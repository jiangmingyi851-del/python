# 执行到input 输入后才会向下执行
input("请输入:")
name=input("123:")
print(name)  #  输入后打印所输入的内容

x=int(input('请输入一个整数')) 
print(x) 
x=eval(input('shuzi'))
print(x)
#处理无线输入
while True:
    try:
        line = input()# 处理每一行的逻辑
    except EOFError:
        break
#这种方法适用于手动输入时使用 Ctrl+D(Unix/Linux)或 Ctrl+Z+Enter(Windows)结束输入的场景[来源 1][来源4][来源 11]。
#利用 sys.stdin 逐行读取

import sys
for line in sys.stdin:# 处理每一行的逻辑(包含换行符)
    line = line.strip() # 通常需要去除首尾空白
#通过 sys.stdin.read()一次性读取所有输入
import sys
sys.stdin.read()
 #整个输入作为字符串data =lines = data.splitlines() # 按行分割for line in lines# 处理每一行的逻辑
#这种方法特别适合处理大规模输入，效率较高[来源 2][来源 8]。
#列表存储法
lines =[]
while True:
    try:
        lines.append(input())
    except EOFError:
        break
#后续处理lines列表
这种方法将所有输入存储在列表中便于后续处理[来源 4]。
n=input().strip() #读取一行输入 去除换行符
a=list(map(int,n.split())) #将字符串按空格分割 转换为整数列表
import sys
b=sys.argv #获取命令行参数 列表形式
c=sys.stdin.readline().strip() #读取一行输入 去除首尾空白符
d=sys.stdin.readlines() #读取所有输入 返回列表 每行一个元素
e=sys.stdin.read.strip() #读取所有输入 去除首尾空白符
for line in sys.stdin:
    print(line.strip()) #逐行读取输入 去除换行符

# a=float(input('请输入第一个数'))
# b=str(input('请输入算符'))
# c=float(input('请输入第二个数'))

# def func():
#     if b=='+':
#         print(a+c)
#     elif b=='-':
#         print(a-c)
#     elif b=='*' :
#         print(a*c)
#     elif b=='/' and c!=0:
#         print(a/c)
#     else:
#         raise Exception('输入错误')
    
# try:
#     func()
# except Exception as e:
#     print(e)






#标准答案：
# 命令行计算器
def calculator():
    print("欢迎使用命令行计算器")
    print("支持的运算符：+（加）、-（减）、*（乘）、/（除）")
    
    while True:
        # 获取用户输入
        num1 = input("请输入第一个数字：")
        operator = input("请输入运算符（+、-、*、/）：")
        num2 = input("请输入第二个数字：")
        
        # 将输入的字符串转换为浮点数
        try:
            num1 = float(num1)
            num2 = float(num2)
        except ValueError:
            print("输入的数字无效，请重新输入！")
            continue
        
        # 根据运算符进行计算
        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                print("除数不能为0，请重新输入！")
                continue
            result = num1 / num2
        else:
            print("输入的运算符无效，请重新输入！")
            continue
        
        # 输出结果
        print(f"计算结果：{num1} {operator} {num2} = {result}")
        
        # 询问用户是否继续
        again = input("是否继续计算？(y/n)：")
        if again.lower() != "y":
            break

    print("感谢使用计算器，再见！")

# 调用计算器函数
calculator()

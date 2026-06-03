n=int(input())
def infix_to_postfix(infix):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack = []
    postfix = ""
    k = len(infix)
    i = 0
    while i < k:
        # 跳过空格
        if infix[i] == ' ':
            i += 1
            continue

        # 操作数（字母、数字、小数点）
        if infix[i].isalnum():
            num = ''
            while i < k:
                if infix[i].isalnum() or infix[i] == '.':
                    num += infix[i]
                    i += 1
                else:
                    break          # 遇到运算符或括号，停止读取操作数
            postfix += num + ' '

        # 运算符
        elif infix[i] in '+-*/':
            while stack and stack[-1] != '(' and precedence[infix[i]] <= precedence[stack[-1]]:
                postfix += stack.pop() + ' '
            stack.append(infix[i])
            i += 1

        # 左括号
        elif infix[i] == '(':
            stack.append(infix[i])
            i += 1

        # 右括号
        elif infix[i] == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop() + ' '
            stack.pop()   # 弹出 '('
            i += 1

        # 其他字符（如制表符），跳过
        else:
            i += 1

    # 弹出栈中剩余运算符
    while stack:
        postfix += stack.pop() + ' '

    return postfix
for i in range(n):
    infix=input()
    postfix=infix_to_postfix(infix)
    print(postfix)

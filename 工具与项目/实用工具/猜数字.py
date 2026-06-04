import random
def guess():
    score=0
    print('现在是休息时间，我们来玩猜数字吧')
    print('你需要猜一个一到一百的数，每次猜完我会告诉你猜到了还是大了、小了，加油💪')
    num=random.randint(1,100)
    attempts=0
    while True:
        num2=input('请输入你的猜测')
        try:
            num2=int(num2)
            1<=num2<=100
        except Exception:
            print('输入数字好像不在1-100内呢，重新输一下吧')
            continue
        attempts+=1
        if num2<num:
            print('输入的太小了，请重输')            
            continue
        if num2>num:
            print('输入的太大了，请重输')
            continue
        if num2==num:
            print('猜对了，你真棒')
            score+=1
            print(f'当前得分：{score}')
            print(f'尝试次数：{attempts}')
        again=input('还要继续吗?（y/n):')
        if again.lower!='y':
            print('欢迎下次来玩')
            break
        else:
            continue
guess()


    
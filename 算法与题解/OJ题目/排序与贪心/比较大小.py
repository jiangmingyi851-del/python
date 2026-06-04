from functools import cmp_to_key

def compare_to_key(s1,s2):
    if s1 + s2 > s2 + s1:
        return 1
    elif s1 + s2 < s2 + s1:
        return -1
    else:
        return 0

m=int(input())
n=int(input())
li=list(map(str,input().split()))
li.sort(key=cmp_to_key(compare_to_key))
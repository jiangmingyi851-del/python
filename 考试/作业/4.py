li=input().split(',')
word=0
for i in li:
    lii=i.split()
    n=len(lii)
    word=max(word,n)
print(word)
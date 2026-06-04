s=input()
sum=0
for j in s:
    sum=sum*26+ord(j)-ord('A')+1
print(sum)
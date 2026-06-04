document='acgscgscg'
# do not do this this spend so much time O(n**2)
letters=''
for c in document:
    if c.isalpha():
        letters+=c
print(letters)
# because the length of string is const,every time we plus it,we should realloc it memory.
# do this
temp=[]
for c in document:
    if c.isalpha():
        temp.append(c)
letters=''.join(temp)
print(letters)
# O(n)
letters=''.join(c for c in document if c.isalpha()) 
print(letters)


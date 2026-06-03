# if True： 
#     print()
#     print()
# print()


# True和False的界定
# 1.have sth. is True
# 2.noyhing,0 are False
# 3.if returns T or F 

age=int(input('age:'))
if age>=18:
    print('Yes')
else:
    print('No')
    
# "!="means inequality
a=5 
b=10
print(a==b) #now they are inequality,so system will print "False"
point=float(input("point:"))
if point<80:
    print("oh ni")
elif point>=80 and point<90:
    print("just so so")
elif point>=90 and point<=100:
    print('well down')
k=int(input('\'cm\'knife_length=:'))
knief_length='20cm'
ticket=int(input('Yes:1;No:2 :'))
if ticket==1:
    print('ok')
    if k<=20:
        print('welcome')
    else:
        print(f"check out your knief length,knief should be within{knief_length}" )
elif ticket==2:
    print("I'm sorry,you can't enter")
else: 
    print('errow')
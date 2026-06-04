class Solution:
    def reverseBits(self, n: int):
        res=''
        while n>0:
            res+=str(n%2)
            n//=2
        if len(res)<32:
            res+='0'*(32-len(res))
        return int(res,2)
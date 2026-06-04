class Solution:
    def sortByBits(self, arr):
        def count_bits(n):
            binary = bin(n)[2:]
            return binary.count('1')
        return sorted(arr, key=lambda x: (count_bits(x), x))

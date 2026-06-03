import sys
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
def create_linked_list(values):
    if not values:
        return None
    head = Node(values[0])  # 创建头节点
    current = head
    for val in values[1:]:
        current.next = Node(val)  # 创建新节点并连接
        current = current.next
    return head
def is_palindrome(head: Node) -> bool:
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    prev, curr = None, slow
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    left, right = head, prev
    while right:
        if left.data != right.data:
            return False
        left = left.next
        right = right.next
    return True
for i in sys.stdin.readlines():
    values = list(map(int, i.strip().split()))
    head = create_linked_list(values)
    if is_palindrome(head):
        print("True")
    else:
        print("False")
    
    
    
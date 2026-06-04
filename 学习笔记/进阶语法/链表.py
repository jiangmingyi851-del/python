# 1. 链表的基本结构
# 链表由一系列节点组成，每个节点包含以下部分：
# val：存储节点的值，可以是任意类型（如整数、字符串等）。
# next：一个指针，指向下一个节点。如果当前节点是链表的最后一个节点，则 next 为 None。

# 在 Python 中，链表节点通常通过一个类来定义：
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val      # 节点的值
        self.next = next    # 指向下一个节点的指针

# 2. 创建链表
# 链表可以通过手动连接节点来创建。以下是一个简单的例子：
# 创建链表：1 -> 2 -> 3
# 将列表中的值转换为链表
def create_linked_list(values):
    if not values:
        return None
    head = ListNode(values[0])  # 创建头节点
    current = head
    for val in values[1:]:
        current.next = ListNode(val)  # 创建新节点并连接
        current = current.next
    return head
node1 = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(3)

node1.next = node2  # 将 node2 连接到 node1
node2.next = node3  # 将 node3 连接到 node2
# 3. 遍历链表
# 链表的遍历需要通过指针逐个访问每个节点。通常使用一个临时指针（如 current）来遍历链表：
def print_list(head: ListNode):
    current = head  # 初始化指针为头节点
    while current:  # 当前节点不为 None
        print(current.val, end=" -> ")
        current = current.next  # 移动指针到下一个节点
    print("None")  # 表示链表结束
head = node1  # 链表的头节点
print_list(head)  # 输出：1 -> 2 -> 3 -> None
# 4. 插入操作
#在链表中插入节点通常涉及修改指针的指向。以下是常见的插入操作：
#1.在链表头部插入节点
def insert_at_head(head: ListNode, val):
    new_node = ListNode(val)  # 创建新节点
    new_node.next = head  # 新节点的 next 指向原头节点
    return new_node  # 返回新的头节点
head = node1  # 原链表：1 -> 2 -> 3
head = insert_at_head(head, 0)  # 插入 0 到头部
print_list(head)  # 输出：0 -> 1 -> 2 -> 3 -> None
# 4.2 在链表尾部插入节点
def insert_at_tail(head: ListNode, val):
    new_node = ListNode(val)  # 创建新节点
    if not head:  # 如果链表为空
        return new_node  # 新节点成为头节点
    current = head
    while current.next:  # 遍历到链表的最后一个节点 # 此时若为 while current,则遍历到none
        current = current.next
    current.next = new_node  # 将新节点连接到链表末尾
    return head

head = node1  # 原链表：1 -> 2 -> 3
head = insert_at_tail(head, 4)  # 插入 4 到尾部
print_list(head)  # 输出：1 -> 2 -> 3 -> 4 -> None
# 4.3 在链表中间插入节点
def insert_after(head: ListNode, target_val, val):
    current = head
    while current:  # 遍历链表
        if current.val == target_val:  # 找到目标节点
            new_node = ListNode(val)
            new_node.next = current.next  # 新节点的 next 指向目标节点的下一个节点
            current.next = new_node  # 目标节点的 next 指向新节点
            return head
        current = current.next
    return head
head = node1  # 原链表：1 -> 2 -> 3
head = insert_after(head, 2, 9)  # 在值为 2 的节点后插入 9
print_list(head)  # 输出：1 -> 2 -> 9 -> 3 -> None
# 5. 删除操作
# 删除链表中的节点也需要修改指针的指向。
# 5.1 删除链表头部节点
def delete_head(head: ListNode):
    if not head:  # 如果链表为空
        return None
    new_head = head.next  # 新头节点为原头节点的下一个节点
    return new_head
head = node1  # 原链表：1 -> 2 -> 3
head = delete_head(head)  # 删除头部节点
print_list(head)  # 输出：2 -> 3 -> None

# 5.2 删除链表尾部节点
def delete_tail(head:ListNode):
    if not head:
        return None
    current=head
    while  current.next.next:
        current=current.next
    current.next=current.next.next
    return head
head=node1
head=delete_tail(head)
print_list(head)

# 5.3 删除链表指定节点
def delete_node(head: ListNode, target_val):
    if not head:  # 如果链表为空
        return None
    if head.val == target_val:  # 如果目标节点是头节点
        return delete_head(head)
    current = head
    while current.next:  # 遍历链表
        if current.next.val == target_val:  # 找到目标节点
            current.next = current.next.next  # 跳过目标节点
        return head
        current = current.next
    return head
head = node1  # 原链表：1 -> 2 -> 3
head = delete_node(head, 4)  # 删除值为 2 的节点
print_list(head)  # 输出：1 -> 3 -> None

# 6. 查找操作
# 在链表中查找某个值是否存在，需要遍历链表并逐个比较节点的值。
def find_node(head: ListNode, target_val):
    current = head
    while current:  # 遍历链表
        if current.val == target_val:  # 找到目标值
            return True
        current = current.next
    return False 
      # 未找到目标值
head = node1  # 原链表：1 -> 2 -> 3
print(find_node(head, 2))  # 输出：True
print(find_node(head, 4))  # 输出：False

# 7. 链表的反转
# 反转链表是一个常见的操作，可以通过迭代或递归实现。
# 7.1 迭代反转链表
def reverse_list(head: ListNode):
    prev = None  # 初始化前一个节点为 None
    current = head  # 当前节点为头节点
    while current:  # 遍历链表
        next_node = current.next  # 保存下一个节点
        current.next = prev  # 当前节点的 next 指向前一个节点
        prev = current  # 更新前一个节点
        current = next_node  # 移动到下一个节点
    return prev  # 返回新的头节点
head = node1  # 原链表：1 -> 2 -> 3
head = reverse_list(head)  # 反转链表
print_list(head)  # 输出：3 -> 2 -> 1 -> None
# 7.2 递归反转链表
def reverse_list_recursive(head: ListNode):
    if not head or not head.next:  # 如果链表为空或只有一个节点
        return head
    new_head = reverse_list_recursive(head.next)  # 递归反转剩余部分
    head.next.next = head  # 将当前节点的下一个节点的 next 指向当前节点
    head.next = None  # 当前节点的 next 指向 None
    return new_head  # 返回新的头节点
head=node3
head=reverse_list_recursive(head)
print_list(head)
# 8. 链表的高级操作
# 8.1 合并两个有序链表
# 将两个有序链表合并为一个新的有序链表。这是一个常见的面试问题，可以通过迭代或递归实现。
def merge_two_lists(l1: ListNode, l2: ListNode) -> ListNode:
    dummy = ListNode(0)  # 创建一个哑节点作为新链表的头节点
    current = dummy  # 当前节点指针

    while l1 and l2:  # 遍历两个链表
        if l1.val < l2.val:
            current.next = l1  # 将较小的节点连接到新链表
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next  # 移动当前节点指针

    # 如果其中一个链表还有剩余节点，直接连接到新链表
    current.next = l1 if l1 else l2
    return dummy.next  # 返回哑节点的下一个节点作为新链表的头节点

#递归方法
def merge_two_lists_recursive(l1: ListNode, l2: ListNode) -> ListNode:
    if not l1:
        return l2
    if not l2:
        return l1
    if l1.val < l2.val:
        l1.next = merge_two_lists_recursive(l1.next, l2)
        return l1
    else:
        l2.next = merge_two_lists_recursive(l1, l2.next)
        return l2
# 8.3 找到链表的中间节点
# 使用快慢指针法，快指针每次移动两步，慢指针每次移动一步。当快指针到达链表末尾时，慢指针正好在链表的中间。
def find_middle_node(head: ListNode) -> ListNode:
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow  # 慢指针指向链表的中间节点
#  8.4 删除链表的倒数第 N 个节点
# 可以通过双指针法解决。让一个指针先移动 N 步，然后两个指针同时移动，直到第一个指针到达链表末尾。
def remove_nth_from_end(head: ListNode, n: int) -> ListNode:
    dummy = ListNode(0)  # 创建哑节点
    dummy.next = head
    first = dummy
    second = dummy

    # 让第一个指针先移动 n + 1 步
    for _ in range(n + 1):
        first = first.next

    # 同时移动两个指针，直到第一个指针到达末尾
    while first:
        first = first.next
        second = second.next

    # 删除倒数第 N 个节点
    second.next = second.next.next
    return dummy.next 
# 9. 链表的优缺点
# 优点
# 动态大小：链表的大小可以动态变化，不需要预先分配固定大小的内存。
# 高效的插入和删除：在链表中插入或删除节点只需要修改指针，时间复杂度为 O(1)。
# 节省内存：链表不需要连续的内存空间，适合内存碎片化的情况。
# 缺点
# 访问效率低：链表不支持随机访问，访问第 k 个节点需要 O(k) 的时间。
# 额外的内存开销：每个节点需要额外存储指针，增加了内存消耗。
# 复杂的指针操作：链表的操作需要手动管理指针，容易出错。  


# 10. 链表的变种
# 除了普通单链表，还有一些变种：
# 双向链表：每个节点包含两个指针，分别指向前一个节点和后一个节点。
# 循环链表：链表的最后一个节点的 next 指向头节点，形成一个环。
# 跳表：一种基于链表的多级索引数据结构，用于快速查找。

class Node:
    def __init__(self, key=-1, value=-1):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        self.cache = {}
        # 哨兵节点，简化边界操作
        self.head = Node()   # head.next 指向最近使用的节点
        self.tail = Node()   # tail.prev 指向最久未使用的节点
        self.head.next = self.tail
        self.tail.prev = self.head
        self.capacity = capacity

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self):
        node = self.tail.prev
        self._remove_node(node)
        return node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # 更新值，并移动到头部
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # 创建新节点，添加到头部
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)
            # 若超出容量，删除尾部节点
            if len(self.cache) > self.capacity:
                tail_node = self._pop_tail()
                del self.cache[tail_node.key]
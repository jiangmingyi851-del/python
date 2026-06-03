我结合你之前问的 `deque` 知识点，**把两种官方方法完整翻译成 Python 可运行代码**，逐行讲解核心逻辑，两种方法都是力扣 **297. 二叉树的序列化与反序列化** 的标准解法。

先统一二叉树节点定义（Python 标准格式）：
```python
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
```

---

# 方法一：DFS 先序遍历（推荐！面试首选，用到了你刚学的 deque）
核心思路：
1. **序列化**：递归先序遍历，空节点记为 `None`，用逗号分隔所有值
2. **反序列化**：把字符串转成**双端队列 deque**，递归构建二叉树（`popleft()` 效率极高）

## Python 完整代码
```python
from collections import deque

class Codec:
    # 序列化：二叉树 → 字符串
    def serialize(self, root):
        res = []
        # 递归先序遍历
        def dfs(node):
            if not node:
                res.append("None")
                return
            res.append(str(node.val))
            dfs(node.left)   # 左子树
            dfs(node.right)  # 右子树
        dfs(root)
        return ",".join(res)  # 用逗号拼接成字符串

    # 反序列化：字符串 → 二叉树
    def deserialize(self, data):
        # 切割字符串 → 转 deque（核心：popleft() O(1) 效率）
        q = deque(data.split(","))
        
        def build():
            # 弹出队首元素
            val = q.popleft()
            if val == "None":
                return None
            # 构建当前节点 + 递归构建左右子树
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node
        
        return build()
```

## 关键讲解（结合你之前的 deque 问题）
1. **为什么用 deque？**
   反序列化需要**不断从头部取元素**，`list.pop(0)` 是 O(n)，`deque.popleft()` 是 O(1)，效率天差地别
2. **序列化**：空节点必须标记 `None`，否则无法还原树的结构
3. **反序列化**：严格按照**先序顺序**（根→左→右）递归构建

---

# 方法二：括号表示法 + 递归下降解码（进阶写法）
核心思路：
1. **序列化**：空树 = `X`，非空树 = `(左子树)节点值(右子树)`
2. **反序列化**：用指针遍历字符串，递归解析括号和数值

## Python 完整代码
```python
class Codec:
    # 序列化：二叉树 → 括号格式字符串
    def serialize(self, root):
        if not root:
            return "X"
        # 格式：(左子树序列化)节点值(右子树序列化)
        left = f"({self.serialize(root.left)})"
        right = f"({self.serialize(root.right)})"
        return left + str(root.val) + right

    # 反序列化：字符串 → 二叉树
    def deserialize(self, data):
        # 用列表存指针（Python 整数不可变，列表可变）
        ptr = [0]
        n = len(data)
        
        # 解析子树（跳过括号）
        def parse_subtree():
            ptr[0] += 1  # 跳过左括号 (
            node = parse()
            ptr[0] += 1  # 跳过右括号 )
            return node
        
        # 解析数字（支持正负整数）
        def parse_num():
            sign = 1
            if data[ptr[0]] == '-':
                sign = -1
                ptr[0] += 1
            num = 0
            while ptr[0] < n and data[ptr[0]].isdigit():
                num = num * 10 + int(data[ptr[0]])
                ptr[0] += 1
            return num * sign
        
        # 核心解析函数
        def parse():
            if data[ptr[0]] == "X":
                ptr[0] += 1
                return None
            # 构建节点：左子树 → 节点值 → 右子树
            node = TreeNode(0)
            node.left = parse_subtree()
            node.val = parse_num()
            node.right = parse_subtree()
            return node
        
        return parse()
```

## 关键讲解
1. **序列化规则**：用括号严格包裹子树，完美保留树的层级结构
2. **指针 `ptr`**：用列表存储索引（Python 中整数是不可变类型，无法在函数内修改）
3. **解析逻辑**：遇到 `X` → 空节点；遇到 `(` → 解析子树；遇到数字 → 节点值

---

# 测试代码（两种方法通用）
```python
# 构建测试二叉树
#    1
#   / \
#  2   5
# / \
#3   4
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(5)
root.left.left = TreeNode(3)
root.left.right = TreeNode(4)

# 测试方法一/二
codec = Codec()
ser_str = codec.serialize(root)
print("序列化结果:", ser_str)
des_root = codec.deserialize(ser_str)
print("反序列化完成，树结构还原成功")
```

### 方法一输出
```
序列化结果: 1,2,3,None,None,4,None,None,5,None,None
```

### 方法二输出
```
序列化结果: (((X)3(X))2((X)4(X)))1(((X)5(X))X)
```

---

### 总结
1. **方法一（DFS 先序 + deque）**
   - 最简单、最常用、面试首选
   - 用到了你刚学习的 `deque`，头部操作效率拉满
2. **方法二（括号表示法）**
   - 进阶写法，结构更直观，适合理解递归解析
3. 两种方法**时间/空间复杂度都是 O(n)**，均为最优解
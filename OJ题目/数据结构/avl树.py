# n=int(input())
# class Node:
#     def __init__(self,val):
#         self.val=val
#         self.left=None
#         self.right=None
#         self.height=1
# def get_height(node):
#     if not node:
#         return 0
#     return node.height
# def update_height(node):
#     node.height=1+max(get_height(node.left),get_height(node.right))
# def rotate_left(node):
#     new_root=node.right
#     node.right=new_root.left
#     new_root.left=node
#     update_height(node)
#     update_height(new_root)
#     return new_root
# def rotate_right(node):
#     new_root=node.left
#     node.left=new_root.right
#     new_root.right=node
#     update_height(node)
#     update_height(new_root)
#     return new_root
# def insert(root,val):
#     if not root:
#         return Node(val)
#     if val<root.val:
#         root.left=insert(root.left,val)
#     else:
#         root.right=insert(root.right,val)
#     update_height(root)
#     balance=get_height(root.left)-get_height(root.right)
#     if balance>1:
#         if val<root.left.val:
#             return rotate_right(root)
#         else:
#             root.left=rotate_left(root.left)
#             return rotate_right(root)
#     if balance<-1:
#         if val>root.right.val:
#             return rotate_left(root)
#         else:
#             root.right=rotate_right(root.right)
#             return rotate_left(root)
#     return root
class Node:
    def __init__(self, data):
        self.data = data
        self.height = 1
        self.left = None
        self.right = None

def get_height(root):
    if root is None:
        return 0
    return root.height

def update_height(root):
    root.height = max(get_height(root.left), get_height(root.right)) + 1

def get_balance_factor(root):
    return get_height(root.left) - get_height(root.right)

def rotate_left(root):
    temp = root.right
    root.right = temp.left
    temp.left = root
    update_height(root)
    update_height(temp)
    return temp

def rotate_right(root):
    temp = root.left
    root.left = temp.right
    temp.right = root
    update_height(root)
    update_height(temp)
    return temp

def insert(root, data):
    if root is None:
        return Node(data)
    if data < root.data:
        root.left = insert(root.left, data)
        update_height(root)
        if get_balance_factor(root) == 2:
            if get_balance_factor(root.left) == 1:
                root = rotate_right(root)
            elif get_balance_factor(root.left) == -1:
                root.left = rotate_left(root.left)
                root = rotate_right(root)
    else:
        root.right = insert(root.right, data)
        update_height(root)
        if get_balance_factor(root) == -2:
            if get_balance_factor(root.right) == -1:
                root = rotate_left(root)
            elif get_balance_factor(root.right) == 1:
                root.right = rotate_right(root.right)
                root = rotate_left(root)
    return root

pre_order_list = []

def pre_order(root):
    if root is None:
        return
    pre_order_list.append(root.data)
    pre_order(root.left)
    pre_order(root.right)

def main():
    n = int(input())
    root = None
    for _ in range(n):
        data = int(input())
        root = insert(root, data)
    pre_order(root)
    print(" ".join(str(x) for x in pre_order_list))

if __name__ == "__main__":
    main()


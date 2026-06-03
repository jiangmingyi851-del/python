
import sys

def build(levels):
    """levels: list of strings, 从第1轮删除的叶子到最后一轮（根）"""
    if not levels:
        return ''
    # 最后一行的第一个字符（且唯一）是根
    root = levels[-1][0]
    # 划分左子树和右子树的字母集合
    left_vals = []
    right_vals = []
    for s in levels[:-1]:   # 除最后一行（根）外的所有轮次
        left_part = []
        right_part = []
        for ch in s:
            if ch < root:
                left_part.append(ch)
            elif ch > root:
                right_part.append(ch)
            # 不会等于，因为根节点只出现在最后一行
        if left_part:
            left_vals.append(''.join(left_part))
        if right_part:
            right_vals.append(''.join(right_part))
    # 递归构建左右子树
    left_pre = build(left_vals)   # left_vals 已是正确格式的 levels
    right_pre = build(right_vals)
    return root + left_pre + right_pre

def main():
    data = sys.stdin.read().strip().split()
    out_lines = []
    i = 0
    while i < len(data):
        levels = []
        while i < len(data) and data[i] not in ('*', '$'):
            levels.append(data[i])
            i += 1
        if not levels:   # 空行跳过
            if i < len(data):
                i += 1
            continue
        # 注意：levels[0] 是第一轮删除的叶子，levels[-1] 是根
        preorder = build(levels)
        out_lines.append(preorder)
        if i < len(data) and data[i] == '$':
            break
        i += 1   # 跳过 '*' 或 '$'
    sys.stdout.write('\n'.join(out_lines))

if __name__ == '__main__':
    main()


                
            
                



        


                    



        
            




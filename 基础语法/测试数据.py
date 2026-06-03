#使用测试数据运行程序**

# 本书提供了一些题目的测试数据，见：
# https://github.com/GMyhf/2021fall-cs101/tree/main/cs101_test_data

# 下载并解压后，你会看到类似 `0.in`, `0.out` 的文件对。

# - `0.in` 是输入数据
# - `0.out` 是正确输出结果

# 将程序文件与测试数据放在同一目录下，然后在 **PowerShell** 中运行：

# ```powershell
# python 4A.py < 0.in > 0my.out
# ```

# 解释：

# - `< 0.in` 表示将 `0.in` 内容作为输入数据
# - `> 0my.out` 表示程序的输出结果写入到 `0my.out` 文件

# 此时，你只需对比 `0my.out` 与 `0.out`，即可发现程序与标准答案的差异，从而定位 bug。
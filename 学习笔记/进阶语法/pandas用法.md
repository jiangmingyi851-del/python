# Pandas 语法详解

## 1. **基本数据结构**

### Series (一维数据)
```python
import pandas as pd
import numpy as np

# 创建Series
s = pd.Series([1, 3, 5, np.nan, 6, 8])
s = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])

# Series操作
print(s.values)    # 值数组
print(s.index)     # 索引
print(s['a'])      # 按索引访问
print(s[0])        # 按位置访问
```

### DataFrame (二维数据)
```python
# 创建DataFrame
df = pd.DataFrame({
    'col1': [1, 2, 3, 4],
    'col2': ['a', 'b', 'c', 'd'],
    'col3': [10.5, 20.3, 30.1, 40.7]
})

# 从其他数据结构创建
df = pd.DataFrame(np.random.randn(6, 4), columns=['A', 'B', 'C', 'D'])
```

## 2. **数据选择和索引**

### 基本选择
```python
# 选择列
df['col1']          # 返回Series
df[['col1', 'col2']] # 返回DataFrame

# 选择行
df[0:2]             # 前两行
df.iloc[0]          # 按位置选择第一行
df.loc[0]           # 按索引选择第一行

# 条件选择
df[df['col1'] > 2]                    # col1大于2的行
df[(df['col1'] > 2) & (df['col2'] == 'c')]  # 多条件
```

### `loc` 和 `iloc` 详细用法
```python
# loc - 基于标签的选择
df.loc[0, 'col1']                     # 选择单个值
df.loc[0:2, ['col1', 'col2']]         # 选择行和列
df.loc[df['col1'] > 2, 'col2']        # 条件选择

# iloc - 基于位置的选择
df.iloc[0, 1]                         # 第一行第二列
df.iloc[0:3, 1:3]                     # 行0-2, 列1-2
df.iloc[[0, 2, 4], [1, 3]]            # 不连续选择
```

## 3. **向量化操作详解**

### 基本数学运算
```python
# 列间运算
df['new_col'] = df['col1'] + df['col2']
df['new_col'] = df['col1'] * 2 + df['col2'] / 3

# 使用NumPy函数
df['sqrt_col'] = np.sqrt(df['col1'])
df['log_col'] = np.log(df['col1'] + 1)

# 多列操作
df[['col1', 'col2']] = df[['col1', 'col2']] * 10
```

### 条件向量化操作
```python
# np.where - 三元条件运算
df['category'] = np.where(df['value'] > 100, 'high', 'low')

# 复杂条件
conditions = [
    df['score'] >= 90,
    df['score'] >= 80,
    df['score'] >= 70
]
choices = ['A', 'B', 'C']
df['grade'] = np.select(conditions, choices, default='D')

# 多条件赋值
df['status'] = np.where(
    (df['age'] > 30) & (df['income'] > 50000), 
    'senior', 
    'junior'
)
```

## 4. **apply 函数详解**

### 按行或列应用函数
```python
# 按行应用 (axis=1)
df['full_name'] = df.apply(
    lambda row: f"{row['first_name']} {row['last_name']}", 
    axis=1
)

# 按列应用 (axis=0)
df_mean = df.apply(np.mean, axis=0)

# 使用自定义函数
def calculate_bmi(row):
    return row['weight'] / (row['height'] ** 2)

df['bmi'] = df.apply(calculate_bmi, axis=1)

# 带参数的apply
def bonus_calc(row, multiplier=1.1):
    return row['salary'] * row['performance'] * multiplier

df['bonus'] = df.apply(bonus_calc, axis=1, multiplier=1.2)
```

### `applymap` - 元素级操作
```python
# 对每个元素应用函数
df_formatted = df.applymap(lambda x: f"${x:.2f}" if isinstance(x, (int, float)) else x)
```

## 5. **字符串向量化操作**

```python
# 字符串方法 (通过 .str 访问器)
df['name_upper'] = df['name'].str.upper()
df['name_length'] = df['name'].str.len()
df['first_letter'] = df['name'].str[0]

# 字符串包含检测
df['has_keyword'] = df['description'].str.contains('important', case=False)

# 字符串分割
df[['first', 'last']] = df['full_name'].str.split(' ', expand=True)

# 正则表达式
df['clean_phone'] = df['phone'].str.replace(r'\D', '', regex=True)
```

## 6. **分组和聚合**

### 基本分组操作
```python
# 单列分组
grouped = df.groupby('category')
print(grouped['value'].mean())

# 多列分组
multi_group = df.groupby(['category', 'subcategory'])

# 聚合函数
agg_result = df.groupby('category').agg({
    'value': ['mean', 'sum', 'std'],
    'count': 'count'
})

# 命名聚合
result = df.groupby('category').agg(
    avg_value=('value', 'mean'),
    total_value=('value', 'sum'),
    count=('value', 'count')
)
```

### 变换和过滤
```python
# transform - 保持原始形状
df['group_mean'] = df.groupby('category')['value'].transform('mean')

# filter - 过滤组
filtered = df.groupby('category').filter(lambda x: x['value'].mean() > 100)
```

## 7. **数据清洗和处理**

### 处理缺失值
```python
# 检测缺失值
df.isnull().sum()
df.notnull()

# 填充缺失值
df_filled = df.fillna(0)
df_filled = df.fillna(method='ffill')  # 前向填充
df_filled = df.fillna(df.mean())       # 用均值填充

# 删除缺失值
df_dropped = df.dropna()               # 删除任何包含NaN的行
df_dropped = df.dropna(axis=1)         # 删除列
df_dropped = df.dropna(subset=['col1', 'col2'])  # 指定列
```

### 数据类型转换
```python
# 查看数据类型
print(df.dtypes)

# 转换数据类型
df['col1'] = df['col1'].astype('int32')
df['col2'] = df['col2'].astype('category')

# 转换为日期
df['date'] = pd.to_datetime(df['date_string'])

# 优化数据类型
df = df.astype({
    'col1': 'int32',
    'col2': 'float32',
    'col3': 'category'
})
```

## 8. **合并和连接数据**

```python
# 合并DataFrame
result = pd.merge(df1, df2, on='key')
result = pd.merge(df1, df2, left_on='key1', right_on='key2', how='inner')

# 连接
result = pd.concat([df1, df2], axis=0)  # 行连接
result = pd.concat([df1, df2], axis=1)  # 列连接

# 追加
result = df1.append(df2, ignore_index=True)
```

## 9. **性能优化技巧**

### 避免链式赋值
```python
# 不好 - 链式赋值
df[df['value'] > 100]['new_col'] = 1  # 可能不工作

# 好 - 使用 loc
df.loc[df['value'] > 100, 'new_col'] = 1
```

### 使用查询优化
```python
# 使用 query 方法
result = df.query('col1 > 100 & col2 == "value"')

# 使用 eval 进行复杂计算
df['result'] = df.eval('(col1 + col2) * col3 / col4')
```

### 内存优化
```python
# 查看内存使用
print(df.info(memory_usage='deep'))

# 优化数值列
for col in df.select_dtypes(include=['int']):
    df[col] = pd.to_numeric(df[col], downcast='integer')

for col in df.select_dtypes(include=['float']):
    df[col] = pd.to_numeric(df[col], downcast='float')
```

## 10. **实际应用示例**

```python
# 完整的数据处理流程示例
def process_data(df):
    # 1. 数据清洗
    df = df.dropna(subset=['important_col'])
    df = df.fillna({'numeric_col': 0, 'text_col': 'Unknown'})
    
    # 2. 数据类型优化
    df = df.astype({
        'category_col': 'category',
        'int_col': 'int32'
    })
    
    # 3. 特征工程 (向量化操作)
    df['total_score'] = df[['score1', 'score2', 'score3']].sum(axis=1)
    df['avg_score'] = df[['score1', 'score2', 'score3']].mean(axis=1)
    df['performance'] = np.where(
        df['total_score'] > df['total_score'].mean(), 
        'above_avg', 
        'below_avg'
    )
    
    # 4. 分组计算
    summary = df.groupby('category').agg({
        'total_score': ['mean', 'std', 'count'],
        'avg_score': 'median'
    }).round(2)
    
    return df, summary

# 使用
processed_df, summary_stats = process_data(raw_df)
```

这些是 Pandas 的核心语法和最佳实践。掌握这些技巧可以让你写出既高效又易读的数据处理代码。关键是多练习，在实际项目中应用这些模式。
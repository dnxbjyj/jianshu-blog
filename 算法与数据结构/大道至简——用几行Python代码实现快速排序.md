本文主要介绍用python实现基本的快速排序算法，体会一下python的快排代码可以写得多么简洁。

# 1. 三言两语概括算法核心思想

先从待排序的数组中找出一个数作为基准数（取第一个数即可），然后将原来的数组划分成两部分：小于基准数的左子数组和大于等于基准数的右子数组。然后对这两个子数组再递归重复上述过程，直到两个子数组的所有数都分别有序。最后返回“左子数组” + “基准数” + “右子数组”，即是最终排序好的数组。

# 2. Talk is cheap, show the code


```python
# 实现快排
def quicksort(nums):
    if len(nums) <= 1:
        return nums
    
    # 左子数组
    less = []
    # 右子数组
    greater = []
    # 基准数
    base = nums.pop()
    
    # 对原数组进行划分
    for x in nums:
        if x < base:
            less.append(x)
        else:
            greater.append(x)
    
    # 递归调用
    return quicksort(less) + [base] + quicksort(greater)

def main():
	nums = [6,1,2,7,9,3,4,5,10,8]
	print quicksort(nums)

main()

```
输出：
```
 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

# 3. 优化
下面充分发挥Python的语法特性对上述过程进行一下优化。
```
# 导入随机数模块
In [1]: import random

# 查看random.randint函数的文档
In [2]: random.randint?
Signature: random.randint(a, b)
Docstring:
Return random integer in range [a, b], including both end points.

File:      d:\programs\python27\lib\random.py
Type:      instancemethod

# 生成20个在[-10,10]区间上的随机整数，存在nums列表中
In [5]: nums = [random.randint(-10,10) for x in range(20)]

In [6]: nums
Out[6]: [3, 2, -2, 8, 9, -3, 6, 4, -7, 5, 5, 10, 9, -2, 2, 6, -8, 9, -5, 8]

# 定义快速排序函数quick_sort
In [9]: def quick_sort(nums):
   ...:     if len(nums) <= 1:
   ...:         return nums
   ...:     # 随意选取一个基准数，比如选取列表第一个数
   ...:     base = nums[0]
   ...:     # left列表为nums中比基准数base小或等于base的数组成的列表
   ...:     left = [x for x in nums[1:] if x <= base]
   ...:     # right列表为nums中比基准数base大的数组成的列表
   ...:     right = [x for x in nums[1:] if x > base]
   ...:     # 对left和right列表递归排序
   ...:     return quick_sort(left) + [base] + quick_sort(right)
   ...:

# 对nums数组排序
In [10]: print quick_sort(nums)
[-8, -7, -5, -3, -2, -2, 2, 2, 3, 4, 5, 5, 6, 6, 8, 8, 9, 9, 9, 10]
```
可以看到只用了7行代码就实现了快排算法。

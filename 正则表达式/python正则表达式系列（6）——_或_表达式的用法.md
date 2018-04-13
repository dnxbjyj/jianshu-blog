```python
import re

s1 = u'距离地铁5号线189米'
s2 = u'距离地铁5号线(环中线)189米'
s3 = u'距离地铁5号线（环中线）189米'

p1 = re.compile(u'号线(\d+)米')
print re.findall(p1,s1)
# 输出：[u'189']
print re.findall(p1,s2)
# 输出：[]
print re.findall(p1,s3)
# 输出：[]

p2 = re.compile(u'(?:号线|\)|）)(\d+)')  # 注：这里的'?:'是为了取消分组，不在结果中捕获
print re.findall(p2,s1)
# 输出：[u'189']
print re.findall(p2,s2)
# 输出：[u'189']
print re.findall(p2,s3)
# 输出：[u'189']
```

```python
# 匹配java中的单行注释的正则表达式：
p1 = r'^\s*(//.*$|/\*.*\*/\s*$|$)'

# 匹配java中的多行注释的正则表达式：
code_text = '...'
p2 = r'/\*.+?\*/'
result = re.findall(p2,code_text,re.S)
```

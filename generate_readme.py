# coding:utf-8
# 生成简书博客的目录结构，并添加至顶层的README.md文件夹中
import os
import urlparse
from collections import OrderedDict
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    root_dir = './'
    with open('tmp_readme.txt','w+') as readme:
        head = '''
# 我的简书技术博客文章同步

### 基本信息

* [我的简书首页](https://www.jianshu.com/u/c398cdabbd5c)
* 我的简书用户名：m2fox

### 目录概览
'''
        readme.write(head + '\n')
    
        for root,dirs,files in os.walk(root_dir):
            if root.startswith('./.git') or root == './':
                continue
            dir_url_abs_path = urlparse.urljoin('https://github.com/dnxbjyj/blog/tree/master/',os.path.basename(root))
            readme.write('* [**{section_name}**]({section_url})\n'.format(section_name = os.path.basename(root),section_url = dir_url_abs_path))
            for file in files:
                base_name = os.path.basename(file)
                file_url_abs_path = urlparse.urljoin('https://github.com/dnxbjyj/blog/blob/master/',os.path.basename(root) + '/')
                file_url_abs_path = urlparse.urljoin(file_url_abs_path,base_name)
                readme.write('\t* [{article_name}]({article_url})\n'.format(article_name = base_name,article_url = file_url_abs_path))
            readme.write('\n\n')
    
if __name__ == '__main__':
    main()
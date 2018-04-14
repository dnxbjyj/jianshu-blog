# coding:utf-8
# 生成简书博客的目录结构，并把生成的目录结构内容添加至顶层的README.md文件中
from __future__ import unicode_literals
import os
import urlparse
from collections import OrderedDict
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MarkdownUtil(object):
    '''
    markdown文本处理工具类
    '''
    def head(self,text,level = 1):
        '''
        获取标题文本
        举例：
        # 标题1
        
        :param text: 文本内容
        :param level: 标题级数，最多支持6级标题，默认为1级标题
        :returns: Markdown标题文本
        '''
        return '{mark} {text}'.format(mark = '#' * level,text = text)
    def bold(self,text):
        '''
        获取加粗文本
        举例：
        **这是加粗文本**
        
        :param text: 文本内容
        :returns: Markdown加粗文本
        '''
        return '**{text}**'.format(text = text)
    def item(self,text,retract = 0):
        '''
        获取单行列表项文本
        举例：
        * 项目1
        
        :param text: 文本内容
        :retract: 缩进的空格数，默认为0
        :returns: 列表项文本
        '''
        return '{retract}* {text}'.format(retract = ' ' * retract,text = text)
    def items(self,text_list,retract = 0):
        '''
        获取多行列表项文本
        举例：
        * 项目1
        * 项目2
        * 项目3
        
        :param text_list: 文本列表
        :retract: 缩进的空格数，默认为0
        :returns: 多行列表项文本
        '''
        return '\n'.join(item(text,retract) for text in text_list if text)
    def link(self,text,href):
        '''
        获取链接文本
        举例：
        [百度](https://www.baidu.com)
        
        :param text: 链接的显示文本
        :param href: 链接的地址
        :returns: 链接文本
        '''
        return '[{text}]({href})'.format(text = text,href = href)
    def enter(self,text,num = 1):
        '''
        在文本末尾加指定数目的换行符
        举例：
        这是一行文字\n
        
        :param text: 文本内容
        :param num: 换行符数量
        :returns: 在末尾追加了num个换行符的文本
        '''
        return '{text}{enter}'.format(text = text,enter = '\n' * num)

def main():
    root_dir = './'
    MD = MarkdownUtil()
    with open('tmp_readme.txt','w+') as readme:
        # 写入我的简书的基本信息
        readme.write(MD.enter(MD.head('我的简书技术博客文章同步'),2))
        readme.write(MD.enter(MD.bold('注：本文件的全部内容（包括现在的这一行文字）都是由当前目录下的generate_readme.py脚本自动生成。'),2))
        readme.write(MD.enter(MD.head('博客信息',3),2))
        readme.write(MD.enter(MD.item(MD.link('我的简书首页','https://www.jianshu.com/u/c398cdabbd5c'))))
        readme.write(MD.enter(MD.item('我的简书用户名：m2fox'),2))
        
        
        # 写入博客文章的目录列表
        readme.write(MD.enter(MD.head(u'目录概览',3),2))
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
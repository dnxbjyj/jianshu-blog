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
    def head(self,text,level = 1,enter_num = 1):
        '''
        获取标题文本
        举例：
        # 标题1
        
        :param text: 文本内容
        :param level: 标题级数，最多支持6级标题，默认为1级标题
        :param enter_num: 文本末尾加的换行数，默认为1
        :returns: Markdown标题文本
        '''
        return '{mark} {text}{enter}'.format(mark = '#' * level,text = text,enter = '\n' * enter_num)
    def bold(self,text,enter_num = 1):
        '''
        获取加粗文本
        举例：
        **这是加粗文本**
        
        :param text: 文本内容
        :param enter_num: 文本末尾加的换行数，默认为1
        :returns: Markdown加粗文本
        '''
        return '**{text}**{enter}'.format(text = text,enter = '\n' * enter_num)
    def item(self,text,retract = 0,enter_num = 1):
        '''
        获取单行列表项文本
        举例：
        * 项目1
        
        :param text: 文本内容
        :retract: 缩进的空格数，默认为0
        :param enter_num: 文本末尾加的换行数，默认为1
        :returns: 列表项文本
        '''
        return '{retract}* {text}{enter}'.format(retract = ' ' * retract,text = text,enter = '\n' * enter_num)
    def items(self,text_list,retract = 0,enter_num = 1):
        '''
        获取多行列表项文本
        举例：
        * 项目1
        * 项目2
        * 项目3
        
        :param text_list: 文本列表
        :retract: 缩进的空格数，默认为0
        :param enter_num: 文本末尾加的换行数，默认为1
        :returns: 多行列表项文本
        '''
        return '\n'.join(item(text,retract,enter_num = 0) for text in text_list if text)
    def link(self,text,href,enter_num = 1):
        '''
        获取链接文本
        举例：
        [百度](https://www.baidu.com)
        
        :param text: 链接的显示文本
        :param href: 链接的地址
        :param enter_num: 文本末尾加的换行数，默认为1
        :returns: 链接文本
        '''
        return '[{text}]({href}){enter}'.format(text = text,href = href,enter = '\n' * enter_num)
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
    def refer(self,text,enter_num = 1):
        '''
        把一个文本变成引用文本
        举例：
        > 这是一段引用文字
        
        :param text: 文本内容
        :param enter_num: 文本末尾加的换行数，默认为1
        :returns: 引用文本
        '''
        return '> {text}{enter}'.format(text = text,enter = '\n' * enter_num)

def generate_copyright():
    MD = MarkdownUtil()
    statement = '版权声明：本仓库的所有文章来源于m2fox的简书（{jianshu_link}）文章，版权归本人所有，转载请注明出处为本仓库地址（{from_}），禁止用于任何商业目的。'.format(jianshu_link = MD.link('jianshu.com','https://www.jianshu.com',0),from_ = MD.link('github.com/dnxbjyj/blog','https://github.com/dnxbjyj/blog',0))
    return MD.refer(statement,2)
        
def main():
    root_dir = './'
    MD = MarkdownUtil()
    with open('tmp_readme.txt','w+') as readme:
        # 写入我的简书的基本信息
        readme.write(MD.head('我的简书技术博客文章同步',2))
        # 版权声明
        readme.write(generate_copyright())
        readme.write(MD.bold('注：本文件的全部内容（包括现在的这一行文字）都是由当前目录下的generate_readme.py脚本自动生成。',2))
        readme.write(MD.head('博客信息',3,1))
        readme.write(MD.item(MD.link('我的简书首页','https://www.jianshu.com/u/c398cdabbd5c',0),0,1))
        readme.write(MD.item('我的简书用户名：m2fox',0,2))
        
        
        # 自动化扫描并生成、写入博客文章的目录列表
        readme.write(MD.head(u'目录概览',3))
        for root,dirs,files in os.walk(root_dir):
            if root.startswith('./.git') or root == './':
                continue
            dir_url_abs_path = urlparse.urljoin('https://github.com/dnxbjyj/blog/tree/master/',os.path.basename(root))
            # 文集名称
            section_name = MD.bold(os.path.basename(root),0)
            readme.write(MD.item(MD.link(section_name,dir_url_abs_path,0),0,1))
            for file in files:
                base_name = os.path.basename(file)
                file_url_abs_path = urlparse.urljoin('https://github.com/dnxbjyj/blog/blob/master/',os.path.basename(root) + '/')
                file_url_abs_path = urlparse.urljoin(file_url_abs_path,base_name)
                article_name = ''.join(base_name.split('.')[:-1])
                # 文章链接
                readme.write(MD.item(MD.link(article_name,file_url_abs_path,0),4,1))
            readme.write('\n\n')
if __name__ == '__main__':
    main()
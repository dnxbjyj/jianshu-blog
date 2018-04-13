> 参考：
[wxPython官方文档](https://docs.wxpython.org/)
[wxPython官方示例demo下载](https://extras.wxpython.org/wxPython4/extras/4.01/)
注：这些示例demo非常有助于入门学习，短小精悍，可快速上手。

有时候在用Python做一些小功能、小工具的时候，希望能封装成GUI桌面程序，方便自己和别人使用。Python有一个内置GUI库`tkinter`，还有`wxPython`、`pyQt`等第三方GUI库，经过多方对比，最终决定使用`wxPthon`这样一个库来开发自己的GUI小程序。

当然你也可以选择使用Python的Web框架来开发B/S模式的GUI程序，但那就是另外一些技术栈了，适用于写功能比较复杂的程序。而像做一些小工具这样的程序，用`wxPython`这样的GUI库足矣，开发起来快速、打包便捷。

# 安装
* 安装wxPython库：`pip install wxpython`
* 在代码中导入wxPython库：`import wx`

# Hello World程序
下面写一个Hello World程序：
```python
# coding:utf-8
# wxPython hello world程序
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    # 1. 创建程序对象
    app = wx.App()
    
    # 2. 创建Frame对象
    win = wx.Frame(None,title = 'Hello World',size = (300,200))
    # 3. 在Frame对象上创建Panel面板对象
    panel = wx.Panel(win)
    # 4. 创建显示文本的区域
    text_area = wx.TextCtrl(panel, style=wx.TE_READONLY)
    # 设置文本区域值
    text_area.SetValue('Hello World!')
    # 5. 创建横向容器box
    hbox = wx.BoxSizer()
    # 6. 把文本区域放到hbox中
    hbox.Add(text_area, proportion=1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=0)
    # 7. 把hbox放到面板中
    panel.SetSizer(hbox)
    
    # 8. 显示窗口
    win.Show()
    # 9. 程序主循环
    app.MainLoop()
    
if __name__ == '__main__':
    main()
```
运行上面代码，显示：
![](https://upload-images.jianshu.io/upload_images/8819542-f77651a607e76585.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
通过上面代码，一个Hello world程序就完成了。

# 一个简单的文本编辑器
下面我们来做一个稍微复杂一点的例子，实现一个简单的文本编辑器，就给它起名为`foxpad`吧，支持以下几点功能：
* 打开文本文件
* 编辑文件内容
* 保存对文件的修改

上代码（代码中有详细的注释）：foxpad.py：
```python
# coding:utf-8
# 用wxPython实现一个最简单的文本编辑器
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Foxpad(object):
    '''
    Foxpad文本编辑器类
    '''
    def __init__(self, size = (700, 500)):
        '''
        初始化窗口
        '''
        self.__size = size
        # 创建Frame窗口对象
        self.__win = wx.Frame(None,title = "Foxpad",size = size)
        # 在窗口对象上创建Panel面板对象
        self.__bkg = wx.Panel(self.__win)
        
        # 创建"打开"按钮，用于打开文件
        self.__openBtn = wx.Button(self.__bkg, label='打开')
        # 给该按钮绑定回调函数：openFile
        self.__openBtn.Bind(wx.EVT_BUTTON, self.openFile)

        # 创建用于显示选择的文件的路径的文本区对象
        self.__filepath_area = wx.TextCtrl(self.__bkg, style=wx.TE_READONLY)
        
        # 创建"保存"按钮，用于保存对文件的修改
        self.__saveBtn = wx.Button(self.__bkg, label='保存')
        # 给该按钮绑定回调函数：saveFile
        self.__saveBtn.Bind(wx.EVT_BUTTON, self.saveFile)
        
        # 创建一个横向box，相当于一个容器
        self.__hbox = wx.BoxSizer()
        # 往横向box中添加打开文件按钮、文件路径文本区、保存文件按钮
        # proportion：控件的横向比例，为0表示自适应大小
        # flag：控件的位置参数、拉伸等属性
        # border：控件的外边距像素值
        self.__hbox.Add(self.__openBtn, proportion=0, flag=wx.LEFT | wx.ALL, border=5)
        self.__hbox.Add(self.__filepath_area, proportion=1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)
        self.__hbox.Add(self.__saveBtn, proportion=0, flag=wx.LEFT | wx.ALL, border=5)

        # 创建一个纵向box，相当于一个容器
        self.__vbox = wx.BoxSizer(wx.VERTICAL)
        # 把横向box添加到纵向box中，比例自适应
        self.__vbox.Add(self.__hbox, proportion=0, flag=wx.EXPAND | wx.ALL)
        
        # 创建用于显示文件文本内容的多行文本区对象
        self.__multiline_editor = wx.TextCtrl(self.__bkg, style=wx.TE_MULTILINE)
        # 把多行文本区添加到纵向box中，比例为1，即尽量多占
        self.__vbox.Add(self.__multiline_editor,proportion=1,flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT,border=5)

        # 把纵向box放到窗口面板中
        self.__bkg.SetSizer(self.__vbox)
    def show(self):
        '''
        显示窗口
        '''
        # 显示窗口
        self.__win.Show()
    def openFile(self,evt):
        '''
        打开按钮回调函数
        '''
        # 打开系统默认风格的文件选择对话框
        dlg = wx.FileDialog(self.__win,"打开文件","","","All files (*.*)|*.*",wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        filepath = ''
        # 当点击了文件选择对话框的确认按钮，给filepath变量赋值为当前选择的文件的路径；如果点击了取消按钮，不做任何操作
        if dlg.ShowModal() == wx.ID_OK:
            filepath = dlg.GetPath()
        else:
            # 当点击了取消按钮或关闭对话框按钮，什么也不做
            return
        # 设置文件路径文本区对象的值为选中的文件路径（绝对路径）
        self.__filepath_area.SetValue(filepath)
        # 打开文件，读取文件内容并显示到多行编辑区中
        with open(filepath,'r') as file:
            fcontent = file.read()
            self.__multiline_editor.SetValue(fcontent)
    def saveFile(self,evt):
        '''
        保存按钮回调函数
        '''
        # 如果当前打开的文件为空，直接返回
        if not self.__filepath_area.GetValue():
            return
        # 获取当前多行编辑区的文本内容
        fcontent = self.__multiline_editor.GetValue()
        # 把当前的文本内容写入文件
        with open(self.__filepath_area.GetValue(),'w+') as file:
            file.write(fcontent)
        # 弹出消息框，提示保存成功，消息框的样式采用"OK_DEFAULT"类型的消息框
        dlg = wx.MessageDialog(None, "保存成功！", "保存修改", wx.OK_DEFAULT)
        # 显示消息框
        dlg.ShowModal()

def main():
    # 创建程序对象
    app = wx.App()
    
    # 创建foxpad对象
    foxpad = Foxpad()
    # 显示窗口
    foxpad.show()
    
    # 程序主循环
    app.MainLoop()
    
if __name__ == '__main__':
    main()
```
运行上面的代码，弹出一个窗口如下：
![](https://upload-images.jianshu.io/upload_images/8819542-f652291f8cf7df6a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击"打开"按钮，会打开Windows系统默认的文件选择对话框：
![](https://upload-images.jianshu.io/upload_images/8819542-ca776a4d84f5215a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

选择一个文件，比如`test.txt`，然后就可以在多行编辑区编辑这个文件的内容：
![](https://upload-images.jianshu.io/upload_images/8819542-2b05d55f031505b2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后点"保存"按钮，提示保存成功：
![](https://upload-images.jianshu.io/upload_images/8819542-241f99e5f62ce18d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 把foxpad.py打包成exe可执行程序
完成了foxpad程序的编写之后，如果想把它打包成一个独立的exe文件，可以直接双击就能运行，也可以在没有安装Python和wxPython的电脑上也可以使用，那么是时候用pyinstaller打包一把了（需要提前用`pip install pyinstaller`命令安装好pyinstaller工具，pyinstaller详细用法参见：[python打包工具pyinstaller的用法](https://www.jianshu.com/p/c9837145cb92)）。

打开命令行，cd到foxpad.py文件所在的目录，然后执行命令：
`pyinstaller -F -w foxpad.py`

稍等片刻后，在当前目录下的`dist`目录下就可以看到`foxpad.exe`这么一个独立可执行程序了，双击`foxpad.exe`执行，可以看到和刚刚用python运行`foxpad.py`同样的效果。

# 总结
本文写了两个非常简单的小例子来展示wxPython这样一个GUI库的入门用法，旨在对这个库有一个基本的认识。更深入的学习可去看官方文档和官方demo，强烈推荐去看官方提供的demo，有很多简单、实用的现成例子，从实例入手，学习起来更加事半功倍。

---
源码已经放到：[我的GitHub](https://github.com/dnxbjyj/python-basic/tree/master/gui/wxpython/samples)

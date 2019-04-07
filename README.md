# kdPythonAPIViewer
通过GUI界面查看python或第三方库的API。

query Python API and third party library API via GUI interface.

# 安装

## 方法一

– 使用[kdPythonInstaller(https://github.com/bkdwei/kdPythonInstaller/releases/download/v1.0.0/kdPythonInstaller-1.0.0.exe/) 快速安装python和kdPythonAPIViewer

## 方法二

- 安装python3和pip，[安装包地址](https://www.python.org/downloads/ 下载地址)
- 使用pip安装kdPythonAPIViewer，命令
	** pip install kdPythonAPIViewer **
- 点击桌面的快捷方式或开始菜单启动kdPythonAPIViewer

# 截图

![kdPythonAPIViewer_screenshot](/screenshot/os.jpg)
![kdPythonAPIViewer_screenshot](/screenshot/os.path.jpg)
![kdPythonAPIViewer_screenshot](/screenshot/QLineEdit.setText.jpg)
![kdPythonAPIViewer_screenshot](/screenshot/QLine)
![kdPythonAPIViewer_screenshot](/screenshot/QLineEdit.show.jpg)

# 使用说明
- 首次使用或安装了新的Python库时，需要先点击“缓存Python库”
- 选择左侧下拉框中的库，然后在类的输入框任意输入一个类的名称即可加载该类的API。比如下拉框选择PyQt5，在类的输入框键入qli即可显示PyQt5.Qt.QLineEdit组件，回车即可显示API文档。![kdPythonAPIViewer_screenshot](/screenshot/使用说明.jpg)
- 加载完类的文档后，可以点击方法与属性下拉框，查看该类对应的方法和属性
- 当库的描述文档太大时（比如PyQt5.QtWidgets的文档就特别大），可以设置仅显示类的文档




# 提交bug和建议
[提交bug和建议](https://github.com/bkdwei/kdPythonAPIViewer/issues)
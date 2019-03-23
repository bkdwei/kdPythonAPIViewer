#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from os import  path
import sys
import json
import inspect
import pkgutil
from PyQt5.QtCore import pyqtSlot, Qt, QFile
from PyQt5.Qt import QCursor, QPushButton
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QWidget,QTreeWidgetItem,QApplication
from PyQt5.QtGui import QTextDocument
from PyQt5.uic import loadUi
from .fileutil import get_file_realpath,config_file,check_and_create
from .pydocc import Helper,resolve

class kdPythonAPIViewer(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(get_file_realpath("kdPythonAPIViewer.ui"), self)

        self.helper = Helper()
        self.load_dict()

        self.le_text.returnPressed.connect(self.on_pb_query_clicked)
        self.le_search.returnPressed.connect(self.on_le_search_returnPressed)
        self.show_status = True
        
#         悬浮置顶按钮
#         self.float_btn = QPushButton("kdPythonAPIViewer")
#         self.float_btn.setWindowFlags(Qt.WindowStaysOnTopHint)
#         self.float_btn.clicked.connect(self.show_window)
#         self.float_btn.show()
        
#     加载系统的已安装的python模块
    def load_dict(self):
        if path.exists(config_file) :
            with open(config_file, "r") as f:
                content = f.read().strip()
                if content != "" :
                    jcontent = json.loads(content)
#                   加载模块时不触发cb_module的currentIndexChanged事件
                    self.adding_module_flag = True
#                     默认不选中任何包
                    self.cb_module.addItem("")
                    for j in jcontent:
                        self.cb_module.addItem(j)
                    self.adding_module_flag = False
                    return
        self.on_pb_refresh_module_clicked()

#   选中某一个包时,加载包下的所有模块
    # ~ @pyqtSlot()
    def on_cb_module_currentIndexChanged(self):
        if not self.adding_module_flag :
            cur_module = self.cb_module.currentText()
            children =self.get_children(cur_module)
            self.fillWidget(children)

#   渲染左侧模块树
    def fillItem(self, item, value):
        if type(value) is dict:
            for key, val in sorted(value.items()):
                child = QTreeWidgetItem()
                child.setText(0, key)
                item.addChild(child)
                item.setExpanded(True)
                child.setFlags(child.flags())
                self.fillItem(child, val)
        elif type(value) is list:
            for single_value in value:
                self.fillItem(item, single_value)
        else:
            child = QTreeWidgetItem()
            child.setText(0, str(value))
            item.addChild(child)
            item.setExpanded(True)

#     初始化左侧模块树
    def fillWidget(self, value):
        self.tw_catelog.clear()
        self.fillItem(self.tw_catelog.invisibleRootItem(), value)

    @pyqtSlot()
    def on_le_text_focusOutEvent(self):
        self.on_pb_query_clicked()

#     点击查询按钮，根据输入框的内容动态解析并查询模块的文档
    @pyqtSlot()
    def on_pb_query_clicked(self):
        query_text = self.le_text.text().strip()
        module_ = None
        show_api_info = True

        # ~ 只有import的情形，形如import string
        only_import_flag = query_text.find("import") == 0
        if only_import_flag:
            module_ = query_text.replace("import", "").strip()

        # ~ 导入单个模块，形如from PyQt5.QtWidgets import QMainWindow
        single_import_flag = (
            query_text.find("from") >= 0
            and query_text.find(",") < 0
            and query_text.find("*") < 0
        )
        if single_import_flag:
            module_ = (
                query_text.replace("from", "").replace("import", ".").replace(" ", "")
            )

        # ~ 导入多个模块，形如from PyQt5.QtWidgets import QMainWindow, QFileDialog, QWidget
        self.multi_import_flag = (
            query_text.find("from") >= 0
            and query_text.find(",") > 0
            and query_text.find("*") < 0
        )
        if self.multi_import_flag:
            show_api_info = False
            module_ = query_text.split("import")
            self.main_module = module_[0].replace("from", "").strip()
            sub_module = str(module_[1]).split(",")
            self.cb_sub_text.clear()
            self.adding_item_flag = True
            for m in sub_module:
                self.cb_sub_text.addItem(str(m).strip())
            self.cb_sub_text.showPopup()
            self.adding_item_flag = False

        if show_api_info:
            self.get_api_doc(module_)
    # ~ @pyqtSlot()
    def on_cb_sub_text_currentIndexChanged(self):
        if self.adding_item_flag is not True:
            cur_item = self.cb_sub_text.currentText()
            module_ = self.main_module + "." + cur_item
            self.get_api_doc(str(module_))

#     查询指定模块或包的API文档
    def get_api_doc(self, module_):
        doc = self.helper.help(str(module_))
        self.tb_result.setHtml(doc)
    
#     拦截快捷键
    def keyPressEvent(self, event):
        curKey = event.key()
        # ~ print("按下：" + str(event.key()))
        if curKey == Qt.Key_F2:
            self.cb_module.setFocus()
            self.cb_module.showPopup()
        elif curKey == Qt.Key_F3:
            self.le_text.setFocus()
        elif curKey == Qt.Key_F4:
            self.cb_sub_text.setFocus()
            self.cb_sub_text.showPopup()
        elif curKey == Qt.Key_F5:
            self.le_search.setFocus()
            self.le_search.selectAll()
        elif curKey == Qt.Key_F6:
            self.showMinimized()
    

    def find(self, keyword):
        # ~ 先向下查找,没有结果则向上查找，貌=貌似不会往回查询
        if not self.tb_result.find(keyword):
            self.tb_result.find(keyword, QTextDocument.FindBackward)

#     单击指定的包
    def on_tw_catelog_itemClicked(self):
        cur_item = self.tw_catelog.currentItem()
        fullpath = self.get_fullpath_of_treeitem(cur_item,cur_item.text(0))
        children = self.get_children(fullpath)
        if cur_item.childCount() == 0 :
            self.fillItem(cur_item,children)
        else :
            cur_item.setExpanded(not cur_item.isExpanded())

#     获取模块完整的包路径
    def get_fullpath_of_treeitem(self,item,path):
        parent = item.parent()
        if parent is None:
            cur_module = self.cb_module.currentText()
            return cur_module + "." + path
        else:
            return self.get_fullpath_of_treeitem(parent,parent.text(0) + "." + path)

#     获取指定包下的子包或模块
    def get_children(self, path):
        children = []
        object, name = resolve(path, 0)
        if inspect.ismodule(object):
#             print("is module")
            if self.rb_all.isChecked():
                self.get_api_doc(path)
            if hasattr(object, '__path__'):
                names = [name  for filefiner, name, ispkg in pkgutil.iter_modules(object.__path__)]
#                 print("names:",names)
                children +=names
            else:
                # ~ modules = inspect.getmembers(object, inspect.ismodule)
                modules = inspect.getmembers(object, inspect.isclass)
                # ~ print("modules",modules)
                children +=[m[0] for m in modules]
        if inspect.isclass(object):
#             print("is class")
            self.get_api_doc(path)
            # ~ children.append(inspect.getmembers(PyQt5, inspect.ismodule))
        if inspect.isroutine(object):
            print("is routine")
        return children

    # ~ 输入框回车后在API文档中查找对应的关键字
    @pyqtSlot()
    def on_le_search_returnPressed(self):
        # ~ 先向下查找,没有结果则向上查找
        keyword = self.le_search.text()
        if self.tb_result.find(keyword) is not True:
            self.tb_result.find(keyword, QTextDocument.FindBackward)
    
#     刷新系统的模块列表，并存入到dict.dat文件，加入程序的启动速度
    @pyqtSlot()
    def on_pb_refresh_module_clicked(self):
        modules  =self.helper.listmodules()
#         print(modules)
        self.cb_module.clear()
        self.adding_module_flag = True
        self.cb_module.addItems(modules)
        self.adding_module_flag = False
        
        check_and_create(config_file)
        with open(config_file,"w+") as f:
            f.write(json.dumps(modules))
    
#     def show_window(self):
#         self.show_status = not self.show_status
#         self.setVisible(self.show_status)
def main():
    import sys
    app = QApplication(sys.argv)
    win = kdPythonAPIViewer()
    win.showMaximized()
#     win.show()
    win.cb_module.showPopup()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
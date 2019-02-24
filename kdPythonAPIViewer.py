#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import sys
import webbrowser
import json
import inspect
import pkgutil
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, QFile, QTextCodec
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QWidget,QTreeWidgetItem
from PyQt5.QtGui import QTextDocument
from PyQt5.uic import loadUi
from fileutil import check_and_create, check_and_create_dir
from pydocc import Helper,resolve

class kdPythonAPIViewer(QWidget):
    def __init__(self):
        super(kdPythonAPIViewer, self).__init__()
        loadUi(sys.path[0] + "/kdPythonAPIViewer.ui", self)

        self.helper = Helper()

        # ~ self.navigate = navigate()
        # ~ 在API文档中查找对应的关键字
        # ~ self.navigate.find_word_signal.connect(self.find)
        # ~ self.navigate.show_key_press_signal.connect(self.switch_navigate_window_state)
        self.load_dict()

        self.le_text.returnPressed.connect(self.on_pb_query_clicked)
        self.le_search.returnPressed.connect(self.on_le_search_returnPressed)
        # ~ self.main_win.centralWidget()
        # ~ screen = QtGui.QDesktopWidget().screenGeometry()
        # ~ self.setGeometry(0, 0, screen.width(), screen.height())


    def load(self, url):
        self.webview.load(QUrl(url))
        self.webview.show()

    def load_dict(self):
        if os.path.exists(sys.path[0] +  "/dict.dat") :
            with open(sys.path[0] + "/dict.dat", "r") as f:
                content = f.read().strip()
                if content != "" :
                    jcontent = json.loads(content)
                    self.adding_module_flag = True
                    self.cb_module.addItem("")
                    for j in jcontent:
                        self.cb_module.addItem(j)
                    self.adding_module_flag = False

                    # ~ self.render_dict_tree(content)
    # ~ @pyqtSlot()
    def on_cb_module_currentIndexChanged(self):
        if self.adding_module_flag is False:
            cur_module = self.cb_module.currentText()
            print(cur_module)
            children =self.get_children(cur_module)
            self.fillWidget(children)

   # Fills single cell in table
    def fillItem(self, item, value):
        if type(value) is dict:
            for key, val in sorted(value.items()):
                child = QtWidgets.QTreeWidgetItem()
                print("key:",key)
                child.setText(0, key)
                item.addChild(child)
                item.setExpanded(True)
                child.setFlags(child.flags() | QtCore.Qt.ItemIsEditable)
                self.fillItem(child, val)
        elif type(value) is list:
            print("list:",value)
            for single_value in value:
                # ~ child = QtWidgets.QTreeWidgetItem()
                # ~ print("single_value",single_value)
                self.fillItem(item, single_value)
        else:
            child = QtWidgets.QTreeWidgetItem()
            child.setText(0, str(value))
            item.addChild(child)
            item.setExpanded(True)

    # Fills entire table widget
    def fillWidget(self, value):
        self.tw_catelog.clear()
        self.fillItem(self.tw_catelog.invisibleRootItem(), value)

    @pyqtSlot()
    def on_le_text_focusOutEvent(self):
        self.on_pb_query_clicked()

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
            # ~ print(",".join(sub_module))
            self.cb_sub_text.clear()
            self.adding_item_flag = True
            for m in sub_module:
                self.cb_sub_text.addItem(str(m).strip())
            self.cb_sub_text.showPopup()
            self.adding_item_flag = False
            # ~ self.on_cb_sub_text_currentIndexChanged()

        if show_api_info:
            self.get_api_doc(module_)
    # ~ @pyqtSlot()
    def on_cb_sub_text_currentIndexChanged(self):
        if self.adding_item_flag is not True:
            cur_item = self.cb_sub_text.currentText()
            module_ = self.main_module + "." + cur_item
            self.get_api_doc(str(module_))

    def get_api_doc(self, module_):
        doc = self.helper.help(str(module_))
        self.tb_result.setHtml(doc)
        # ~ self.tb_result.setText(doc)
        # ~ self.navigate.init_catelog(doc)
        # ~ self.tb_result.find("Methods inherited from")
        # ~ 定为到指定行
        # ~ self.tb_result.find("Methods inherited from")
        # ~ QTextBrowser
        # ~ self.webview.setHtml("<html>a</html>")

    def keyPressEvent(self, event):
        curKey = event.key()
        # ~ print("按下：" + str(event.key()))
        if curKey == Qt.Key_F2:
            self.cb_module.setFocus()
            self.switch_navigate_window_state(True)
        elif curKey == Qt.Key_F3:
            self.le_text.setFocus()
        elif curKey == Qt.Key_F4:
            self.cb_sub_text.showPopup()
        elif curKey == Qt.Key_F5:
            self.le_search.setFocus()
        elif curKey == Qt.Key_F6:
            self.showMinimized()

    def switch_navigate_window_state(self, show_flag):
        if show_flag:
            self.navigate.show()
            self.navigate.activateWindow()
        else:
            self.navigate.hide()

    def find(self, keyword):
        # ~ 先向下查找,没有结果则向上查找
        if self.tb_result.find(keyword) is not True:
            self.tb_result.find(keyword, QTextDocument.FindBackward)

    def close(self):
        self.navigate.close()

    def on_tw_catelog_itemClicked(self):
        # ~ print(self.tw_catelog.currentItem().text(0))
        cur_item = self.tw_catelog.currentItem()
        # ~ print(cur_item.parent().text(0))

        fullpath = self.get_fullpath_of_treeitem(cur_item,cur_item.text(0))
        print(fullpath)
        children = self.get_children(fullpath)
        if cur_item.childCount() == 0 :
            self.fillItem(cur_item,children)
            print("data",cur_item.childCount())
        else :
            print(cur_item.isExpanded())
            cur_item.setExpanded(not cur_item.isExpanded())



    def get_fullpath_of_treeitem(self,item,path):
        parent = item.parent()
        if parent is None:
            cur_module = self.cb_module.currentText()
            return cur_module + "." + path
        else:
            return self.get_fullpath_of_treeitem(parent,parent.text(0) + "." + path)

    def get_children(self, path):
        children = []
        object, name = resolve(path, 0)
        if inspect.ismodule(object):
            print("is module")
            if self.rb_all.isChecked():
                self.get_api_doc(path)
            if hasattr(object, '__path__'):
                names = [name  for filefiner, name, ispkg in pkgutil.iter_modules(object.__path__)]
                print("names:",names)
                children +=names
            else:
                # ~ modules = inspect.getmembers(object, inspect.ismodule)
                modules = inspect.getmembers(object, inspect.isclass)
                # ~ print("modules",modules)
                children +=[m[0] for m in modules]
        if inspect.isclass(object):
            print("is class")
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
    @pyqtSlot()
    def on_pb_refresh_module_clicked(self):
        modules  =self.helper.listmodules()
        print(modules)
        self.cb_module.clear()
        self.adding_module_flag = True
        self.cb_module.addItems(modules)
        self.adding_module_flag = False
        with open(sys.path[0] + "/dict.dat","w+") as f:
            f.write(json.dumps(modules))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = kdPythonAPIViewer()
    win.showMaximized()
    print(dir(win))
    win.cb_module.showPopup()
    sys.exit(app.exec_())

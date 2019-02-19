# coding: utf-8
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, QFile, QTextCodec
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
import sys
import webbrowser
from PyQt5.QtGui import QTextDocument
from PyQt5.uic import loadUi
from fileutil import check_and_create, check_and_create_dir
from pydocc import Helper
from navigate import navigate


class kdPythonAPIViewer(QWidget):
    def __init__(self):
        super(kdPythonAPIViewer, self).__init__()
        loadUi("kdPythonAPIViewer.ui", self)
        # ~ print(dir(Qt))

        self.webview = QWebEngineView()
        self.helper = Helper()

        self.navigate = navigate()
        # ~ 在API文档中查找对应的关键字
        self.navigate.find_word_signal.connect(self.find)
        self.navigate.show_key_press_signal.connect(self.switch_navigate_window_state)

    def load(self, url):
        self.webview.load(QUrl(url))
        self.webview.show()

    @pyqtSlot()
    def on_cb_text_focusOutEvent(self):
        self.on_pb_query_clicked()

    @pyqtSlot()
    def on_pb_query_clicked(self):
        query_text = self.cb_text.currentText().strip()
        if self.cb_text.findText(query_text) < 0:
            self.cb_text.addItem(query_text)
        module_ = None
        print(query_text)
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
            self.adding_item_flag = False
            # ~ self.on_cb_sub_text_currentIndexChanged()

        if show_api_info:
            self.get_api_doc(module_)

    def on_cb_sub_text_currentIndexChanged(self):
        if self.adding_item_flag is not True:
            cur_item = self.cb_sub_text.currentText()
            module_ = self.main_module + "." + cur_item
            self.get_api_doc(str(module_))

    def get_api_doc(self, module_):
        doc = self.helper.help(str(module_))
        self.tb_result.setHtml(doc)
        # ~ self.tb_result.setText(doc)
        self.navigate.init_catelog(doc)
        # ~ self.tb_result.find("Methods inherited from")
        # ~ 定为到指定行
        # ~ self.tb_result.find("Methods inherited from")
        # ~ QTextBrowser
        # ~ self.webview.setHtml("<html>a</html>")

    def keyPressEvent(self, event):
        curKey = event.key()
        print("按下：" + str(event.key()))
        if curKey == Qt.Key_F3:
            self.switch_navigate_window_state(True)
        elif curKey == Qt.Key_Return:
            self.on_pb_query_clicked()

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


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = kdPythonAPIViewer()
    win.show()
    sys.exit(app.exec_())

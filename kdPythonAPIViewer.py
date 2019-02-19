# coding: utf-8
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, QFile, QTextCodec
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QWidget
import os
import sys
import webbrowser
#~ from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from fileutil import check_and_create, check_and_create_dir
from pydocc import Helper


class kdPythonAPIViewer(QWidget):
    def __init__(self):
        super(kdPythonAPIViewer, self).__init__()
        loadUi("kdPythonAPIViewer.ui", self)
        print(dir(self.cb_text))

        self.helper = Helper(self.tb_result,self.tb_result)



    @pyqtSlot()
    def on_pb_query_clicked(self):
        query_text = str(self.cb_text.currentText())
        print(query_text)
        #~ 导入单个模块
        single_import_flag = query_text.find("from") >=0 and query_text.find(",") <0 and query_text.find("*") <0
        if single_import_flag :
            module_ = query_text.replace("from","").replace("import",".").replace(" ","")
            print(module_)
            #~ help(module_)

            self.helper.help(str(module_))

        #~ 导入多个模块
        self.multi_import_flag = query_text.find("from") >=0 and query_text.find(",") >0 and query_text.find("*") <0
        if self.multi_import_flag :
            module_ = query_text.split("import")
            print(",".join(module_))
            sub_module = str(module_[1]).split(",")
            self.cb_sub_text.clear()
            for m in enumerate(sub_module,1):
                self.cb_sub_text.addItem(str(m).strip())

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = kdPythonAPIViewer()
    win.show()
    sys.exit(app.exec_())

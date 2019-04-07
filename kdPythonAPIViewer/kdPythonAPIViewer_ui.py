# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/bkd/pyqt/kdPythonAPIViewer/kdPythonAPIViewer/kdPythonAPIViewer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from .class_search import class_search

class Ui_main_win(object):
    def setupUi(self, main_win):
        main_win.setObjectName("main_win")
        main_win.resize(1005, 347)
        self.gridLayout = QtWidgets.QGridLayout(main_win)
        self.gridLayout.setObjectName("gridLayout")
        self.tw_catelog = QtWidgets.QTreeWidget(main_win)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tw_catelog.sizePolicy().hasHeightForWidth())
        self.tw_catelog.setSizePolicy(sizePolicy)
        self.tw_catelog.setMinimumSize(QtCore.QSize(200, 0))
        self.tw_catelog.setMaximumSize(QtCore.QSize(520, 16777215))
        self.tw_catelog.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tw_catelog.setAutoScroll(False)
        self.tw_catelog.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tw_catelog.setWordWrap(True)
        self.tw_catelog.setHeaderHidden(True)
        self.tw_catelog.setObjectName("tw_catelog")
        self.tw_catelog.headerItem().setText(0, "1")
        self.tw_catelog.header().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tw_catelog, 2, 0, 4, 1)
        self.cb_library = QtWidgets.QComboBox(main_win)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_library.sizePolicy().hasHeightForWidth())
        self.cb_library.setSizePolicy(sizePolicy)
        self.cb_library.setMaximumSize(QtCore.QSize(250, 16777215))
        self.cb_library.setEditable(True)
        self.cb_library.setObjectName("cb_library")
        self.gridLayout.addWidget(self.cb_library, 1, 0, 1, 1)
        self.tb_result = QtWidgets.QTextBrowser(main_win)
        self.tb_result.setObjectName("tb_result")
        self.gridLayout.addWidget(self.tb_result, 3, 1, 1, 1)
        self.pb_refresh_module = QtWidgets.QPushButton(main_win)
        self.pb_refresh_module.setObjectName("pb_refresh_module")
        self.gridLayout.addWidget(self.pb_refresh_module, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lb_text = QtWidgets.QLabel(main_win)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_text.sizePolicy().hasHeightForWidth())
        self.lb_text.setSizePolicy(sizePolicy)
        self.lb_text.setObjectName("lb_text")
        self.horizontalLayout_2.addWidget(self.lb_text)
        self.le_class = class_search()
        self.le_class.setObjectName("le_class")
        self.horizontalLayout_2.addWidget(self.le_class)
        self.lb_sub_text = QtWidgets.QLabel(main_win)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_sub_text.sizePolicy().hasHeightForWidth())
        self.lb_sub_text.setSizePolicy(sizePolicy)
        self.lb_sub_text.setObjectName("lb_sub_text")
        self.horizontalLayout_2.addWidget(self.lb_sub_text)
        self.cb_sub_text = QtWidgets.QComboBox(main_win)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_sub_text.sizePolicy().hasHeightForWidth())
        self.cb_sub_text.setSizePolicy(sizePolicy)
        self.cb_sub_text.setMinimumSize(QtCore.QSize(200, 0))
        self.cb_sub_text.setMaximumSize(QtCore.QSize(200, 16777215))
        self.cb_sub_text.setEditable(True)
        self.cb_sub_text.setObjectName("cb_sub_text")
        self.horizontalLayout_2.addWidget(self.cb_sub_text)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lb_search = QtWidgets.QLabel(main_win)
        self.lb_search.setObjectName("lb_search")
        self.horizontalLayout.addWidget(self.lb_search)
        self.le_search = QtWidgets.QLineEdit(main_win)
        self.le_search.setToolTip("")
        self.le_search.setStatusTip("")
        self.le_search.setWhatsThis("")
        self.le_search.setObjectName("le_search")
        self.horizontalLayout.addWidget(self.le_search)
        self.pb_query = QtWidgets.QPushButton(main_win)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_query.sizePolicy().hasHeightForWidth())
        self.pb_query.setSizePolicy(sizePolicy)
        self.pb_query.setObjectName("pb_query")
        self.horizontalLayout.addWidget(self.pb_query)
        self.lb_display = QtWidgets.QLabel(main_win)
        self.lb_display.setObjectName("lb_display")
        self.horizontalLayout.addWidget(self.lb_display)
        self.rb_all = QtWidgets.QRadioButton(main_win)
        self.rb_all.setObjectName("rb_all")
        self.horizontalLayout.addWidget(self.rb_all)
        self.rb_class = QtWidgets.QRadioButton(main_win)
        self.rb_class.setChecked(True)
        self.rb_class.setObjectName("rb_class")
        self.horizontalLayout.addWidget(self.rb_class)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)

        self.retranslateUi(main_win)
        QtCore.QMetaObject.connectSlotsByName(main_win)

    def retranslateUi(self, main_win):
        _translate = QtCore.QCoreApplication.translate
        main_win.setWindowTitle(_translate("main_win", "kdPythonAPI查看器"))
        self.tb_result.setHtml(_translate("main_win", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">快捷键</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">F2:选择库</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">F3:搜索类</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">F4:选择方法与属性</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">F5:搜索API正文</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">F6:最小化窗口</p></body></html>"))
        self.pb_refresh_module.setText(_translate("main_win", "缓存Python库"))
        self.lb_text.setText(_translate("main_win", "类     "))
        self.lb_sub_text.setText(_translate("main_win", "方法与属性"))
        self.lb_search.setText(_translate("main_win", "正文"))
        self.pb_query.setText(_translate("main_win", "查询"))
        self.lb_display.setText(_translate("main_win", "显示对象"))
        self.rb_all.setText(_translate("main_win", "模块与类"))
        self.rb_class.setText(_translate("main_win", "类"))


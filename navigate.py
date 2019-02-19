# -*- coding:utf-8 -*-

import os
import re
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QDialog


class navigate(QDialog):
    """  """

    find_word_signal = pyqtSignal(str)
    show_key_press_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        loadUi("navigate.ui", self)
        # ~ self.config_path = os.environ['HOME'] + ".config/kdssh/"
        self.nav_tree = (
            "Method resolution order",
            "Methods defined here",
            "Data and other attributes defined here",
        )
        self.inherited_method = "Methods inherited from {}"
        self.inherited_data = "Data descriptors inherited from {}"
        self.lw_catelog.itemClicked.connect(self.on_lw_catelog_itemClicked)

    # ~ 输入框回车后在API文档中查找对应的关键字
    @pyqtSlot()
    def on_le_search_returnPressed(self):
        self.find_word_signal.emit(self.le_search.text())

    @pyqtSlot()
    def on_lw_catelog_itemClicked(self):
        print("选中:" + self.lw_catelog.currentItem().text())
        self.find_word_signal.emit(self.lw_catelog.currentItem().text())

    def keyPressEvent(self, event):
        curKey = event.key()
        if curKey == Qt.Key_F3:
            self.show_key_press_signal.emit(False)

    def init_catelog(self, html_doc):
        self.lw_catelog.clear()
        for nav_tree_item in self.nav_tree:
            self.lw_catelog.addItem(nav_tree_item)
        print(html_doc)
        if html_doc:
            inherit_total = re.search(
                r"(?<=Method resolution order)[\s\S]+?(?=Methods defined here)",
                html_doc,
            )[0]
            print(inherit_total)
            if inherit_total:
                inherit_single = re.findall(r"(?<=\">)[\s\S]+?(?=</a>)", inherit_total)
                if inherit_single:
                    for single in inherit_single:
                        # ~ if re.search(self.inherited_method.format(single),html_doc):
                        self.lw_catelog.addItem(self.inherited_method.format(single))
                        # ~ if re.match(self.inherited_data.format(single),html_doc):
                        self.lw_catelog.addItem(self.inherited_data.format(single))
                        print(
                            single,
                            re.search(self.inherited_method.format(single), html_doc),
                        )

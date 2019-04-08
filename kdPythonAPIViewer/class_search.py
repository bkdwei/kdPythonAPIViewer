'''
Created on 2019年4月6日

@author: bkd
'''
from PyQt5.QtCore import  Qt, QPoint,QSize, pyqtSignal
from PyQt5.QtWidgets import  QLineEdit,QListWidget,QSizePolicy,QListWidgetItem

class class_search(QLineEdit):
        get_api_doc_signal = pyqtSignal(str)
        def __init__(self):
            super().__init__()
            
#             设置下拉列表的属性
            sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            p = self.geometry()
            self.lv_class = QListWidget()
            self.lv_class.setParent(self)
            self.lv_class.setAttribute(Qt.WA_ShowWithoutActivating)
            self.lv_class.setSizePolicy(sizePolicy)
            self.lv_class.setFixedSize(QSize(500,500))
            self.lv_class.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            
            self.textChanged.connect(self.on_le_class_currentTextChanged)
            
            self.adding_lv_class_flag = False
            
        def on_le_class_currentTextChanged(self):
            cur_class = self.text()
            if len(cur_class) < 3:
                return
            
#             self.lv_class.setFixedSize(QSize(500,500))
            p = self.geometry()
            self.lv_class.move(QPoint(p.x(),p.y()+50))
            
            result_list = []
            for c in self.class_list :
                if cur_class.lower() in c["name"].lower() :
                    result_list.append(c)
            self.popup_class_search_result(result_list)
        
#         弹出类的索引列表
        def popup_class_search_result(self,result_list):
            path_list = [item["path"] for item in result_list]
            if path_list:
                self.lv_class.setVisible(True)
                self.adding_lv_class_flag = True
                self.lv_class.clear()

#             弹窗默认选中空白项，避免on_lv_class_currentItemChanged总是莫名选中选中第一项的bug
                blank_item = QListWidgetItem("");
                self.lv_class.addItem(blank_item)
                self.lv_class.setCurrentItem(blank_item)
                
                self.lv_class.addItems(path_list)
                self.adding_lv_class_flag = False
        
#         查询选中的类的文档    
        def get_doc(self):
            if not self.adding_lv_class_flag :
                cur_item= self.lv_class.currentItem()
#                 print("previous",previous.text())
#                 if not cur_item :
#                     print("currentText",self.lv_class.currentText())
                if cur_item and cur_item.text() != "" :
                    print("cur_item.text():" + cur_item.text())
                    self.get_api_doc_signal.emit(cur_item.text())
#                 self.lv_class.setFixedSize(QSize(500,0))
                self.lv_class.setVisible(False)
        
        def keyReleaseEvent(self, event):
            key = event.key()
            if key  == Qt.Key_Down :
                self.lv_class.setCurrentRow(self.lv_class.currentRow() + 1)
            elif key  == Qt.Key_Up :
                self.lv_class.setCurrentRow(self.lv_class.currentRow() - 1)
            elif key  == Qt.Key_Home :
                self.lv_class.setCurrentRow(1)
            elif key  == Qt.Key_End :
                self.lv_class.setCurrentRow(self.lv_class.count()-1)
            elif key  == Qt.Key_PageUp :
                row = self.lv_class.currentRow() - 5
                if row > -1 :
                    self.lv_class.setCurrentRow(row)
            elif key  == Qt.Key_PageDown :
                row = self.lv_class.currentRow() + 5
                if row < self.lv_class.count()  :
                    self.lv_class.setCurrentRow(row)
            elif key  == Qt.Key_Right or key == Qt.Key_Return :
                self.get_doc()
            elif key == Qt.Key_Escape :
                self.lv_class.setVisible(False)
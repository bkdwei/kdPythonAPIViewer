#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from os import  path
import sys
import json
import inspect
import pkgutil
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import  QWidget,QTreeWidgetItem,QApplication
from PyQt5.QtGui import QTextDocument, QTextCursor,QIcon
from .fileutil import config_file,check_and_create,class_file
from .pydocc import Helper,resolve
from .kdPythonAPIViewer_ui import Ui_main_win
from kdDesktopAssistant.fileutil import get_file_realpath
from numpy.core.setup_common import get_api_versions

class kdPythonAPIViewer(QWidget,Ui_main_win):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
#         self.setWindowIcon(QIcon("logo.jpg"))
        self.setWindowIcon(QIcon(get_file_realpath("logo.png")))
#         获取API文档的类
        self.helper = Helper()

#       一个库对应一个list,list包含该库下的所有类
        self.package_map = {}
#         指定库的类列表,单独放到class_search类中好控制
        self.le_class.class_list = []
#         控制新增库的时候，不触发组合下拉框的itemIndexChange事件
        self.adding_library_flag = True
        self.main_module = None
        self.adding_class_flag  =False
        
#         加载系统已安装的库
        self.load_dict()
        self.load_package_map()
        
#         关联界面元素的事件
        self.le_search.returnPressed.connect(self.on_le_search_returnPressed)
        self.cb_sub_text.currentTextChanged.connect(self.on_cb_sub_text_currentIndexChanged)
        
        self.le_class.get_api_doc_signal.connect(self.on_lv_class_seleted)

#         悬浮置顶按钮
#         self.show_status = True
#         self.float_btn = QPushButton("kdPythonAPIViewer")
#         self.float_btn.setWindowFlags(Qt.WindowStaysOnTopHint)
#         self.float_btn.clicked.connect(self.show_window)
#         self.float_btn.show()
        
#     加载系统的已安装的python库，如果缓存文件存在，则直接从缓存文件获取
    def load_dict(self):
        if not path.exists(config_file) :
            self.on_pb_refresh_module_clicked()
        else :
            with open(config_file, "r",encoding="utf-8") as f:
                content = f.read().strip()
                if content != "" :
                    jcontent = json.loads(content)
#                   加载模块时不触发cb_module的currentIndexChanged事件
                    self.adding_library_flag = True
#                     默认不选中任何包
                    self.cb_library.addItem("")
                    self.cb_library.addItems(jcontent)
                    self.adding_library_flag = False

#     加载缓存过的库的类列表                
    def load_package_map(self):
        if path.exists(class_file) :
            with open(class_file, "r",encoding="utf-8") as f:
                content = f.read().strip()
                if content != "" :
                    self.package_map = json.loads(content)

#   选中某一个包时,加载包下的所有模块
#     @pyqtSlot()
    def on_cb_library_currentIndexChanged(self):
        cur_module = self.cb_library.currentText()
        if not self.adding_library_flag and not  cur_module in self.package_map.keys():
            print("首次加载库")
            self.le_class.class_list.clear()
            children =self.get_children(cur_module)
#             更新左侧界面树
            self.fillWidget(children)
#             放到内存
            for c in children :
                self.get_class_recursive(cur_module + "." + c)
            
#             self.tb_result.append("即使加载库异常，也不影响正常使用")
#             self.tb_result.moveCursor(QTextCursor.End)
            
#             更新当前包的遍历结果到文件
            package_item ={cur_module:self.le_class.class_list}
            self.package_map.update(package_item)
            check_and_create(config_file)
            with open(class_file,"w") as f:
                f.write(json.dumps(self.package_map))
        elif hasattr(self,"package_map") and hasattr(self.le_class,"class_list") and cur_module != "":
                self.le_class.class_list = self.package_map[cur_module]
                children =self.get_children(cur_module)
                self.fillWidget(children)
        print("self.le_class.class_list:", self.le_class.class_list)
        
#     初始化左侧树状库的根部
    def fillWidget(self, value):
        self.tw_catelog.clear()
        self.fillItem(self.tw_catelog.invisibleRootItem(), value)
        
#   渲染左侧树状库的子节点
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
#     单击指定的包
    def on_tw_catelog_itemClicked(self):
        cur_item = self.tw_catelog.currentItem()
#         没有选中任何模块时，默认选中库
        if not cur_item :
            cur_item = self.cb_library.currentText()
            self.get_api_doc(cur_item)
            return
            
        fullpath = self.get_fullpath_of_treeitem(cur_item,cur_item.text(0))
        children = self.get_children(fullpath)
        if cur_item.childCount() == 0 :
            self.fillItem(cur_item,children)
        else :
            cur_item.setExpanded(not cur_item.isExpanded())

    @pyqtSlot()
    def on_rb_all_clicked(self):
        self.on_tw_catelog_itemClicked()

#     刷新系统的模块列表，并存入到dict.dat文件，加入程序的启动速度
    @pyqtSlot()
    def on_pb_refresh_module_clicked(self):
        self.tb_result.append("正在加载系统已安装的Python库。。。")
        self.tb_result.moveCursor(QTextCursor.End)
        
        modules  =self.helper.listmodules()
        self.adding_library_flag = True
        self.cb_library.clear()
        self.cb_library.addItems(modules)
        self.adding_library_flag = False
        
        check_and_create(config_file)
        with open(config_file,"w+") as f:
            f.write(json.dumps(modules))
        self.tb_result.append("加载结束")
        self.tb_result.moveCursor(QTextCursor.End)
        
#         清空类的缓存，防止缓存类出错的现象
        with open(class_file,"w") as f:
            pass

#     @pyqtSlot()
    def on_cb_sub_text_currentIndexChanged(self):
        if not self.adding_item_flag :
            cur_item = self.cb_sub_text.currentText()
            if self.main_module:
                try:
                    module_ = self.main_module + "." + cur_item
                    self.get_api_doc(str(module_))
                except Exception:
                    if not 'A' <= cur_item[0] <= 'Z':
                        cur_item = cur_item +"(...)" 
                    if not self.tb_result.find(cur_item):
                        self.tb_result.moveCursor(QTextCursor.Start)
                        find_result = self.tb_result.find(cur_item)
                        print(find_result)
            else:
                if not 'A' <= cur_item[0] <= 'Z':
                    cur_item = cur_item +"(...)" 
                if not self.tb_result.find(cur_item):
                    self.tb_result.moveCursor(QTextCursor.Start)
                    find_result = self.tb_result.find(cur_item)
                    print(find_result)

    def on_lv_class_seleted(self,module_):
        self.get_api_doc(str(module_))
        resolved_object, _ = resolve(module_, 0)
        final_items = []
        methods  = dir(resolved_object)
        for b in methods :
            if not b.startswith("__"):
                final_items.append(b)
        if final_items :
            sorted(final_items)        
            self.adding_item_flag = True
            self.cb_sub_text.clear()
            self.cb_sub_text.addItems(final_items)
            self.adding_item_flag = False
        
#     查询指定模块或包的API文档
    def get_api_doc(self, module_):
        doc = self.helper.help(str(module_))
        self.tb_result.setHtml(doc)
    
#     拦截快捷键
    def keyPressEvent(self, event):
        curKey = event.key()
        # ~ print("按下：" + str(event.key()))
        if curKey == Qt.Key_F2:
            self.cb_library.setFocus()
#             self.cb_library.showPopup()
        elif curKey == Qt.Key_F3:
            self.le_class.setFocus()
            self.le_class.selectAll()
        elif curKey == Qt.Key_F4:
            self.cb_sub_text.setFocus()
            self.cb_sub_text.showPopup()
        elif curKey == Qt.Key_F5:
            self.le_search.setFocus()
            self.le_search.selectAll()
        elif curKey == Qt.Key_F6:
            self.showMinimized()
    
    def find(self, keyword):
        # ~ 先向下查找,没有结果则向上查找，貌似不会往回查询
        if not self.tb_result.find(keyword):
            self.tb_result.find(keyword, QTextDocument.FindBackward)

#     获取模块完整的包路径
    def get_fullpath_of_treeitem(self,item,path):
        parent = item.parent()
        if parent is None:
            cur_module = self.cb_library.currentText()
            return cur_module + "." + path
        else:
            return self.get_fullpath_of_treeitem(parent,parent.text(0) + "." + path)

#     获取指定包下的子包或模块
    def get_children(self, path):
        children = []
        resolved_object, _ = resolve(path, 0)
        if inspect.ismodule(resolved_object):
#             print("is module")
            if self.rb_all.isChecked():
                self.get_api_doc(path)
            if hasattr(resolved_object, '__path__'):
                names = [name  for _, name, _ in pkgutil.iter_modules(resolved_object.__path__)]
#                 print("names:",names)
                children +=names
            else:
                # ~ modules = inspect.getmembers(resolved_object, inspect.ismodule)
                modules = inspect.getmembers(resolved_object, inspect.isclass)
                # ~ print("modules",modules)
                children +=[m[0] for m in modules]
        if inspect.isclass(resolved_object):
#             print("is class")
            final_items = []
            methods  = dir(resolved_object)
            for b in methods :
                if not b.startswith("__"):
                    final_items.append(b)
            sorted(final_items)        
            self.adding_item_flag = True
            self.cb_sub_text.addItems(final_items)
#             self.cb_sub_text.showPopup()
            self.adding_item_flag = False
            
            self.get_api_doc(path)
            # ~ children.append(inspect.getmembers(PyQt5, inspect.ismodule))
        if inspect.isroutine(resolved_object):
            print("is routine")
        return children

#     获取指定包下的所有类
    def get_class_recursive(self, path):
        try :
            resolved_object, resolve_name = resolve(path, 0)
        except Exception as e:
            print("忽略加载异常，库：{}，异常详情：{}".format(path,str(e)))
#             self.tb_result.append("忽略加载异常，库：{}，异常详情：{}".format(path,str(e)))
#             self.tb_result.moveCursor(QTextCursor.End)
            return
        children = []
        if inspect.ismodule(resolved_object):
            if hasattr(resolved_object, '__path__'):
                names = [name  for _, name, _ in pkgutil.iter_modules(resolved_object.__path__)]
#                 print("names:",names)
                children +=names
                print("children has  path:" ,path)
                for c in names :
                    self.get_class_recursive(path + "." + c)
            else:
                # ~ modules = inspect.getmembers(resolved_object, inspect.ismodule)
                modules = inspect.getmembers(resolved_object, inspect.isclass)
                # ~ print("modules",modules)
                children +=[{"name":m[0],"path":path + "." + m[0]} for m in modules]
                print("children has not path:" , path)
                self.le_class.class_list += children
        if inspect.isclass(resolved_object):
            print("add single class",{"name":resolve_name,"path":path})
            self.le_class.class_list.append({"name":resolve_name,"path":path})


    @pyqtSlot()
    def on_pb_query_clicked(self):
        self.on_le_search_returnPressed()
        
    # ~ 输入框回车后在API文档中查找对应的关键字
    @pyqtSlot()
    def on_le_search_returnPressed(self):
        # ~ 先向下查找,没有结果则向上查找
        keyword = self.le_search.text()
        if not self.tb_result.find(keyword) :
            self.tb_result.find(keyword, QTextDocument.FindBackward)
    
 
        
#     def show_window(self):
#         self.show_status = not self.show_status
#         self.setVisible(self.show_status)
    
def main():
    app = QApplication(sys.argv)
    win = kdPythonAPIViewer()
    win.showMaximized()
#     win.show()
#     win.cb_library.showPopup()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
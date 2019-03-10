#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages
        
with open("kdPythonAPIViewer/README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

# see https://packaging.python.org/tutorials/packaging-projects/
setup(
#     固定部分
    name="kdPythonAPIViewer",
    version="1.0.5",
    author="bkdwei",
    author_email="bkdwei@163.com",
    maintainer="韦坤东",
    maintainer_email="bkdwei@163.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bkdwei/kdPythonAPIViewer",
    license="GPLv3+",
    platforms=["Windows", "Linux"],
    setup_requires=["shortcutter"],
#     需要安装的依赖
    install_requires=["PyQt5"],
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,

#     可变部分
    description="an Python API viewer,query python module's method and attribute.",
    keywords=("API","viewer","module","method"),
#   see  https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Developers",
        "Natural Language :: Chinese (Simplified)",
        "Topic :: Internet :: File Transfer Protocol (FTP)",
        "Programming Language :: Python :: 3",
        " License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows"
    ],
    
     # 添加这个选项，在windows下Python目录的scripts下生成exe文件
     # 注意：模块与函数之间是冒号:
    entry_points={
        'console_scripts': [
            'kdPythonAPIViewer=kdPythonAPIViewer.kdPythonAPIViewer:main'
        ],    
    }
)
print("正在使用shortcutter创建快捷方式和开始菜单")
from shortcutter import ShortCutter
sc = ShortCutter()
sc.create_desktop_shortcut("kdPythonAPIViewer")
sc.create_menu_shortcut("kdPythonAPIViewer")
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project: nii_slice_tool
# @File  : main
# @Author: super
# @Date  : 2021/5/19

import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
"""
    GUI启动入口
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())


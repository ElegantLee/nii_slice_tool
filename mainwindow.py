# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project: nii_slice_tool
# @File  : mainwindow
# @Author: super
# @Date  : 2021/5/19

import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.Qt import QThread, QMutex, pyqtSignal
from uiMainwindow import Ui_MainWindow

class SliceThread(QThread):

    def __init__(self):
        super(SliceThread, self).__init__()

    def run(self):

        pass

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.getcwd()
        self.output_path = {'coronal': 'D:/', 'axial': 'D:/', 'sagittal': 'D:/'}       # 输出文件的路径列表

        """ 按钮对应的逻辑函数"""
        # 点击open
        self.action_open.triggered.connect(self.open_file)
        # 点击open folder
        self.action_open_Folder.triggered.connect(self.open_folder)
        # 点击coronal的输出文件夹
        self.coronal_path_toolButton.clicked.connect(self.set_coronal_path)
        # 点击axial的输出文件夹
        self.axial_path_toolButton.clicked['bool'].connect(self.set_axial_path)
        # 点击sagittal的输出文件夹
        self.sagittal_path_toolButton.clicked.connect(self.set_sagittal_path)
        # 点击slice button后，更新进度条
        self.slice_button.clicked.connect(self.do_slice)
        # 点击slice button后，更新log
        # self.slice_button.clicked.connect(self.log_textEdit)

    # option---open---打开单个nii文件
    def open_file(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, caption='Open a nii file',
                                                           directory=self.cwd, filter="nii files (*.nii)")

        self.filename_lineEdit.setText(file_name)

    # option---open folder---打开一个文件夹
    def open_folder(self):
        file_dir = QFileDialog.getExistingDirectory(self, caption='open a directory',
                                                    directory='D:/')
        self.folder_path_lineEdit.setText(file_dir)

    # 设置冠状切片的输出路径
    def set_coronal_path(self):
        dir = QFileDialog.getExistingDirectory(self, 'set coronal slice output path', directory='D:/')
        self.output_path['coronal'] = dir
        self.coronal_path_lineEdit.setText(dir)

    # 设置水平切片的输出路径
    def set_axial_path(self):
        dir = QFileDialog.getExistingDirectory(self, 'set axial slice output path', directory='D:/')
        self.output_path['axial'] = dir
        self.axial_path_lineEdit.setText(dir)

    # 设置矢状切片的输出路径
    def set_sagittal_path(self):
        dir = QFileDialog.getExistingDirectory(self, 'set sagittal slice output path', directory='D:/')
        self.output_path['sagittal'] = dir
        print(self.output_path)
        self.sagittal_path_lineEdit.setText(dir)

    # 启动切片---切片的主要逻辑
    def do_slice(self):

        pass



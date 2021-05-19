# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project: nii_slice_tool
# @File  : mainwindow
# @Author: super
# @Date  : 2021/5/19

import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from uiMainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.getcwd()

        """ 按钮对应的逻辑函数"""
        # 点击open
        self.action_open.triggered.connect(self.open_file)
        # 点击open folder
        self.action_open_Folder.triggered.connect(self.open_folder)
        # 点击coronal的输出文件夹
        self.coronal_path_toolButton.clicked.connect(self.coronal_path_lineEdit.clear)
        # 点击axial的输出文件夹
        self.axial_path_toolButton.clicked['bool'].connect(self.axial_path_lineEdit.clear)
        # 点击sagittal的输出文件夹
        self.sagittal_path_toolButton.clicked.connect(self.sagittal_path_lineEdit.clear)
        # 点击slice button后，更新进度条
        self.slice_button.clicked.connect(self.process_progressBar.reset)
        # 点击slice button后，更新log
        # self.slice_button.clicked.connect(self.log_textEdit)

    def open_file(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, caption='Open a nii file',
                                                           directory=self.cwd, filter="nii files (*.nii)")

        self.filename_lineEdit.setText(file_name)

    def open_folder(self):
        file_dir = QFileDialog.getExistingDirectory(self, caption='open a directory',
                                                    directory='D:/')
        self.folder_path_lineEdit.setText(file_dir)

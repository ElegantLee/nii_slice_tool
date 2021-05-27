# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project: nii_slice_tool
# @File  : mainwindow
# @Author: super
# @Date  : 2021/5/19

import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QTextCursor
from uiMainwindow import Ui_MainWindow
from updateProgressBarThread import UpdateProgressBarThread
from updateLogThread import UpdateLogThread


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.getcwd()
        self.input_file = ''
        self.input_folder = ''
        self.output_path = {'coronal': 'D:/', 'axial': 'D:/', 'sagittal': 'D:/', 'all': 'D:/'}  # 输出文件的路径列表
        self.output_folder = ''
        self.direction = 'axial'
        self.rotate = 'Yes'
        self.rotate_num = 90
        self.update_progressBar_thread = None
        self.update_log_thread = None

        """ 按钮对应的逻辑函数"""
        # 点击open
        self.action_open.triggered.connect(self.open_file)
        # 点击open folder
        self.action_open_Folder.triggered.connect(self.open_folder)
        # 点击coronal的输出文件夹
        self.coronal_path_toolButton.clicked.connect(self.set_coronal_path)
        # 点击axial的输出文件夹
        self.axial_path_toolButton.clicked.connect(self.set_axial_path)
        # 点击sagittal的输出文件夹
        self.sagittal_path_toolButton.clicked.connect(self.set_sagittal_path)
        # 点击all的输出文件夹
        self.all_path_toolButton.clicked.connect(self.set_all_path)
        # 点击slice button后，更新进度条
        self.slice_button.clicked.connect(self.do_slice)
        # 选择切片方向
        self.slice_option_comboBox.activated[str].connect(self.select_slice_direction)
        # 选择是否旋转图像
        self.rotate_comboBox.activated[str].connect(self.select_rotate)
        # 选择旋转的角度
        self.rotate_num_comboBox.currentIndexChanged.connect(self.select_rotate_num)

    def __str__(self):
        return "input_file:%s\ninput_folder:%s\noutput_path:%s\ndirection:%s\nrotate:%s\nrotate_num:%d\n" \
               % (self.input_file, self.input_folder, self.output_path, self.direction, self.rotate, self.rotate_num)

    # option---open---打开单个nii文件
    def open_file(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, caption='Open a nii file',
                                                           directory=self.cwd, filter="nii files (*.nii)")
        self.input_file = file_name
        self.filename_lineEdit.setText(file_name)

    # option---open folder---打开一个文件夹
    def open_folder(self):
        file_dir = QFileDialog.getExistingDirectory(self, caption='open a directory',
                                                    directory='D:/')
        self.input_folder = file_dir
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

    # 设置all方向的输出路径
    def set_all_path(self):
        dir = QFileDialog.getExistingDirectory(self, 'set all direction slice output path', directory='D:/')
        self.output_folder = dir
        print(dir)
        self.all_path_lineEdit.setText(dir)

    # 选择切片方向
    def select_slice_direction(self, direction):
        self.direction = direction
        print(self.direction)

    # 选择是否旋转图像
    def select_rotate(self, rotate):
        self.rotate = rotate
        print(self.rotate)

    # 选择旋转角度
    def select_rotate_num(self):
        self.rotate_num = int(self.rotate_num_comboBox.currentText())
        print(type(self.rotate_num), self.rotate_num)

    # 启动切片---切片的主要逻辑
    def do_slice(self):
        # slice_thread_test = SliceThread(self.input_file, self.output_path[self.direction], self.direction,
        #                                 self.rotate, self.rotate_num, self.process_progressBar)
        # slice_thread_test.start()
        # slice_thread_test.finish_signal.connect(self.get_msg)
        self.log_textEdit.clear()
        self.update_log_thread = UpdateLogThread()
        self.update_progressBar_thread = UpdateProgressBarThread(input_file=self.input_file,
                                                                 input_folder=self.input_folder,
                                                                 output_path=self.output_path[self.direction],
                                                                 output_folder=self.output_folder,
                                                                 direction=self.direction, rotate=self.rotate,
                                                                 rotate_num=self.rotate_num,
                                                                 update_log_thread=self.update_log_thread)
        self.update_progressBar_thread.start()

        self.update_progressBar_thread.update_progress_signal.connect(self.update_progressBar)
        self.update_log_thread.update_log_signal.connect(self.update_log)

    def update_log(self, msg):
        self.log_textEdit.append(msg)
        self.log_textEdit.moveCursor(QTextCursor.End)

    def update_progressBar(self, progress_counter):
        self.process_progressBar.setValue(progress_counter)

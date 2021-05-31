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
from dicom2niiThread import Dicom2Nii

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.getcwd()
        self.input_nii_file = ''
        self.input_dicom_file = []
        self.input_nii_folder = ''
        self.input_dicom_folder = ''
        self.output_path = {'coronal': 'D:/', 'axial': 'D:/', 'sagittal': 'D:/', 'all': 'D:/'}  # 输出文件的路径列表
        self.output_nii_folder = ''
        self.output_dicom_folder = ''
        self.direction = 'axial'
        self.rotate = 'Yes'
        self.rotate_num = 90
        self.dataset = 'ADNI'
        self.update_progressBar_thread = None
        self.update_log_thread = None
        self.dicom2nii_thread = None

        """ 按钮对应的逻辑函数"""
        # 点击open nii file
        self.action_nii_file.triggered.connect(self.open_nii_file)
        # 点击open dicom file
        self.action_dicom_file.triggered.connect(self.open_dicom_file)
        # 点击open nii folder
        self.action_nii_folder.triggered.connect(self.open_nii_folder)
        # 点击open dicom folder
        self.action_dicom_folder.triggered.connect(self.open_dicom_folder)
        # 点击coronal的输出文件夹
        self.coronal_path_toolButton.clicked.connect(self.set_coronal_path)
        # 点击axial的输出文件夹
        self.axial_path_toolButton.clicked.connect(self.set_axial_path)
        # 点击sagittal的输出文件夹
        self.sagittal_path_toolButton.clicked.connect(self.set_sagittal_path)
        # 点击all的输出文件夹
        self.all_path_toolButton.clicked.connect(self.set_all_path)
        # 选择切片方向
        self.direction_comboBox.activated[str].connect(self.select_slice_direction)
        # 选择是否旋转图像
        self.rotate_comboBox.activated[str].connect(self.select_rotate)
        # 选择旋转的角度
        self.rotate_num_comboBox.currentIndexChanged.connect(self.select_rotate_num)
        # 选择数据集
        self.dataset_comboBox.currentIndexChanged.connect(self.select_dataset)
        # 点击slice button后，更新进度条和日志
        self.slice_button.clicked.connect(self.do_slice)
        # 点击convert button
        self.convert_pushButton.clicked.connect(self.do_convert)

    def __str__(self):
        return "input_file:%s\ninput_folder:%s\noutput_path:%s\ndirection:%s\nrotate:%s\nrotate_num:%d\n" \
               % (self.input_file, self.input_folder, self.output_path, self.direction, self.rotate, self.rotate_num)

    # option---open---打开单个nii文件
    def open_nii_file(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, caption='Open a nii file',
                                                           directory=self.cwd, filter="nii files (*.nii)")
        self.input_nii_file = file_name
        self.nii_folder_lineEdit.clear()
        self.input_nii_folder = ''
        self.nii_file_lineEdit.setText(file_name)

    # 打开一个dicom文件
    def open_dicom_file(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, caption='Open a dicom file',
                                                           directory=self.cwd, filter="dicom files (*.dcm)")
        self.input_dicom_file.append(file_name)
        self.dicom_folder_lineEdit.clear()
        self.input_dicom_folder = []
        self.dicom_file_lineEdit.setText(file_name)

    # option---open folder---打开一个nii文件夹
    def open_nii_folder(self):
        file_dir = QFileDialog.getExistingDirectory(self, caption='open a nii directory',
                                                    directory='D:/')
        self.input_nii_folder = file_dir
        self.nii_folder_lineEdit.setText(file_dir)
        self.nii_file_lineEdit.clear()
        self.input_nii_file = ''

    # 打开一个dicom文件夹
    def open_dicom_folder(self):
        file_dir = QFileDialog.getExistingDirectory(self, caption='open a dicom directory',
                                                    directory='D:/')
        self.input_dicom_folder = file_dir
        self.dicom_folder_lineEdit.setText(file_dir)
        # self.dicom_file_lineEdit.clear()
        # self.input_dicom_file = []

    # 设置冠状切片的输出路径
    def set_coronal_path(self):
        dir = QFileDialog.getExistingDirectory(self, 'set coronal slice output path', directory='D:/')
        self.output_path['coronal'] = dir
        self.coronal_path_lineEdit.setText(dir)
        self.axial_path_lineEdit.clear()
        self.sagittal_path_lineEdit.clear()
        self.all_path_lineEdit.clear()

    # 设置水平切片的输出路径
    def set_axial_path(self):
        dir = QFileDialog.getExistingDirectory(self, 'set axial slice output path', directory='D:/')
        self.output_path['axial'] = dir
        self.axial_path_lineEdit.setText(dir)
        self.coronal_path_lineEdit.clear()
        self.sagittal_path_lineEdit.clear()
        self.all_path_lineEdit.clear()

    # 设置矢状切片的输出路径
    def set_sagittal_path(self):
        dir = QFileDialog.getExistingDirectory(self, 'set sagittal slice output path', directory='D:/')
        self.output_path['sagittal'] = dir
        print(self.output_path)
        self.sagittal_path_lineEdit.setText(dir)
        self.axial_path_lineEdit.clear()
        self.coronal_path_lineEdit.clear()
        self.all_path_lineEdit.clear()

    # 设置all方向的输出路径
    def set_all_path(self):
        dir = QFileDialog.getExistingDirectory(self, 'set all direction slice output path', directory='D:/')
        self.output_nii_folder = dir
        print(dir)
        self.all_path_lineEdit.setText(dir)
        self.axial_path_lineEdit.clear()
        self.coronal_path_lineEdit.clear()
        self.sagittal_path_lineEdit.clear()

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

    # 选择数据集
    def select_dataset(self):
        self.dataset = self.dataset_comboBox.currentText()
        print(self.dataset)

    # 启动切片---切片的主要逻辑
    def do_slice(self):
        # slice_thread_test = SliceThread(self.input_file, self.output_path[self.direction], self.direction,
        #                                 self.rotate, self.rotate_num, self.process_progressBar)
        # slice_thread_test.start()
        # slice_thread_test.finish_signal.connect(self.get_msg)
        self.log_textEdit.clear()
        self.update_log_thread = UpdateLogThread()
        self.update_progressBar_thread = UpdateProgressBarThread(input_file=self.input_nii_file,
                                                                 input_folder=self.input_nii_folder,
                                                                 output_path=self.output_path[self.direction],
                                                                 output_folder=self.output_nii_folder,
                                                                 direction=self.direction,
                                                                 rotate=self.rotate,
                                                                 rotate_num=self.rotate_num,
                                                                 dataset=self.dataset,
                                                                 update_log_thread=self.update_log_thread)
        self.update_progressBar_thread.start()
        self.update_progressBar_thread.update_progress_signal.connect(self.update_progressBar)
        self.update_log_thread.update_log_signal.connect(self.update_log)

    def do_convert(self):
        self.log_textEdit.clear()
        self.dicom2nii_thread = Dicom2Nii(self.input_dicom_folder, self.output_dicom_folder)
        self.dicom2nii_thread.start()
        self.dicom2nii_thread.dicom2nii_signal.connect(self.update_log)

    def update_log(self, msg):
        self.log_textEdit.append(msg)
        self.log_textEdit.moveCursor(QTextCursor.End)

    def update_progressBar(self, progress_counter):
        self.process_progressBar.setValue(progress_counter)

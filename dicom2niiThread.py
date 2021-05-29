# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project: nii_slice_tool
# @File  : dicom2niiThread
# @Author: superlee
# @Date  : 2021/5/29

from PyQt5.QtCore import QThread, QMutex, pyqtSignal
import dicom2nifti

class Dicom2Nii(QThread):

    def __init__(self, input_dicom_file, input_dicom_folder, output_dicom_folder):
        super(Dicom2Nii, self).__init__()
        self.input_dicom_file = input_dicom_file
        self.input_dicom_folder = input_dicom_folder
        self.output_dicom_folder = output_dicom_folder

    def run(self):
        dicom2nifti.dicom_series_to_nifti(self.input_dicom_file, output_file, reorient_nifti=True)

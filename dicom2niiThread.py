# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project: nii_slice_tool
# @File  : dicom2niiThread
# @Author: superlee
# @Date  : 2021/5/29

import os
import dicom2nifti
from dicom2nifti.compressed_dicom import is_dicom_file
from pathlib import Path
from PyQt5.QtCore import QThread, QMutex, pyqtSignal


class Dicom2Nii(QThread):
    dicom2nii_signal = pyqtSignal(str, name='the log of convert dicom2nii')

    def __init__(self, input_dicom_folder, output_dicom_folder):
        super(Dicom2Nii, self).__init__()
        self.input_dicom_folder = input_dicom_folder
        self.output_dicom_folder = output_dicom_folder

    def run(self):
        # dicom2nifti.dicom_series_to_nifti(self.input_dicom_file, output_file, reorient_nifti=True)
        for root, dirs, files in os.walk(self.input_dicom_folder):
            root = Path(root).as_posix()
            if len(dirs) == 0 and len(files) != 0:
                if is_dicom_file(Path(os.path.join(root, files[0])).as_posix()):
                    print('the root contains dicom slice')
                    self.dicom2nii_signal.emit('the root contains dicom slice')
                    print('=======================================================')
                    self.dicom2nii_signal.emit('=========================root==============================')
                    print('root: ', root)

                    self.dicom2nii_signal.emit('root: ' + root)
                    print('=======================================================')
                    self.dicom2nii_signal.emit('=============================files==========================')
                    for file in files:
                        print(file)
                        self.dicom2nii_signal.emit(file)
                    print('========================dicom2nii processing===============================')
                    self.dicom2nii_signal.emit('========================dicom2nii processing===============================')
                    dicom2nifti.convert_directory(dicom_directory=root, output_folder=root, compression=False, reorient=True)
                    print('success')
                    self.dicom2nii_signal.emit('success')
                    print('\nthe next path\n')
                    self.dicom2nii_signal.emit('\nthe next path\n')
                else:
                    print('root: %s contains no dicom files!'.format(root))
                    msg = 'root: %s contains no dicom files!'.format(root)
                    self.dicom2nii_signal.emit(msg)
                    print('\nthe next path\n')
                    self.dicom2nii_signal.emit('\nthe next path\n')

        print('all dicom files have been converted to nii files!')
        self.dicom2nii_signal.emit('all dicom files have been converted to nii files!')

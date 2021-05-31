# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project: nii_slice_tool
# @File  : updateProgressBarThread
# @Author: super
# @Date  : 2021/5/25
import shutil
import sys
import os
import time
import math

import imageio
import nibabel
import numpy
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from pathlib import Path


class UpdateProgressBarThread(QThread):
    update_progress_signal = pyqtSignal(int, name='UpdateProgressBar')
    finish_signal = pyqtSignal(bool, name='is finished slicing signal')

    def __init__(self, input_file, input_folder, output_path, output_folder, direction, rotate, rotate_num, dataset, update_log_thread):
        super(UpdateProgressBarThread, self).__init__()
        print('update progressBar thread...')
        self.input_file = input_file
        self.input_folder = input_folder
        self.output_path = output_path
        self.output_folder = output_folder
        self.direction = direction
        self.rotate = rotate
        self.rotate_num = rotate_num
        self.dataset = dataset
        self._mutex = QMutex()
        self.update_log_thread = update_log_thread
        self.counter = 0

    def run(self):
        if self.input_file != '' and self.input_folder == '' and self.direction != 'all':
            self.nii2png_one_direction()
        elif self.input_file != '' and self.input_folder == '' and self.direction == 'all':
            self.nii2png_all_direction()
        elif self.input_file == '' and self.input_folder != '' and self.direction == 'all':
            self.nii2png_all_direction_folder()
        # self.finish_signal.emit('update success')
        return

    def set_rotate_by_direction_num(self, image_array, current_slice):
        if self.rotate_num == 90:
            if self.direction == 'axial':
                data = numpy.rot90(image_array[:, :, current_slice])
            elif self.direction == 'coronal':
                data = numpy.rot90(image_array[:, current_slice, :])
            elif self.direction == 'sagittal':
                data = numpy.rot90(image_array[current_slice, :, :])
            else:
                pass
        elif self.rotate_num == 180:
            if self.direction == 'axial':
                data = numpy.rot90(numpy.rot90(image_array[:, :, current_slice]))
            elif self.direction == 'coronal':
                data = numpy.rot90(numpy.rot90(image_array[:, current_slice, :]))
            elif self.direction == 'sagittal':
                data = numpy.rot90(numpy.rot90(image_array[current_slice, :, :]))
            else:
                pass
        elif self.rotate_num == 270:
            if self.direction == 'axial':
                data = numpy.rot90(numpy.rot90(numpy.rot90(image_array[:, :, current_slice])))
            elif self.direction == 'coronal':
                data = numpy.rot90(numpy.rot90(numpy.rot90(image_array[:, current_slice, :])))
            elif self.direction == 'sagittal':
                data = numpy.rot90(numpy.rot90(numpy.rot90(image_array[current_slice, :, :])))
            else:
                pass
        else:
            if self.direction == 'axial':
                # data = image_array[:, :, current_slice]

                data = numpy.rot90(numpy.rot90(image_array[:, current_slice, :]))

            elif self.direction == 'coronal':
                # data = image_array[:, current_slice, :]
                data = numpy.rot90(numpy.rot90(image_array[current_slice, :, :]))
            elif self.direction == 'sagittal':
                # data = image_array[current_slice, :, :]
                data = numpy.rot90(image_array[:, :, current_slice])
        return data

    def nii2png_one_direction(self):
        output_path_direction = Path(os.path.join(self.output_path, self.direction)).as_posix()
        print('Input file is ', self.input_file)
        print('Output folder is ', self.output_path)
        self.update_log_thread.update_log_signal.emit('Input file is ' + self.input_file)
        self.update_log_thread.update_log_signal.emit('Output folder is ' + self.output_path)

        image_array = nibabel.load(self.input_file).get_data()
        print('len: {}'.format(len(image_array.shape)))
        print('image shape: {}'.format(image_array.shape))
        self.update_log_thread.update_log_signal.emit('len: {}'.format(len(image_array.shape)))
        self.update_log_thread.update_log_signal.emit('image shape: {}'.format(image_array.shape))

        if self.rotate.lower() == 'yes':
            if self.rotate_num == 90 or self.rotate_num == 180 or self.rotate_num == 270:
                print('Got it. Your images will be rotated by {} degrees.'.format(self.rotate_num))
                self.update_log_thread.update_log_signal.emit(
                    'Got it. Your images will be rotated by {} degrees.'.format(self.rotate_num))
            else:
                print('You must enter a value that is either 90, 180, or 270. Quitting...')
                self.update_log_thread.update_log_signal.emit(
                    'You must enter a value that is either 90, 180, or 270. Quitting...')
                sys.exit()
        elif self.rotate.lower() == 'no':
            print('OK, Your images will be converted it as it is.')
            self.update_log_thread.update_log_signal.emit('OK, Your images will be converted it as it is.')
        else:
            print('You must choose either y or n. Quitting...')
            self.update_log_thread.update_log_signal.emit('You must choose either y or n. Quitting...')
            sys.exit()
        shape = 3
        # else if 3D image inputted
        self._mutex.lock()
        if shape == 3:
            # set destination folder
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
                print("Created output directory: " + self.output_path)
                self.update_log_thread.update_log_signal.emit("Created output directory: " + self.output_path)

            if not os.path.exists(output_path_direction):
                os.mkdir(output_path_direction)
                print("Created output-direction directory: " + output_path_direction)
                self.update_log_thread.update_log_signal.emit(
                    "Created output-direction directory: " + output_path_direction)
            print('Reading NIfTI file...')
            self.update_log_thread.update_log_signal.emit('Reading NIfTI file...')
            if self.direction == 'axial':
                total_slices = 230
            elif self.direction == 'coronal':
                total_slices = 240
            elif self.direction == 'sagittal':
                total_slices = 230
            else:
                pass

            # image_array[coronal, axial, Sagittal]  [冠状面，水平面，矢状面]
            slice_counter = 0
            # 映射切片进度
            y_max = 100
            y_min = 1
            x_max = total_slices
            x_min = 1
            progress_counter = 0
            # iterate through slices
            # for current_slice in range(0, total_slices):
            #     # alternate slices
            #     if (slice_counter % 1) == 0:
            #         # rotate or no rotate
            #         time.sleep(1)
            #         # alternate slices and save as png
            #         if (slice_counter % 1) == 0:
            #             # time.sleep(3)
            #             slice_counter += 1
            #             print('Moved.')
            #             self.update_log_thread.update_log_signal.emit('Moved.')
            #         progress_counter = y_min + math.ceil((y_max - y_min) / (x_max - x_min) * (current_slice - x_min))
            #         self.update_progress_signal.emit(progress_counter)
            #         # self.progressBar.setValue = progress_counter

            for current_slice in range(0, total_slices):
                # alternate slices
                if (slice_counter % 1) == 0:
                    # rotate or no rotate
                    if self.rotate.lower() == 'yes':
                        if self.rotate_num == 90 or self.rotate_num == 180 or self.rotate_num == 270:
                            if self.rotate_num == 90:
                                # data = numpy.rot90(image_array[:, :, current_slice])
                                # data = numpy.rot90(image_array[:, current_slice, :])  # T1
                                # [矢状, 冠状, 水平]
                                data = self.set_rotate_by_direction_num(image_array=image_array,
                                                                        current_slice=current_slice)
                            elif self.rotate_num == 180:
                                # data = numpy.rot90(numpy.rot90(image_array[:, :, current_slice]))
                                # data = image_array[:, :, current_slice]  # T2
                                data = self.set_rotate_by_direction_num(image_array=image_array,
                                                                        current_slice=current_slice)
                            elif self.rotate_num == 270:
                                data = self.set_rotate_by_direction_num(image_array=image_array,
                                                                        current_slice=current_slice)
                    elif self.rotate.lower() == 'no':
                        # data = image_array[:, :, current_slice]
                        # data = image_array[:, current_slice, :]  # T1
                        self.rotate_num = 0
                        data = self.set_rotate_by_direction_num(image_array=image_array,
                                                                current_slice=current_slice)

                    # alternate slices and save as png
                    if (slice_counter % 1) == 0:
                        print('Saving image...')
                        self.update_log_thread.update_log_signal.emit('Saving image...')
                        image_name = self.input_file[:-4] + "_" + self.direction + "{:0>3}".format(
                            str(current_slice + 1)) + ".png"
                        self.update_log_thread.update_log_signal.emit(image_name)
                        imageio.imwrite(image_name, data)
                        print('Saved.')
                        self.update_log_thread.update_log_signal.emit('Saved.')

                        # move images to folder
                        print('Moving image...')
                        self.update_log_thread.update_log_signal.emit('Moving image...')
                        src = image_name
                        shutil.move(src, output_path_direction)
                        slice_counter += 1
                        print('Moved.')
                        self.update_log_thread.update_log_signal.emit('Moved.')
                    progress_counter = y_min + math.ceil((y_max - y_min) / (x_max - x_min) * (current_slice - x_min))
                    self.update_progress_signal.emit(progress_counter)
            print('Finished converting images')
            self.update_log_thread.update_log_signal.emit('Finished converting images')
            result = True
        else:
            print('Not a 3D or 4D Image. Please try again.')
            result = False
        self._mutex.unlock()

    def nii2png_all_direction(self):
        if self.output_folder == '':
            self.output_folder = Path(os.path.splitext(self.input_file)[0]).as_posix()
        output_path_axial = Path(os.path.join(self.output_folder, 'axial')).as_posix()
        output_path_coronal = Path(os.path.join(self.output_folder, 'coronal')).as_posix()
        output_path_sagittal = Path(os.path.join(self.output_folder, 'sagittal')).as_posix()
        print('Input file is ', self.input_file)
        print('Output folder is ', self.output_folder)
        print('output axial folder is ', output_path_axial)
        print('output coronal folder is ', output_path_coronal)
        print('output sagittal folder is ', output_path_sagittal)
        self.update_log_thread.update_log_signal.emit('Input file is ' + self.input_file)
        self.update_log_thread.update_log_signal.emit('Output folder is ' + self.output_folder)
        self.update_log_thread.update_log_signal.emit('output axial folder is ' + output_path_axial)
        self.update_log_thread.update_log_signal.emit('output coronal folder is ' + output_path_coronal)
        self.update_log_thread.update_log_signal.emit('output sagittal folder is ' + output_path_sagittal)
        # set fn as your 4d nifti file
        image_array = nibabel.load(self.input_file).get_data()
        print(len(image_array.shape))
        print('image shape: ', image_array.shape)
        self.update_log_thread.update_log_signal.emit('len: {}'.format(len(image_array.shape)))
        self.update_log_thread.update_log_signal.emit('image shape: {}'.format(image_array.shape))

        if self.rotate.lower() == 'yes':
            if self.rotate_num == 90 or self.rotate_num == 180 or self.rotate_num == 270:
                print('Got it. Your images will be rotated by {} degrees.'.format(self.rotate_num))
                self.update_log_thread.update_log_signal.emit('Got it. Your images will be rotated by {} degrees.'.format(self.rotate_num))
            else:
                print('You must enter a value that is either 90, 180, or 270. Quitting...')
                self.update_log_thread.update_log_signal.emit('You must enter a value that is either 90, 180, or 270. Quitting...')
                sys.exit()
        elif self.rotate.lower() == 'no':
            print('OK, Your images will be converted it as it is.')
            self.update_log_thread.update_log_signal.emit('OK, Your images will be converted it as it is.')
        else:
            print('You must choose either y or n. Quitting...')
            self.update_log_thread.update_log_signal.emit('You must choose either y or n. Quitting...')
            sys.exit()

        # else if 3D image inputted
        if len(image_array.shape) == 3:
            # set 3d array dimension values
            nx, ny, nz = image_array.shape
            # set destination folder
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)
                print("Created output directory: " + self.output_folder)
                self.update_log_thread.update_log_signal.emit("Created output directory: " + self.output_folder)
            # 创建子文件夹
            if not os.path.exists(output_path_axial):
                os.makedirs(output_path_axial)
            if not os.path.exists(output_path_coronal):
                os.makedirs(output_path_coronal)
            if not os.path.exists(output_path_sagittal):
                os.mkdir(output_path_sagittal)

            # image_array[coronal, axial, Sagittal]  [冠状面，水平面，矢状面]
            slice_counter = 0
            total_slices = nz
            data_all = {}

            # 映射切片进度
            y_max = 100
            y_min = 1
            x_max = total_slices
            x_min = 1
            progress_counter = 0

            # iterate through slices
            for current_slice in range(0, total_slices):

                # alternate slices
                if (slice_counter % 1) == 0:
                    # rotate or no rotate
                    if self.rotate.lower() == 'yes':
                        if self.rotate_num == 90 or self.rotate_num == 180 or self.rotate_num == 270:
                            if self.rotate_num == 90:
                                # data = numpy.rot90(image_array[:, :, current_slice])
                                # data = numpy.rot90(image_array[:, current_slice, :])  # T1
                                # [矢状, 冠状, 水平]
                                data_axial = numpy.rot90(image_array[:, :, current_slice])  # T2
                                data_coronal = numpy.rot90(image_array[:, current_slice, :])
                                data_sagittal = numpy.rot90(image_array[current_slice, :, :])
                            elif self.rotate_num == 180:
                                # data = numpy.rot90(numpy.rot90(image_array[:, :, current_slice]))
                                # data = image_array[:, :, current_slice]  # T2
                                data_axial = numpy.rot90(numpy.rot90(image_array[:, :, current_slice]))  # T2
                                data_coronal = numpy.rot90(numpy.rot90(image_array[:, current_slice, :]))
                                data_sagittal = numpy.rot90(numpy.rot90(image_array[current_slice, :, :]))
                            elif self.rotate_num == 270:
                                data_axial = numpy.rot90(numpy.rot90(numpy.rot90(image_array[:, :, current_slice])))  # T2
                                data_coronal = numpy.rot90(numpy.rot90(numpy.rot90(image_array[:, current_slice, :])))
                                data_sagittal = numpy.rot90(numpy.rot90(numpy.rot90(image_array[current_slice, :, :])))
                    elif self.rotate.lower() == 'no':
                        # data = image_array[:, :, current_slice]
                        # data = image_array[:, current_slice, :]  # T1
                        data_axial = image_array[:, :, current_slice]
                        data_coronal = image_array[:, current_slice, :]
                        data_sagittal = image_array[current_slice, :, :]

                    data_all['axial'] = data_axial
                    data_all['coronal'] = data_coronal
                    data_all['sagittal'] = data_sagittal
                    # alternate slices and save as png
                    print('Start slicing...')
                    self.update_log_thread.update_log_signal.emit('Start slicing...')
                    if (slice_counter % 1) == 0:
                        for direction, data in data_all.items():
                            print('Saving image...')
                            self.update_log_thread.update_log_signal.emit('Saving {} image...'.format(direction))
                            image_name = self.input_file[:-4] + "_" + direction + "{:0>3}".format(
                                str(current_slice + 1)) + ".png"
                            self.update_log_thread.update_log_signal.emit('image_name: ' + image_name)
                            imageio.imwrite(image_name, data)
                            print('Saved.')
                            self.update_log_thread.update_log_signal.emit('Saved.')
                            # move images to folder
                            print('Moving image...')
                            self.update_log_thread.update_log_signal.emit('Moving image...')
                            src = image_name
                            shutil.move(src, Path(os.path.join(self.output_folder, direction)).as_posix())
                            slice_counter += 1
                            print('Moved.')
                            self.update_log_thread.update_log_signal.emit('Moved.')
                    progress_counter = y_min + math.ceil((y_max - y_min) / (x_max - x_min) * (current_slice - x_min))
                    self.update_progress_signal.emit(progress_counter)

            print('Finished converting images')
            self.update_log_thread.update_log_signal.emit('Finished converting images')
            result = True
        else:
            print('Not a 3D or 4D Image. Please try again.')
            self.update_log_thread.update_log_signal.emit('Not a 3D or 4D Image. Please try again.')
            result = False
        return result

    def nii2png_ADNI(self):
        pass

    def nii2png_IXI(self):
        pass

    def nii2png_OASIS(self):
        pass

    def nii2png_all_direction_folder(self):
        # print('direction: ' + self.direction)
        self.update_log_thread.update_log_signal.emit('direction: ' + self.direction)
        # print('rotate: ' + self.rotate)
        self.update_log_thread.update_log_signal.emit('rotate: ' + self.rotate)
        # print('rotate_num: ' + str(self.rotate_num))
        self.update_log_thread.update_log_signal.emit('rotate_num: ' + str(self.rotate_num))
        # print('dataset: ' + self.dataset)
        self.update_log_thread.update_log_signal.emit('dataset: ' + self.dataset)
        # print('当前工作目录: ' + os.getcwd())
        # self.update_log_thread.update_log_signal.emit('当前工作目录: ' + os.getcwd())
        # nii_files = os.listdir(self.input_folder)
        os.chdir(self.input_folder)
        # self._mutex.lock()
        for root, dirs, files in os.walk(self.input_folder):
            root = Path(root).as_posix()
            if len(files) != 0:
                for file in files:
                    file_name = os.path.splitext(file)[0]
                    if os.path.splitext(file)[1] == '.nii':
                            # 拼接nii文件的绝对路径
                            nii_file_path = Path(os.path.join(root, file)).as_posix()
                            print(nii_file_path)
                            self.update_log_thread.update_log_signal.emit('nii file path: ' + nii_file_path)
                            # 图片存放位置
                            png_dir_name = file_name
                            print(png_dir_name)
                            png_dir = Path(os.path.join(root, png_dir_name)).as_posix()
                            self.update_log_thread.update_log_signal.emit('png dir: ' + png_dir)
                            output_path_axial = Path(os.path.join(png_dir, 'axial')).as_posix()
                            output_path_coronal = Path(os.path.join(png_dir, 'coronal')).as_posix()
                            output_path_sagittal = Path(os.path.join(png_dir, 'sagittal')).as_posix()
                            self.update_log_thread.update_log_signal.emit('Input file is ' + self.input_file)
                            self.update_log_thread.update_log_signal.emit('Output folder is ' + self.output_folder)
                            self.update_log_thread.update_log_signal.emit('output axial folder is ' + output_path_axial)
                            self.update_log_thread.update_log_signal.emit('output coronal folder is ' + output_path_coronal)
                            self.update_log_thread.update_log_signal.emit('output sagittal folder is ' + output_path_sagittal)

                            # 创建png的存储目录
                            if not os.path.exists(png_dir):
                                os.makedirs(png_dir)
                                print("Created output directory: " + png_dir)
                                self.update_log_thread.update_log_signal.emit("Created output directory: " + png_dir)

                            # 创建子文件夹
                            if not os.path.exists(output_path_axial):
                                os.makedirs(output_path_axial)
                                self.update_log_thread.update_log_signal.emit('create output axial folder: ' + output_path_axial)
                            if not os.path.exists(output_path_coronal):
                                os.makedirs(output_path_coronal)
                                self.update_log_thread.update_log_signal.emit('create output coronal folder: ' + output_path_coronal)
                            if not os.path.exists(output_path_sagittal):
                                os.mkdir(output_path_sagittal)
                                self.update_log_thread.update_log_signal.emit('create output sagittal folder: ' + output_path_sagittal)

                            # 读取nii文件
                            print('Reading NIfTI file...')
                            self.update_log_thread.update_log_signal.emit('Reading NIfTI file...')
                            image_array = nibabel.load(nii_file_path).get_data()
                            # else if 3D image inputted
                            if len(image_array.shape) == 3:
                                # set 4d array dimension values
                                nx, ny, nz = image_array.shape
                                # nz = 10
                                total_slices = max(nx, ny, nz)
                                # total_slices = 3
                                data_all = {}
                                # image_array[coronal, axial, Sagittal]  [冠状面，水平面，矢状面]
                                slice_counter = 0
                                # 映射切片进度
                                y_max = 100
                                y_min = 1
                                x_max = total_slices
                                x_min = 1
                                progress_counter = 0
                                # iterate through slices
                                # ADNI
                                '''
                                for current_slice in range(0, total_slices):
                                    # alternate slices
                                    if (slice_counter % 1) == 0:
                                        # rotate or no rotate
                                        if self.rotate.lower() == 'yes':
                                            if self.rotate_num == 90 or self.rotate_num == 180 or self.rotate_num == 270:
                                                if self.rotate_num == 90:
                                                    data_axial = numpy.rot90(image_array[:, :, current_slice])
                                                    data_coronal = numpy.rot90(image_array[:, current_slice, :])
                                                    data_sagittal = numpy.rot90(image_array[current_slice, :, :])
                                                elif self.rotate_num == 180:
                                                    data_axial = numpy.rot90(
                                                        numpy.rot90(image_array[:, :, current_slice]))
                                                    data_coronal = numpy.rot90(
                                                        numpy.rot90(image_array[:, current_slice, :]))
                                                    data_sagittal = numpy.rot90(
                                                        numpy.rot90(image_array[current_slice, :, :]))
                                                elif self.rotate_num == 270:
                                                    data_axial = numpy.rot90(
                                                        numpy.rot90(numpy.rot90(image_array[:, :, current_slice])))
                                                    data_coronal = numpy.rot90(
                                                        numpy.rot90(numpy.rot90(image_array[:, current_slice, :])))
                                                    data_sagittal = numpy.rot90(
                                                        numpy.rot90(numpy.rot90(image_array[current_slice, :, :])))
                                        elif self.rotate.lower() == 'no':
                                            data_axial = image_array[:, :, current_slice]
                                            data_coronal = image_array[:, current_slice, :]
                                            data_sagittal = image_array[current_slice, :, :]

                                        data_all['axial'] = data_axial
                                        data_all['coronal'] = data_coronal
                                        data_all['sagittal'] = data_sagittal
                                        # alternate slices and save as png
                                        print('Start slicing...')
                                        self.update_log_thread.update_log_signal.emit('Start slicing...')
                                        # alternate slices and save as png
                                        if (slice_counter % 1) == 0:
                                            for direction, data in data_all.items():
                                                print('Saving image...')
                                                self.update_log_thread.update_log_signal.emit('Saving image...')
                                                image_name = png_dir + "_" + direction + "{:0>3}".format(
                                                    str(current_slice + 1)) + ".png"
                                                self.update_log_thread.update_log_signal.emit(
                                                    'image name: ' + image_name)
                                                imageio.imwrite(image_name, data)
                                                print('Saved.')
                                                self.update_log_thread.update_log_signal.emit('Saved.')
                                                # move images to folder
                                                print('Moving image...')
                                                self.update_log_thread.update_log_signal.emit('Moving image...')
                                                src = image_name
                                                shutil.move(src, Path(os.path.join(png_dir, direction)).as_posix())
                                                slice_counter += 1
                                                print('Moved.')
                                                self.update_log_thread.update_log_signal.emit('Moved.')

                                        progress_counter = y_min + math.ceil(
                                            (y_max - y_min) / (x_max - x_min) * (current_slice - x_min))
                                        self.update_progress_signal.emit(progress_counter)
                                '''
                                # print(self.dataset)
                                # IXI
                                for current_slice in range(0, total_slices):
                                    # alternate slices
                                    if (slice_counter % 1) == 0:
                                        # rotate or no rotate
                                        if self.rotate.lower() == 'yes':
                                            if self.rotate_num == 90 or self.rotate_num == 180 or self.rotate_num == 270:
                                                if self.rotate_num == 90:
                                                    data_axial = numpy.rot90(image_array[:, :, current_slice])
                                                    data_coronal = numpy.rot90(image_array[:, current_slice, :])
                                                    data_sagittal = numpy.rot90(image_array[current_slice, :, :])
                                                elif self.rotate_num == 180:
                                                    data_axial = numpy.rot90(
                                                        numpy.rot90(image_array[:, :, current_slice]))
                                                    data_coronal = numpy.rot90(
                                                        numpy.rot90(image_array[:, current_slice, :]))
                                                    data_sagittal = numpy.rot90(
                                                        numpy.rot90(image_array[current_slice, :, :]))
                                                elif self.rotate_num == 270:
                                                    data_axial = numpy.rot90(
                                                        numpy.rot90(numpy.rot90(image_array[:, :, current_slice])))
                                                    data_coronal = numpy.rot90(
                                                        numpy.rot90(numpy.rot90(image_array[:, current_slice, :])))
                                                    data_sagittal = numpy.rot90(
                                                        numpy.rot90(numpy.rot90(image_array[current_slice, :, :])))
                                        elif self.rotate.lower() == 'no':
                                            if self.dataset == 'ADNI':
                                                pass
                                            elif self.dataset == 'IXI':
                                                # IXI
                                                data_coronal = numpy.rot90(numpy.rot90(image_array[current_slice, :, :]))
                                                data_axial = numpy.rot90(numpy.rot90(image_array[:, current_slice, :]))
                                                if current_slice < nz:
                                                    data_sagittal = numpy.rot90(image_array[:, :, current_slice])
                                            elif self.dataset == 'OASIS':
                                                pass
                                            else:
                                                pass

                                            # IXI
                                            # data_coronal = numpy.rot90(numpy.rot90(image_array[current_slice, :, :]))
                                            # data_axial = numpy.rot90(numpy.rot90(image_array[:, current_slice, :]))
                                            # if current_slice < nz:
                                            #     data_sagittal = numpy.rot90(image_array[:, :, current_slice])

                                        data_all['axial'] = data_axial
                                        data_all['coronal'] = data_coronal
                                        data_all['sagittal'] = data_sagittal
                                        # alternate slices and save as png
                                        print('Start slicing...')
                                        self.update_log_thread.update_log_signal.emit('Start slicing...')
                                        # alternate slices and save as png
                                        if (slice_counter % 1) == 0:
                                            for direction, data in data_all.items():
                                                if direction == 'sagittal' and current_slice > nz:
                                                    continue
                                                else:
                                                    # print('Saving image...')
                                                    self.update_log_thread.update_log_signal.emit('Saving image...')
                                                    image_name = png_dir + "_" + direction + "{:0>3}".format(
                                                        str(current_slice + 1)) + ".png"
                                                    self.update_log_thread.update_log_signal.emit(
                                                        'image name: ' + image_name)
                                                    imageio.imwrite(image_name, data)
                                                    print('Saved.')
                                                    self.update_log_thread.update_log_signal.emit('Saved.')
                                                    # move images to folder
                                                    print('Moving image...')
                                                    self.update_log_thread.update_log_signal.emit('Moving image...')
                                                    src = image_name
                                                    shutil.move(src, Path(os.path.join(png_dir, direction)).as_posix())
                                                    slice_counter += 1
                                                    print('Moved.')
                                                    self.update_log_thread.update_log_signal.emit('Moved.')

                                        progress_counter = y_min + math.ceil(
                                            (y_max - y_min) / (x_max - x_min) * (current_slice - x_min))
                                        self.update_progress_signal.emit(progress_counter)
                                print('Finished converting images')
                                self.update_log_thread.update_log_signal.emit('Finished converting images')
                            else:
                                # print('Not a 3D or 4D Image. Please try again.')
                                self.update_log_thread.update_log_signal.emit('Not a 3D or 4D Image. Please try again.')

            else:
                print('looking for nii file...')
                self.update_log_thread.update_log_signal.emit('\nlooking for nii file...\n')

        # print('nii2png finished!')
        # self._mutex.unlock()
        self.update_log_thread.update_log_signal.emit('nii2png finished!')
        '''
        for nii_file in nii_files:
            # 拼接nii文件的绝对路径
            nii_file_path = Path(os.path.join(self.input_folder, nii_file)).as_posix()
            print(nii_file_path)
            self.update_log_thread.update_log_signal.emit('nii file path: ' + nii_file_path)
            # 图片存放位置
            png_dir_name = os.path.splitext(nii_file)[0]
            print(png_dir_name)
            png_dir = Path(os.path.join(self.input_folder, png_dir_name)).as_posix()
            self.update_log_thread.update_log_signal.emit('png dir: ' + png_dir)
            output_path_axial = Path(os.path.join(png_dir, 'axial')).as_posix()
            output_path_coronal = Path(os.path.join(png_dir, 'coronal')).as_posix()
            output_path_sagittal = Path(os.path.join(png_dir, 'sagittal')).as_posix()
            self.update_log_thread.update_log_signal.emit('Input file is ' + self.input_file)
            self.update_log_thread.update_log_signal.emit('Output folder is ' + self.output_folder)
            self.update_log_thread.update_log_signal.emit('output axial folder is ' + output_path_axial)
            self.update_log_thread.update_log_signal.emit('output coronal folder is ' + output_path_coronal)
            self.update_log_thread.update_log_signal.emit('output sagittal folder is ' + output_path_sagittal)

            # 创建png的存储目录
            if not os.path.exists(png_dir):
                os.makedirs(png_dir)
                print("Created output directory: " + png_dir)
                self.update_log_thread.update_log_signal.emit("Created output directory: " + png_dir)

            # 创建子文件夹
            if not os.path.exists(output_path_axial):
                os.makedirs(output_path_axial)
                self.update_log_thread.update_log_signal.emit('create output axial folder: ' + output_path_axial)
            if not os.path.exists(output_path_coronal):
                os.makedirs(output_path_coronal)
                self.update_log_thread.update_log_signal.emit('create output coronal folder: ' + output_path_coronal)
            if not os.path.exists(output_path_sagittal):
                os.mkdir(output_path_sagittal)
                self.update_log_thread.update_log_signal.emit('create output sagittal folder: ' + output_path_sagittal)

            # 读取nii文件
            print('Reading NIfTI file...')
            self.update_log_thread.update_log_signal.emit('Reading NIfTI file...')
            image_array = nibabel.load(nii_file_path).get_data()
            # else if 3D image inputted
            if len(image_array.shape) == 3:
                # set 4d array dimension values
                nx, ny, nz = image_array.shape
                total_slices = nz
                data_all = {}
                # image_array[coronal, axial, Sagittal]  [冠状面，水平面，矢状面]
                slice_counter = 0
                # 映射切片进度
                y_max = 100
                y_min = 1
                x_max = total_slices
                x_min = 1
                progress_counter = 0
                # iterate through slices
                for current_slice in range(0, total_slices):
                    # alternate slices
                    if (slice_counter % 1) == 0:
                        # rotate or no rotate
                        if self.rotate.lower() == 'yes':
                            if self.rotate_num == 90 or self.rotate_num == 180 or self.rotate_num == 270:
                                if self.rotate_num == 90:
                                    data_axial = numpy.rot90(image_array[:, :, current_slice])
                                    data_coronal = numpy.rot90(image_array[:, current_slice, :])
                                    data_sagittal = numpy.rot90(image_array[current_slice, :, :])
                                elif self.rotate_num == 180:
                                    data_axial = numpy.rot90(numpy.rot90(image_array[:, :, current_slice]))
                                    data_coronal = numpy.rot90(numpy.rot90(image_array[:, current_slice, :]))
                                    data_sagittal = numpy.rot90(numpy.rot90(image_array[current_slice, :, :]))
                                elif self.rotate_num == 270:
                                    data_axial = numpy.rot90(numpy.rot90(numpy.rot90(image_array[:, :, current_slice])))
                                    data_coronal = numpy.rot90(
                                        numpy.rot90(numpy.rot90(image_array[:, current_slice, :])))
                                    data_sagittal = numpy.rot90(
                                        numpy.rot90(numpy.rot90(image_array[current_slice, :, :])))
                        elif self.rotate.lower() == 'no':
                            data_axial = image_array[:, :, current_slice]
                            data_coronal = image_array[:, current_slice, :]
                            data_sagittal = image_array[current_slice, :, :]

                        data_all['axial'] = data_axial
                        data_all['coronal'] = data_coronal
                        data_all['sagittal'] = data_sagittal
                        # alternate slices and save as png
                        print('Start slicing...')
                        self.update_log_thread.update_log_signal.emit('Start slicing...')
                        # alternate slices and save as png
                        if (slice_counter % 1) == 0:
                            for direction, data in data_all.items():
                                print('Saving image...')
                                self.update_log_thread.update_log_signal.emit('Saving image...')
                                image_name = png_dir + "_" + direction + "{:0>3}".format(
                                    str(current_slice + 1)) + ".png"
                                self.update_log_thread.update_log_signal.emit('image name: ' + image_name)
                                imageio.imwrite(image_name, data)
                                print('Saved.')
                                self.update_log_thread.update_log_signal.emit('Saved.')
                                # move images to folder
                                print('Moving image...')
                                self.update_log_thread.update_log_signal.emit('Moving image...')
                                src = image_name
                                shutil.move(src, Path(os.path.join(png_dir_name, direction)).as_posix())
                                slice_counter += 1
                                print('Moved.')
                                self.update_log_thread.update_log_signal.emit('Moved.')

                        progress_counter = y_min + math.ceil((y_max - y_min) / (x_max - x_min) * (current_slice - x_min))
                        self.update_progress_signal.emit(progress_counter)
                print('Finished converting images')
                self.update_log_thread.update_log_signal.emit('Finished converting images')
            else:
                print('Not a 3D or 4D Image. Please try again.')
                self.update_log_thread.update_log_signal.emit('Not a 3D or 4D Image. Please try again.')
        '''
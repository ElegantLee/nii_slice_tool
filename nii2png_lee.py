#!/usr/bin/env python
#########################################
#       nii2png for Python 3.7          #
#         NIfTI Image Converter         #
#                v0.2.9                 #
#                                       #
#     Written by Alexander Laurence     #
# http://Celestial.Tokyo/~AlexLaurence/ #
#    alexander.adamlaurence@gmail.com   #
#              09 May 2019              #
#              MIT License              #
#########################################

import numpy, shutil, os, nibabel
import imageio
from pathlib import Path


def splite_file_IXI():
    pass


def splite_file_ADNI():
    pass


def splite_file_OASIS():
    pass


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
            data = image_array[:, :, current_slice]
        elif self.direction == 'coronal':
            data = image_array[:, current_slice, :]
        elif self.direction == 'sagittal':
            data = image_array[current_slice, :, :]
    return data

def nii2png_all_direction_folder(input_path, rotate='Yes', rotate_num=90):
    """

    :param input_path: 输入的nii文件或包含nii文件的文件夹
    :param rotate: 图片旋转的角度
    :param output_path: 输出的路径
    :return:
    """
    print(os.getcwd())
    nii_files = os.listdir(input_path)
    os.chdir(input_path)

    for nii_file in nii_files:
        ''' IXI '''
        # 拼接nii文件的绝对路径
        nii_file_path = Path(os.path.join(input_path, nii_file)).as_posix()
        print(nii_file_path)
        # 拼接png图片存放位置
        # nii_file_split = nii_file.split('-')
        # png_dir_name = nii_file_split[0] + nii_file_split[1] + nii_file_split[2]
        png_dir_name = os.path.splitext(nii_file)[0]
        print(png_dir_name)
        png_dir = Path(os.path.join(input_path, png_dir_name)).as_posix()
        output_path_axial = Path(os.path.join(png_dir, 'axial')).as_posix()
        output_path_coronal = Path(os.path.join(png_dir, 'coronal')).as_posix()
        output_path_sagittal = Path(os.path.join(png_dir, 'sagittal')).as_posix()

        # 创建png的存储目录
        if not os.path.exists(png_dir):
            os.makedirs(png_dir_name)
            print("Created output directory: " + png_dir)

        # 创建子文件夹
        if not os.path.exists(output_path_axial):
            os.makedirs(output_path_axial)
        if not os.path.exists(output_path_coronal):
            os.makedirs(output_path_coronal)
        if not os.path.exists(output_path_sagittal):
            os.mkdir(output_path_sagittal)

        # 读取nii文件
        print('Reading NIfTI file...')
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
                    if rotate.lower() == 'yes':
                        if rotate_num == 90 or rotate_num == 180 or rotate_num == 270:
                            if rotate_num == 90:
                                data_axial = numpy.rot90(image_array[:, :, current_slice])
                                data_coronal = numpy.rot90(image_array[:, current_slice, :])
                                data_sagittal = numpy.rot90(image_array[current_slice, :, :])
                            elif rotate_num == 180:
                                data_axial = numpy.rot90(numpy.rot90(image_array[:, :, current_slice]))
                                data_coronal = numpy.rot90(numpy.rot90(image_array[:, current_slice, :]))
                                data_sagittal = numpy.rot90(numpy.rot90(image_array[current_slice, :, :]))
                            elif rotate_num == 270:
                                data_axial = numpy.rot90(numpy.rot90(numpy.rot90(image_array[:, :, current_slice])))
                                data_coronal = numpy.rot90(numpy.rot90(numpy.rot90(image_array[:, current_slice, :])))
                                data_sagittal = numpy.rot90(numpy.rot90(numpy.rot90(image_array[current_slice, :, :])))
                    elif rotate.lower() == 'no':
                        data_axial = image_array[:, :, current_slice]
                        data_coronal = image_array[:, current_slice, :]
                        data_sagittal = image_array[current_slice, :, :]

                    data_all['axial'] = data_axial
                    data_all['coronal'] = data_coronal
                    data_all['sagittal'] = data_sagittal
                    # alternate slices and save as png
                    print('Start slicing...')
                    # self.update_log_thread.update_log_signal.emit('Start slicing...')
                    # alternate slices and save as png
                    if (slice_counter % 1) == 0:
                        # for direction, data in data_all.items():
                        #     print('Saving image...')
                        #     self.update_log_thread.update_log_signal.emit('Saving {} image...'.format(direction))
                        #     image_name = self.input_file[:-4] + "_" + direction + "{:0>3}".format(
                        #         str(current_slice + 1)) + ".png"
                        #     self.update_log_thread.update_log_signal.emit('image_name: ' + image_name)
                        #     imageio.imwrite(image_name, data)
                        #     print('Saved.')
                        #     self.update_log_thread.update_log_signal.emit('Saved.')
                        #     # move images to folder
                        #     print('Moving image...')
                        #     self.update_log_thread.update_log_signal.emit('Moving image...')
                        #     src = image_name
                        #     shutil.move(src, Path(os.path.join(self.output_folder, direction)).as_posix())
                        #     slice_counter += 1
                        #     print('Moved.')
                        #     self.update_log_thread.update_log_signal.emit('Moved.')
                        for direction, data in data_all.items():
                            print('Saving image...')
                            # self.update_log_thread.update_log_signal.emit('Saving {} image...'.format(direction))
                            image_name = png_dir + "_" + direction + "{:0>3}".format(
                                str(current_slice + 1)) + ".png"
                            # self.update_log_thread.update_log_signal.emit('image_name: ' + image_name)
                            imageio.imwrite(image_name, data)
                            print('Saved.')
                            # self.update_log_thread.update_log_signal.emit('Saved.')
                            # move images to folder
                            print('Moving image...')
                            # self.update_log_thread.update_log_signal.emit('Moving image...')
                            src = image_name
                            shutil.move(src, Path(os.path.join(png_dir_name, direction)).as_posix())
                            slice_counter += 1
                            print('Moved.')
                            # self.update_log_thread.update_log_signal.emit('Moved.')
            print('Finished converting images')
        else:
            print('Not a 3D or 4D Image. Please try again.')



nii2png_all_direction_folder(input_path='D:/Users/super/Documents/Datasets/IXI/test')
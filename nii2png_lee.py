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


def main(input_path, output_path, direction='axial', ask_rotate=270):
    """

    :param input_path: 输入的nii文件或包含nii文件的文件夹
    :param ask_rotate: 图片旋转的角度
    :param output_path: 输出的路径
    :return:
    """
    print(os.getcwd())
    nii_files = os.listdir(input_path)
    os.chdir(input_path)

    for nii_file in nii_files:
        # 拼接nii文件的绝对路径
        nii_file_path = input_path + '/' + nii_file
        nii_file_path = Path(nii_file_path).as_posix()
        print(nii_file_path)
        # 拼接png图片存放位置
        nii_file_split = nii_file.split('-')
        png_dir_name = nii_file_split[0] + nii_file_split[1] + nii_file_split[2]
        print(png_dir_name)

        # 创建png的存储目录
        if not os.path.exists(png_dir_name):
            os.makedirs(png_dir_name)
            print("Created ouput directory: " + png_dir_name)

        # 读取nii文件
        print('Reading NIfTI file...')
        image_array = nibabel.load(nii_file_path).get_data()
        # else if 3D image inputted
        if len(image_array.shape) == 3:
            # set 4d array dimension values
            nx, ny, nz = image_array.shape

            # set destination folder
            if not os.path.exists(png_dir_name):
                os.makedirs(png_dir_name)
                print("Created ouput directory: " + png_dir_name)

            print('Reading NIfTI file...')

            total_slices = image_array.shape[2]
            # print('-------------------------------')
            # print(image_array.shape)
            # print(total_slices)
            # print('-------------------------------')
            # image_array[coronal, axial, Sagittal]  [冠状面，水平面，矢状面]
            slice_counter = 0
            # start_slice = 150
            # end_slice = 100
            # iterate through slices
            for current_slice in range(0, total_slices):
                # alternate slices
                if (slice_counter % 1) == 0:
                    # rotate or no rotate
                    if ask_rotate.lower() == 'y':
                        if ask_rotate_num == 90 or ask_rotate_num == 180 or ask_rotate_num == 270:
                            if ask_rotate_num == 90:
                                # data = numpy.rot90(image_array[:, :, current_slice])
                                data = numpy.rot90(image_array[:, current_slice, :])  # T1
                                # data = image_array[:, :, current_slice]  # T2
                            elif ask_rotate_num == 180:
                                data = numpy.rot90(numpy.rot90(image_array[:, :, current_slice]))   # T1
                                # data = image_array[:, :, current_slice]  # T2
                            elif ask_rotate_num == 270:
                                data = numpy.rot90(numpy.rot90(numpy.rot90(image_array[:, :, current_slice])))
                    elif ask_rotate.lower() == 'n':
                        # data = image_array[:, :, current_slice]
                        data = image_array[:, current_slice, :]   # T1
                        # data = image_array[:, :, current_slice]     # T2

                    # alternate slices and save as png
                    if (slice_counter % 1) == 0:
                        print('Saving image...')
                        image_name = input_path[:-4] + "_z" + "{:0>3}".format(str(current_slice + 1)) + ".png"
                        imageio.imwrite(image_name, data)
                        print('Saved.')

                        # move images to folder
                        print('Moving image...')
                        src = image_name
                        shutil.move(src, png_dir_name)
                        slice_counter += 1
                        print('Moved.')

            print('Finished converting images')
        else:
            print('Not a 3D or 4D Image. Please try again.')

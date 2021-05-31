# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project: nii_slice_tool
# @File  : test
# @Author: super
# @Date  : 2021/5/30

# import dicom2nifti

# dicom_directory = 'D:/Users/super/Downloads/ADNI/168_S_6426/Accelerated_Sagittal_MPRAGE_MPR_Cor/2019-10-16_14_37_01.0/S884707'
# output_folder = 'D:/Users/super/Documents/test-dicom2nii'
# dicom2nifti.convert_directory(dicom_directory, output_folder, compression=False, reorient=True)

# import os
# from pathlib import Path
#
# dicom_directory = Path('D:/Users/super/Documents/Datasets/ADNI/ADNI_AD_MRI_3D_T1/002_S_5018').as_posix()
#
# for root, dirs, files in os.walk(dicom_directory):
#     print(Path(root).as_posix())
#     print('------------------------------')
#     for dir in dirs:
#         print(Path(dir).as_posix())
#     print('------------------------------')
#     for file in files:
#         print(Path(file).as_posix())

# import os
#
# print(os.path.splitext('D:/Users/super/Documents/002_S_5018/MPRAGE/2012-11-08_07_22_59.0/S174291/301_mprage.nii'))


""" 解压gz包的脚本 """
# import gzip
# import os
# from pathlib import Path
#
# root_path = Path('D:\\Users\\super\\Documents\\Datasets\\OASIS3').as_posix()
#
# for root, dirs, files in os.walk(root_path):
#     root = Path(root).as_posix()
#     print('root: ', root)
#     for file in files:
#         file_path = Path(os.path.join(root, file)).as_posix()
#         file_in_gz_path, file_type = os.path.splitext(file_path)
#         if file_type != '.gz':
#             break
#         print('file path: ', file_path)
#         g_file = gzip.GzipFile(file_path)
#         with open(file_in_gz_path, 'wb+') as g_file_write:
#             g_file_write.write(g_file.read())

""" 脚本-移动nii文件到指定文件夹 """
# D:\Users\super\Documents\test\OAS30001\OAS30001_MR_d0129\scans\anat2\resources\NIFTI
import os
from pathlib import Path

root_path = Path('D:\\Users\\super\\Documents\\test\\OAS30001').as_posix()
for root, dirs, files in os.walk(root_path):
    pass

# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project: nii_slice_tool
# @File  : updateLogThread
# @Author: super
# @Date  : 2021/5/25
import time
from PyQt5.QtCore import QThread, pyqtSignal, QMutex

'''
def nii2png_one_direction(input_file, output_path, rotate_num, progressBar, direction='axial', rotate='No'):
    output_path_direction = Path(os.path.join(output_path, direction)).as_posix()
    print('Input file is ', input_file)
    print('Output folder is ', output_path)

    if rotate.lower() == 'yes':
        if rotate_num == 90 or rotate_num == 180 or rotate_num == 270:
            print('Got it. Your images will be rotated by {} degrees.'.format(rotate_num))
        else:
            print('You must enter a value that is either 90, 180, or 270. Quitting...')
            sys.exit()
    elif rotate.lower() == 'no':
        print('OK, Your images will be converted it as it is.')
    else:
        print('You must choose either y or n. Quitting...')
        sys.exit()
    shape = 3
    # else if 3D image inputted
    if shape == 3:
        # set destination folder
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print("Created output directory: " + output_path)

        if not os.path.exists(output_path_direction):
            os.mkdir(output_path_direction)
            print("Created output-direction directory: " + output_path_direction)
        print('Reading NIfTI file...')
        if direction == 'axial':
            total_slices = 230
        elif direction == 'coronal':
            total_slices = 240
        elif direction == 'sagittal':
            total_slices = 230
        else:
            pass

        # image_array[coronal, axial, Sagittal]  [冠状面，水平面，矢状面]
        slice_counter = 0
        # 映射切片进度
        update_progressBar_thread = UpdateProgressBarThread(0, progressBar)
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
                time.sleep(3)
                # alternate slices and save as png
                if (slice_counter % 1) == 0:
                    time.sleep(20)
                    slice_counter += 1
                    print('Moved.')
                progress_counter = y_min + math.ceil((y_max - y_min) / (x_max - x_min) * (current_slice - x_min))
                update_progressBar_thread = UpdateProgressBarThread(progress_counter, progressBar)
                update_progressBar_thread.start()
        print('Finished converting images')
        result = True
    else:
        print('Not a 3D or 4D Image. Please try again.')
        result = False
    return result
'''


class UpdateLogThread(QThread):
    update_log_signal = pyqtSignal(str, name='UpdateLog')

    def __init__(self):
        super(UpdateLogThread, self).__init__()

    def run(self):
        print('run updateLogThreadTest...')
        return

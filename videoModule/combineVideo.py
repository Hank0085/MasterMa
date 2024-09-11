import os

import cv2


def combine_image_to_video(comb_path, output_file_path, fps=30, is_print=False):
    '''
        合并图像到视频
    '''
    fourcc = cv2.VideoWriter_fourcc(*'x264')

    file_items = [item for item in os.listdir(comb_path) if item.endswith('.png')]
    file_len = len(file_items)
    # print(comb_path, file_items)
    if file_len > 0:
        print(file_len)
        temp_img = cv2.imread(os.path.join(comb_path, file_items[0]))
        img_height, img_width, _ = temp_img.shape

        out = cv2.VideoWriter(output_file_path, fourcc, fps, (img_width, img_height))

        for i in range(file_len):
            pic_name = os.path.join(comb_path, 'result' + str(i) + ".png")
            print(pic_name)
            if is_print:
                print(i + 1, '/', file_len, ' ', pic_name)
            img = cv2.imread(pic_name)
            out.write(img)
        out.release()






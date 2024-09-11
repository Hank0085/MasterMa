import re

import numpy as np
import paddlehub as hub
import cv2
import os
import shutil

def imageSeg():
    human_seg = hub.Module(name="deeplabv3p_xception65_humanseg")
    count = 0
    with open('./model/mp4_img/imgList.txt','r') as file:
        lines = file.read().splitlines()

    # img = cv2.imread('mp4_img/'+lines[0])
    # cv2.imshow("image",img)
    # cv2.waitKey()
    print(lines)


    for i in lines:
        index = i.replace(".jpg","")
        if index != 'imgList.txt':
            result = human_seg.segmentation(images=[cv2.imread('./model/mp4_img/'+index+'.jpg')],
                                            visualization=True,
                                            use_gpu=True,
                                            output_dir='./model/mp4_img_mask/'+index)
            count += 1


        print(i)

    root_dir = './model/mp4_img_mask'

    # 遍历根目录下的所有文件夹
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)

        # 检查是否为文件夹且是否以数字命名
        if os.path.isdir(folder_path) and folder_name.isdigit():
            # 查找文件夹中的PNG图片
            for filename in os.listdir(folder_path):
                if filename.lower().endswith('.png'):
                    # 假设每个文件夹中只有一个PNG图片
                    source_file = os.path.join(folder_path, filename)
                    target_file = os.path.join(root_dir, f"{folder_name}.png")

                    # 移动并重命名文件
                    if not os.path.exists(target_file):
                        shutil.move(source_file, target_file)
                        print(f"Moved and renamed {source_file} to {target_file}")
                        break  # 找到后跳出循环

            # 删除文件夹，无论是否为空
            shutil.rmtree(folder_path, ignore_errors=True)
            print(f"Deleted folder {folder_path}")


    # 读取图像
    for i in range(0,count):
        # 加载图像
        image = cv2.imread('./model/mp4_img_mask/'+str(i)+'.png')

        # 将图像转换为灰度
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 通过阈值化将人像和背景分离
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # 进行形态学操作来去除噪声
        kernel = np.ones((5, 5), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        # 将背景部分设置为黑色
        image[binary == 255] = [0, 0, 0]
        # 将人像部分设置为红色
        image[binary == 0] = [0, 0, 255]

        cv2.imwrite('./model/mp4_img_mask/'+str(i)+'.png', image)
        # 显示结果
        print(i)

    return count
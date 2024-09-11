import os

import cv2

from model import paddleSegModel


def VideoProgress():
    os.environ['CUDA_VISIBLE_DEVICES']='0'
    transformVideoToImage('./model/videos/video.mp4','./model/mp4_img/')
    return paddleSegModel.imageSeg()


def transformVideoToImage(videoPath,imgPath):
    '''将视频保存成图片'''
    videoCapture = cv2.VideoCapture(videoPath)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    count = 0
    while (True):
        ret, frame = videoCapture.read()
        if ret:
            cv2.imwrite(imgPath + '%d.jpg' % count, frame)
            count += 1
        else:
            break
    videoCapture.release()

    filenameList = os.listdir(imgPath)
    with open(os.path.join(imgPath,'imgList.txt'),'w',encoding='utf-8')as file:
        file.writelines('\n'.join(filenameList))
    print('视频图片保存成功, 共有 %d 张' % count)
    return fps
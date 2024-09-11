#在这里下载b站视频
import shutil

import requests
import re
import json
from lxml import etree
import os
from videoModule import downloadText
from model import transformVideoToImage
from videoModule import fillByText
from videoModule import combineVideo
def getFinalVideo(bv):
    get_video(bv)
    downloadText.get_Dm(bv)
    title = downloadText.getContent(bv)
    #title='不惧困难，顽强乐观。贵在坚持，顺其自然！加油！奥利给！哈哈哈哈哈哈'
    count=transformVideoToImage.VideoProgress()
    fillByText.create_wordcloud('./model/texts/'+title+'弹幕.txt','./model/texts/'+title+'评论.txt',count)
    combineVideo.combine_image_to_video('./model/mp4_img_analysis/','./videoModule/video.mp4',30)


    #添加音频
    cmd = 'ffmpeg -i ./videoModule/video.mp4 -i ./model/videos/voice.mp4 -c:v copy -c:a aac -strict experimental ./videoModule/video1.mp4'
    os.system(cmd)
    shutil.move('./videoModule/video1.mp4','./masterMa/')


def get_video(bvId):
    url = "https://www.bilibili.com/video/"+bvId
    headers = {
            "referer": "https://www.bilibili.com",
            "origin": "https://www.bilibili.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}
    # 第一步   请求 视频网页的地址，拿到网页数据
    resp_ = requests.get(url,headers=headers)
    resp = resp_.text
    resp_.close()
    tree = etree.HTML(resp)
    # 第二步   从网页数据中提取视频标题
    title = tree.xpath('//h1/text()')[0]
    # print(title)
    # 第三步   从网页数据中提取视频url和音频url
    try:
        tree1 = tree.xpath('/html/head/script[3]/text()')[0]
        tree1 = re.sub(r'window.__playinfo__=', '', tree1)
        # print(tree1)
        tree1 = json.loads(tree1)
    except:
        tree1 = tree.xpath('/html/head/script[4]/text()')[0]
        tree1 = re.sub(r'window.__playinfo__=', '', tree1)
        # print(tree1)
        tree1 = json.loads(tree1)
        video = tree1['data']['dash']['video'][0]
        video_url = video['backupUrl'][0]
        print(video_url)
        audio = tree1['data']['dash']['audio'][0]
        audio_url = audio['backupUrl'][0]
        print(audio_url)
        ### 上述video_url 即视频url。audio_url 即音频url
        resp1 = requests.get(video_url, headers=headers).content
        resp2 = requests.get(audio_url, headers=headers).content
        with open("./model/videos/video.mp4", mode='wb') as file1:
            file1.write(resp1)
        with open("./model/videos/voice.mp4", mode='wb') as file2:
            file2.write(resp2)

# getFinalVideo('BV1J4411v7g6')
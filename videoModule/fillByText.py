import os
import re

import jieba
import stylecloud.stylecloud


def create_wordcloud(danmu,comment,count):
    for i in range(count):
        file_name = os.path.join("./model/mp4_img_mask/", str(i) + '.png')
        print(file_name)
        result = os.path.join("./model/mp4_img_analysis/", 'result' + str(i) + '.png')
        # print(result)
        text_content = ""
        with open(danmu, 'r',encoding='utf-8') as file:
            text1 = file.read()
        with open(comment,'r',encoding='utf-8') as file:
            text2 = file.read()
        text_content = text1+text2

        print(text_content)
        #print(text_content)
        stylecloud.gen_stylecloud(text=text_content,
                                  font_path='./方正兰亭刊黑.TTF',
                                  output_name=result,
                                  background_color="black",
                                  mask_img=file_name)
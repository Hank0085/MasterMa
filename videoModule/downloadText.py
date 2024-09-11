#这里负责下载视频弹幕与评论
import requests
import re
from videoModule import fillByText


def getResponse(html_url,params=None):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}
    response = requests.get(url=html_url,params=params, headers=headers)
    return response

def getOid(bvid):
    url = f'https://www.bilibili.com/video/{bvid}/'
    html_data = getResponse(url).text
    oid = re.findall('window.__INITIAL_STATE__={"aid":(\d+),', html_data)[0]
    title = re.findall('"title":"(.*?)","pubdate"', html_data)[0].replace(' ', '')
    return oid, title


#根据bv号获取弹幕相关网页
def getDmUrl(bvid):
    url = f'https://www.bilibili.com/video/{bvid}/'
    html_data = getResponse(url).text
    title = re.findall('"title":"(.*?)","pubdate"', html_data)[0].replace(' ', '')
    cid = re.search(r'"cid":(\d*),',html_data).group(1)
    dm_url = f'https://comment.bilibili.com/{cid}.xml'
    return dm_url,title

#下载弹幕
def get_Dm(bvid):
     url,title = getDmUrl(bvid)

     html_data = getResponse(url)
     html_data.encoding = html_data.apparent_encoding
     content_list = re.findall('<d p=".*?">(.*?)</d>', html_data.text)
     for content in content_list:
         with open(f'./model/texts/{title}弹幕.txt',mode='a',encoding='utf-8')as f:
             f.write(content)
             f.write('\n')



#获取评论
def getContent(bvid):
    oid, title = getOid(bvid)
    contentUrl = 'https://api.bilibili.com/x/v2/reply/main'
    try:
        for page in range(1,500):
            data = {
                'csrf': '6b0592355acbe9296460eab0c0a0b976',
                'mode': '3',
                'next': page,
                'oid': oid,
                'plat': '1',
                'type': '1',
            }
            jsonData = getResponse(contentUrl,data)
            jsonData.encoding = jsonData.apparent_encoding
            jsonData = jsonData.json()
            content = '\n'.join([i['content']['message'] for i in jsonData['data']['replies']])
            with open(f'./model/texts/{title}评论.txt', mode='a', encoding='utf-8') as f:
                f.write(content)
                f.write('\n')
    except:
        pass
    return title
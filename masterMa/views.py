import os.path
import pdb
import threading
import time

from django.http import JsonResponse, FileResponse
import urllib.parse
import re
from videoModule import downloadVideo
def responseVideo(request):
    if request.method == 'GET':
        url = request.GET.get('url','')
        url = urllib.parse.unquote(url)

        bv = re.search(r'BV.*?.{10}',url).group()
        print(bv)
        video = generate_video_url(bv)
        if len(video)!=0:
            response = FileResponse(open('./masterMa/video1.mp4', 'rb'), content_type='video/mp4')
            response['Content-Disposition'] = f'inline; filename="{"video1.mp4"}"'
            return response
        else:
            return JsonResponse("faile to create")
    else:
        return JsonResponse({'error':'Invalid request'},status=400)

def generate_video_url(bv):
    # pdb.set_trace()
    #print(os.getcwd())
    if (os.path.exists('./masterMa/video1.mp4')):
        print('done')
        return './masterMa/video1.mp4'
    #子线程执行函数
    worker_thread = threading.Thread(target=downloadVideo.getFinalVideo, args=(bv,))
    worker_thread.start()

    while True:
        if(os.path.exists('./masterMa/video1.mp4')):
            print('done')
            return './masterMa/video1.mp4'
        else:
            print('waiting...')
            time.sleep(5)

    return ""

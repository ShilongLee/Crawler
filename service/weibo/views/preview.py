from flask import request, Response
from utils.error_code import ErrorCode
from utils.reply import reply
import requests

# route
def preview():
    """
    预览视频
    """
    url = request.args.get('url', '')
    # 重新拼接url
    for key, value in request.args.items(multi=True):
        if key != 'url':
            url += f'&{key}={value}'
    # 发送请求
    headers = {'referer': 'https://weibo.com/'}
    response = requests.get(url, headers=headers, stream=True)
    if url == '':
        return reply(code=ErrorCode.PARAMETER_ERROR, msg='url不能为空')
    
    content_type = response.headers.get('content-type', '')
    
    def generate():
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk

    return Response(generate(), content_type=content_type)
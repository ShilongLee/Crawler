from fastapi import Request
from fastapi.responses import StreamingResponse
from utils.error_code import ErrorCode
from utils.reply import reply
import httpx

async def preview(request: Request):
    """
    预览视频
    """
    url = request.query_params.get('url', '')
    # 重新拼接url
    for key, value in dict(request.query_params).items():
        if key != 'url':
            url += f'&{key}={value}'
    # 发送请求
    headers = {'referer': 'https://weibo.com/'}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    if url == '':
        return reply(code=ErrorCode.PARAMETER_ERROR, msg='url不能为空')
    
    content_type = response.headers.get('content-type', '')

    async def generate():
        async for chunk in response.aiter_bytes():
            if chunk:
                yield chunk

    return StreamingResponse(generate(), media_type=content_type)
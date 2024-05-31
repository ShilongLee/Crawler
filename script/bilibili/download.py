import requests
import uuid
import os
import argparse
from moviepy.editor import VideoFileClip, AudioFileClip

def get_url(video_id: str, host: str) -> tuple[str, str]:
    """
    获取bilibili音视频下载地址
    :param video_id: 视频id
    :return: 视频下载地址, 音频下载地址
    """
    url = f'{host}/bilibili/detail?id={video_id}'
    respone = requests.get(url)
    if respone.status_code != 200:
        print(f"请求失败: {respone.status_code}, content: {respone.text}")
        return '', ''
    if respone.json().get('code', 0) != 0 :
        print(f"请求失败: {respone.json().get('msg', '')}, content: {respone.text}")
        return '', ''
    video_url = respone.json().get('data', {}).get('dash', {}).get('video', [{}])[0].get('baseUrl', '')
    audio_url = respone.json().get('data', {}).get('dash', {}).get('audio', [{}])[0].get('baseUrl', '')
    return  video_url, audio_url

def download(url: str, dir: str, ext: str = 'mp4') -> str:
    """
    下载bilibili音视频
    :param url: 视频下载地址
    """
    filename = f'{str(uuid.uuid4())}.{ext}'
    print(f"下载文件中: {dir + filename}")
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "DNT": "1",
        "Origin": "https://www.bilibili.com",
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        # "Range": "bytes=6091079-6495228", # 不加范围代表下载所有
        "Referer": "https://www.bilibili.com",
        "Sec-CH-UA": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    if not os.path.exists(dir):
        os.makedirs(dir)
    respone = requests.get(url, headers=headers)
    if respone.status_code != 200:
        print(f"请求失败: {respone.status_code}, content: {respone.text}")
        return ''
    with open(dir + filename, "wb") as f:
        f.write(respone.content)

    print(f"下载完成: {dir + filename}")
    return dir + filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download Bilibili program.')
    parser.add_argument('--id', type=str, help='Bilibili video id like `BV1Tz421D7R6`.', default='')
    parser.add_argument('--dir', type=str, help='Download path dir, default `.cache/bilibili/`.', default='.cache/bilibili/')
    parser.add_argument('--retain', type=int, help='Whether to keep the original file, 1 to keep, 0 not to keep.', default='0')
    parser.add_argument('--hostport', type=str, help='Crawler server hostport, default localhost.', default='http://localhost:8080')
    args = parser.parse_args()

    video_url, audio_url = get_url(args.id, args.hostport)
    video_path = download(video_url, args.dir, 'm4s')
    audio_path = download(audio_url, args.dir, 'm4s')
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    video = video.set_audio(audio)
    final_path = f'{args.dir}{args.id}.mp4'
    video.write_videofile(final_path)
    print(f"获取视频成功: {final_path}")
    if args.retain == 0:
        os.remove(video_path)
        os.remove(audio_path)

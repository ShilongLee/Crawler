import requests
from cookie import HOST, BILIBILI_COOKIE
import unittest
import time

class TestModule(unittest.TestCase):
    # 添加账户接口
    def test_add_account(self):
        data = {
            "id": "test",
            "cookie": BILIBILI_COOKIE
        }
        response = requests.post(f'{HOST}/bilibili/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
    
    # 账户列表接口
    def test_account_list(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": BILIBILI_COOKIE
        }
        response = requests.post(f'{HOST}/bilibili/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取账户列表
        response = requests.get(f'{HOST}/bilibili/account_list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']), 0)

    # 过期账户接口
    def test_expire_account(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": BILIBILI_COOKIE
        }
        response = requests.post(f'{HOST}/bilibili/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 过期账户
        data = {
            "id": "test",
        }
        response = requests.post(f'{HOST}/bilibili/expire_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

    # 获取详情接口
    def test_detail(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": BILIBILI_COOKIE
        }
        response = requests.post(f'{HOST}/bilibili/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取详情
        param = {
            "id" : 'BV1KJ4m137jv'# 抖音官方视频
        }
        response = requests.get(f'{HOST}/bilibili/detail', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data']['bvid'], param['id'])

    # 获取评论接口
    def test_comments(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": BILIBILI_COOKIE
        }
        response = requests.post(f'{HOST}/bilibili/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取评论
        param = {
            "id" : 'BV1KJ4m137jv'# 抖音官方视频
        }
        response = requests.get(f'{HOST}/bilibili/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        
        time.sleep(1)
        # 测试翻页 page_size = 20
        offset = 15
        limit = 5
        param = {
            "id" : 'BV1KJ4m137jv',   # 抖音官方视频
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/bilibili/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        first_page = [comment['rpid'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 20
        limit = 5
        param = {
            "id" : 'BV1KJ4m137jv',   # 抖音官方视频
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/bilibili/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        second_page = [comment['rpid'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 15
        limit = 10
        param = {
            "id" : 'BV1KJ4m137jv',   # 抖音官方视频
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/bilibili/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        self.assertSequenceEqual([comment['rpid'] for comment in response.json()['data']['comments']], first_page + second_page)
 
    # 获取评论回复接口
    def test_reply(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": BILIBILI_COOKIE
        }
        response = requests.post(f'{HOST}/bilibili/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取评论回复
        param = {
            "id" : 'BV1KJ4m137jv', # 抖音官方视频
            "comment_id": '228310046880'
        }
        response = requests.get(f'{HOST}/bilibili/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)

        time.sleep(1)
        # 测试翻页 page_size = 20
        offset = 5
        limit = 5
        param = {
            "id" : 'BV1KJ4m137jv',   # 抖音官方视频
            "comment_id": '228310046880',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/bilibili/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        first_page = [comment['rpid'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 10
        limit = 5
        param = {
            "id" : 'BV1KJ4m137jv',   # 抖音官方视频
            "comment_id": '228310046880',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/bilibili/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        second_page = [comment['rpid'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 5
        limit = 10
        param = {
            "id" : 'BV1KJ4m137jv',   # 抖音官方视频
            "comment_id": '228310046880',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/bilibili/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        self.assertSequenceEqual([comment['rpid'] for comment in response.json()['data']['comments']], first_page + second_page)

    # 搜索接口
    def test_search(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": BILIBILI_COOKIE
        }
        response = requests.post(f'{HOST}/bilibili/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 搜索
        param = {
            "keyword" : "白丝"
        }
        response = requests.get(f'{HOST}/bilibili/search', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']), 0)

    # 用户接口
    def test_user(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": BILIBILI_COOKIE
        }
        response = requests.post(f'{HOST}/bilibili/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取用户信息
        mid = '8047632'
        param = {
            "id" : mid    # bilibili弹幕网官方账号
        }
        response = requests.get(f'{HOST}/bilibili/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertNotEqual(response.json()['data']['mid'], mid)

        time.sleep(1)
        # 测试翻页 page_size = 10
        offset = 25
        limit = 5
        param = {
            "id" : mid,   # bilibili弹幕网官方账号
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/bilibili/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['videos']['list']), 0)
        first_page = [video['bvid'] for video in response.json()['data']['videos']['list']]

        time.sleep(1)
        offset = 30
        limit = 5
        param = {
            "id" : mid,   # bilibili弹幕网官方账号
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/bilibili/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['videos']['list']), 0)
        second_page = [video['bvid'] for video in response.json()['data']['videos']['list']]

        time.sleep(1)
        offset = 25
        limit = 10
        param = {
            "id" : mid,   # bilibili弹幕网官方账号
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/bilibili/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['videos']['list']), 0)
        self.assertSequenceEqual([video['bvid'] for video in response.json()['data']['videos']['list']], first_page + second_page)
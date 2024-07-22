import requests
from cookie import HOST, TB_COOKIE
import unittest
import time

class TestModule(unittest.TestCase):
    # 添加账户接口
    def test_add_account(self):
        data = {
            "id": "test",
            "cookie": TB_COOKIE
        }
        response = requests.post(f'{HOST}/taobao/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
    
    # 账户列表接口
    def test_account_list(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": TB_COOKIE
        }
        response = requests.post(f'{HOST}/taobao/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取账户列表
        response = requests.get(f'{HOST}/taobao/account_list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']), 0)

    # 过期账户接口
    def test_expire_account(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": TB_COOKIE
        }
        response = requests.post(f'{HOST}/taobao/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 过期账户
        data = {
            "id": "test",
        }
        response = requests.post(f'{HOST}/taobao/expire_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

    # 获取详情接口
    def test_detail(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": TB_COOKIE
        }
        response = requests.post(f'{HOST}/taobao/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取详情
        param = {
            "id" : '738605376921'
        }
        response = requests.get(f'{HOST}/taobao/detail', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data']['item']['itemId'], param['id'])

    # 获取评论接口
    def test_comments(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": TB_COOKIE
        }
        response = requests.post(f'{HOST}/taobao/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取评论
        param = {
            "id" : '738605376921'
        }
        response = requests.get(f'{HOST}/taobao/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        
        time.sleep(1)
        # 测试翻页 page_size = 20
        offset = 55
        limit = 5
        param = {
            "id" : '738605376921',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/taobao/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        first_page = [comment['id'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 60
        limit = 5
        param = {
            "id" : '738605376921',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/taobao/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        second_page = [comment['id'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 55
        limit = 10
        param = {
            "id" : '738605376921',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/taobao/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        self.assertSequenceEqual([comment['id'] for comment in response.json()['data']['comments']], first_page + second_page)

    # 搜索接口
    def test_search(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": TB_COOKIE
        }
        response = requests.post(f'{HOST}/taobao/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 搜索
        param = {
            "keyword" : "白丝"
        }
        response = requests.get(f'{HOST}/taobao/search', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['results']), 0)
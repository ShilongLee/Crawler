import requests
from cookie import HOST, DY_COOKIE
import unittest
import time
 
class TestModule(unittest.TestCase):
    # 添加账户接口
    def test_add_account(self):
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
    
    # 账户列表接口
    def test_account_list(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取账户列表
        response = requests.get(f'{HOST}/douyin/account_list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']), 0)

    # 过期账户接口
    def test_expire_account(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 过期账户
        data = {
            "id": "test",
        }
        response = requests.post(f'{HOST}/douyin/expire_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

    # 获取详情接口
    def test_detail(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取详情
        param = {
            "id" : '6911683747733671175'# 抖音官方视频
        }
        response = requests.get(f'{HOST}/douyin/detail', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data']['aweme_id'], param['id'])

    # 获取评论接口
    def test_comments(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取评论
        param = {
            "id" : '6911683747733671175'# 抖音官方视频
        }
        response = requests.get(f'{HOST}/douyin/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        
        time.sleep(1)
        # 测试翻页 page_size = 20
        offset = 55
        limit = 5
        param = {
            "id" : '6911683747733671175',   # 抖音官方视频
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        first_page = [comment['cid'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 60
        limit = 5
        param = {
            "id" : '6911683747733671175',   # 抖音官方视频
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        second_page = [comment['cid'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 55
        limit = 10
        param = {
            "id" : '6911683747733671175',   # 抖音官方视频
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/comments', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        self.assertSequenceEqual([comment['cid'] for comment in response.json()['data']['comments']], first_page + second_page)
 
    # 获取评论回复接口
    def test_reply(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取评论回复
        param = {
            "id" : '6911683747733671175', # 抖音官方视频
            "comment_id": '6912088044888031236'
        }
        response = requests.get(f'{HOST}/douyin/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)

        time.sleep(1)
        # 测试翻页 page_size = 20
        offset = 5
        limit = 5
        param = {
            "id" : '6911683747733671175',   # 抖音官方视频
            "comment_id": '6912088044888031236',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        first_page = [comment['cid'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 10
        limit = 5
        param = {
            "id" : '6911683747733671175',   # 抖音官方视频
            "comment_id": '6912088044888031236',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        second_page = [comment['cid'] for comment in response.json()['data']['comments']]

        time.sleep(1)
        offset = 5
        limit = 10
        param = {
            "id" : '6911683747733671175',   # 抖音官方视频
            "comment_id": '6912088044888031236',
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/replys', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['comments']), 0)
        self.assertSequenceEqual([comment['cid'] for comment in response.json()['data']['comments']], first_page + second_page)

    # 搜索接口
    def test_search(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 搜索
        param = {
            "keyword" : "白丝"
        }
        response = requests.get(f'{HOST}/douyin/search', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']), 0)

    # 用户接口
    def test_user(self):
        # 添加账户
        data = {
            "id": "test",
            "cookie": DY_COOKIE
        }
        response = requests.post(f'{HOST}/douyin/add_account', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 获取用户信息
        param = {
            "id" : "MS4wLjABAAAA3y0gs9xhygmvZhVEHWt5Y4aLHi9KooKSNxVQ2pslu10"    # 抖音官方账号
        }
        response = requests.get(f'{HOST}/douyin/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertNotEqual(response.json()['data']['user'], {})

        time.sleep(1)
        # 测试翻页 page_size = 10
        offset = 25
        limit = 5
        param = {
            "id" : 'MS4wLjABAAAA3y0gs9xhygmvZhVEHWt5Y4aLHi9KooKSNxVQ2pslu10',   # 抖音官方账号
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['aweme_list']), 0)
        first_page = [aweme['aweme_id'] for aweme in response.json()['data']['aweme_list']]

        time.sleep(1)
        offset = 30
        limit = 5
        param = {
            "id" : 'MS4wLjABAAAA3y0gs9xhygmvZhVEHWt5Y4aLHi9KooKSNxVQ2pslu10',   # 抖音官方账号
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['aweme_list']), 0)
        second_page = [aweme['aweme_id'] for aweme in response.json()['data']['aweme_list']]

        time.sleep(1)
        offset = 25
        limit = 10
        param = {
            "id" : 'MS4wLjABAAAA3y0gs9xhygmvZhVEHWt5Y4aLHi9KooKSNxVQ2pslu10',   # 抖音官方账号
            "offset": offset,
            "limit": limit
        }
        response = requests.get(f'{HOST}/douyin/user', params=param)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertGreater(len(response.json()['data']['aweme_list']), 0)
        self.assertSequenceEqual([aweme['aweme_id'] for aweme in response.json()['data']['aweme_list']], first_page + second_page)
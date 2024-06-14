from flask import Blueprint
from . import views

weibo = Blueprint('weibo', __name__)

weibo.add_url_rule('/add_account', 'add_account', views.add_account, methods=['POST'])
weibo.add_url_rule('/account_list', 'account_list', views.account_list, methods=['GET'])
weibo.add_url_rule('/detail', 'detail', views.detail, methods=['GET'])
weibo.add_url_rule('/comments', 'comments', views.comments, methods=['GET'])
weibo.add_url_rule('/replys', 'replys', views.replys, methods=['GET'])
weibo.add_url_rule('/search', 'search', views.search, methods=['GET'])
weibo.add_url_rule('/preview', 'preview', views.preview, methods=['GET'])
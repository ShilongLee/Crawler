from flask import Blueprint
from . import views

bilibili = Blueprint('bilibili', __name__)

bilibili.add_url_rule('/add_account', 'add_account', views.add_account, methods=['POST'])
bilibili.add_url_rule('/account_list', 'account_list', views.account_list, methods=['GET'])
bilibili.add_url_rule('/detail', 'detail', views.detail, methods=['GET'])
bilibili.add_url_rule('/comments', 'comments', views.comments, methods=['GET'])
bilibili.add_url_rule('/replys', 'replys', views.replys, methods=['GET'])
bilibili.add_url_rule('/search', 'search', views.search, methods=['GET'])
bilibili.add_url_rule('/user', 'user', views.user, methods=['GET'])
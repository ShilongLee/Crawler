from flask import Blueprint
from . import views

douyin = Blueprint('douyin', __name__)

douyin.add_url_rule('/add_account', 'add_account', views.add_account, methods=['POST'])
douyin.add_url_rule('/account_list', 'account_list', views.account_list, methods=['GET'])
douyin.add_url_rule('/detail', 'detail', views.detail, methods=['GET'])
douyin.add_url_rule('/comments', 'comments', views.comments, methods=['GET'])
douyin.add_url_rule('/replys', 'replys', views.replys, methods=['GET'])
douyin.add_url_rule('/search', 'search', views.search, methods=['GET'])
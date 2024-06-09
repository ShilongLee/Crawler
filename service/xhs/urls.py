from flask import Blueprint
from . import views

xhs = Blueprint('xhs', __name__)

xhs.add_url_rule('/add_account', 'add_account', views.add_account, methods=['POST'])
xhs.add_url_rule('/account_list', 'account_list', views.account_list, methods=['GET'])
xhs.add_url_rule('/detail', 'detail', views.detail, methods=['GET'])
xhs.add_url_rule('/comments', 'comments', views.comments, methods=['GET'])
xhs.add_url_rule('/replys', 'replys', views.replys, methods=['GET'])
xhs.add_url_rule('/search', 'search', views.search, methods=['GET'])
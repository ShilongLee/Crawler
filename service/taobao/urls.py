from flask import Blueprint
from . import views

taobao = Blueprint('taobao', __name__)

taobao.add_url_rule('/add_account', 'add_account', views.add_account, methods=['POST'])
taobao.add_url_rule('/account_list', 'account_list', views.account_list, methods=['GET'])
taobao.add_url_rule('/search', 'search', views.search, methods=['GET'])

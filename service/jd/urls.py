from flask import Blueprint
from . import views

jd = Blueprint('jd', __name__)

jd.add_url_rule('/add_account', 'add_account', views.add_account, methods=['POST'])
jd.add_url_rule('/account_list', 'account_list', views.account_list, methods=['GET'])
jd.add_url_rule('/search', 'search', views.search, methods=['GET'])

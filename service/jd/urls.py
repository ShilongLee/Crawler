from fastapi import APIRouter
from . import views

router = APIRouter(prefix='/jd')

router.add_api_route('/add_account', views.add_account, methods=['POST'])
router.add_api_route('/expire_account', views.expire_account, methods=['POST'])
router.add_api_route('/account_list', views.account_list, methods=['GET'])
router.add_api_route('/search', views.search, methods=['GET'])
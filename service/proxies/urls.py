from . import views
from fastapi import APIRouter

router = APIRouter(prefix='/proxies')

router.add_api_route('/add', views.add, methods=['POST'])
router.add_api_route('/list', views.list, methods=['GET'])
router.add_api_route('/remove', views.remove, methods=['POST'])
router.add_api_route('/disable', views.disable, methods=['POST'])
router.add_api_route('/enable', views.enable, methods=['POST'])

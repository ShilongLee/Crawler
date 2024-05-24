from flask import Flask
from service.douyin.urls import douyin
from service.kuaishou.urls import kuaishou
from lib.logger import logger
import yaml

app = Flask(__name__)
app.register_blueprint(douyin, url_prefix="/douyin")
app.register_blueprint(kuaishou, url_prefix="/kuaishou")

def init_service():
    config_file = "config/config.yaml"
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    logger.setup(config)
    app.logger.handlers = logger.get_logger().handlers
    app.logger.setLevel(logger.get_logger().level)

init_service()

if __name__ == '__main__':
    app.run(debug=False)

from flask import Flask

# 导入配置别名
from app.configs import conf_alias
# 导入插件初始化函数
from app.extensions import init_extensions
# 导入视图初始化函数
from app.views import init_views
# 导入模型, 使用manage db创建数据表
from app.models.demands import Demands
from app.models.users import Users
from app.models.roles import Roles
from app.models.auth import Auth


def create_app(conf='development'):
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(conf_alias[conf])

    # 加载插件
    init_extensions(app)

    # 加载视图函数
    init_views(app)

    return app

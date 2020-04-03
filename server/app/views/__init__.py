from app.views.demands import demands
from app.views.users import users
from app.views.public import public


def init_views(app, prefix='/api'):
    app.register_blueprint(public, url_prefix=prefix)
    app.register_blueprint(users, url_prefix=prefix)
    app.register_blueprint(demands, url_prefix=prefix)

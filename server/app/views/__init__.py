from app.views.demands import demands
from app.views.users import users


def init_views(app, prefix='/api'):
    app.register_blueprint(users, url_prefix=prefix)
    app.register_blueprint(demands, url_prefix=prefix)

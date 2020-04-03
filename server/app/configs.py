def sqlalchemy_uri():
    db_user = 'postgres'
    db_pwd = 'password'
    db_host = '47.96.145.90'
    db_port = '5432'
    db_dbname = 'graduation'
    return f'postgresql+psycopg2://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_dbname}'


class Config:
    SECRET_KEY = ''
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = sqlalchemy_uri()


class ProConfig(Config):
    SECRET_KEY = 'pro'
    SQLALCHEMY_DATABASE_URI = sqlalchemy_uri()


conf_alias = {
    'development': DevConfig,
    'production': ProConfig
}

# coding: utf-8
# 站点配置文件
import os


# 激活 跨站点请求伪造 保护
CSRF_ENABLED = True

# 加密秘钥
SECRET_KEY = 'shi-yan-lou'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

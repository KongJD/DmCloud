from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

__all__ = ['celery_app']

import pymysql
pymysql.version_info = (1, 4, 13, "final", 0) # 解决mysql版本问题报错而添加的代码
pymysql.install_as_MySQLdb()


# -*- coding: utf-8 -*-
__author__ = 'cht'

import redis


class operatRedis(object):

    def __init__(self,name):
        self.name = name
        # self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
        # self.r = redis.Redis(host='10.211.55.4', port=6379)
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379)

    ## 得到实例
    def get_instent(self):
        r = redis.Redis(connection_pool=self.pool)
        return r

    # 添加数据
    def add_url_filepath(self,r,url,filepath):
        r.hset(self.name,url,filepath)

    # 删除集合
    def del_key(self, r):
        r.delete(self.name)

    # 得到链接



    pass
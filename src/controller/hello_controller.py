#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Zella Zhong
Date: 2024-05-24 05:41:52
LastEditors: Zella Zhong
LastEditTime: 2024-05-24 05:44:12
FilePath: /id_allocation/src/controller/hello_controller.py
Description: 
'''
from httpsvr import httpsvr


class HelloController(httpsvr.BaseController):
    def __init__(self, obj, param=None):
        super(HelloController, self).__init__(obj)

    def hello(self):
        return httpsvr.Resp(msg="pong", data={}, code=0)

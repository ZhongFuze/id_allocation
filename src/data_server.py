#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Zella Zhong
Date: 2024-05-23 22:34:52
LastEditors: Zella Zhong
LastEditTime: 2024-05-23 22:54:59
FilePath: /id_allocation/src/data_server.py
Description: main entry point for allocating
'''
import os
import logging

import setting
import setting.filelogger as logger

from controller.allocation_controller import AllocationController


if __name__ == "__main__":
    config = setting.load_settings(env="development")
    # config = setting.load_settings(env="production")
    if not os.path.exists(config["server"]["log_path"]):
        os.makedirs(config["server"]["log_path"])
    logger.InitLogger(config)
    logger.SetLoggerName("id_allocation")

    try:
        from httpsvr import httpsvr
        # [path, controller class, method]
        ctrl_info = [
            ["/id_allocation/allocation", AllocationController, "allocation"],
        ]
        svr = httpsvr.HttpSvr(config, ctrl_info)
        svr.Start()

    except Exception as e:
        logging.exception(e)

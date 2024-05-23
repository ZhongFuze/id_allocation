#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Zella Zhong
Date: 2024-05-23 22:47:04
LastEditors: Zella Zhong
LastEditTime: 2024-05-24 04:52:22
FilePath: /id_allocation/src/controller/allocation_controller.py
Description: allocation controller
'''
import json
import logging
import time
import setting

from httpsvr import httpsvr
import psycopg2
from setting import get_write_conn


def dict_factory(cursor, row):
    """
    Convert query result to a dictionary.
    """
    col_names = [col_desc[0] for col_desc in cursor.description]
    return dict(zip(col_names, row))


class AllocationController(httpsvr.BaseController):
    '''AllocationController'''
    def __init__(self, obj, param=None):
        super(AllocationController, self).__init__(obj)

    def allocation(self):
        '''
        description:
        requestbody: {
            "graph_id": "string",
            "updated_nanosecond": "int64",
            "vids": ["string"],
        }
        return: {
            "return_graph_id": "string",
            "return_updated_nanosecond": "int64",
        }
        '''
        post_data = self.inout.request.body
        data = json.loads(post_data)
        graph_id = data.get("graph_id", "")
        updated_nanosecond = data.get("updated_nanosecond", 0)
        vids = data.get("vids", [])
        if graph_id == "" or updated_nanosecond == 0:
            return httpsvr.Resp(msg="Invalid input body", data={}, code=-1)
        if len(vids) == 0:
            return httpsvr.Resp(msg="Invalid input body", data={}, code=-1)

        
        data = {}
        rows = []
        code = 0
        msg = ""
        try:
            pg_conn = get_write_conn()
            cursor = pg_conn.cursor()

            process_vids = "ARRAY[" + ",".join(["'" + x + "'" for x in vids]) + "]"
            ssql = "SELECT * FROM process_id_allocation(%s, '%s', %d);" % (process_vids, graph_id, updated_nanosecond)
            cursor.execute(ssql)
            rows = [dict_factory(cursor, row) for row in cursor.fetchall()]
            logging.debug("allocation vids: {}, result: {}".format(process_vids, rows))
            if len(rows) == 0:
                cursor.close()
                pg_conn.close()
                return httpsvr.Resp(msg="allocation ID=null", data={}, code=-1)

            data = rows[0]
            cursor.close()
            pg_conn.close()
        except Exception as e:
            code = -1
            msg = repr(e)
            logging.exception(e)

        return httpsvr.Resp(msg=msg, data=data, code=code)
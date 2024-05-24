#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: Zella Zhong
Date: 2024-05-23 22:36:57
LastEditors: Zella Zhong
LastEditTime: 2024-05-24 23:57:37
FilePath: /id_allocation/src/setting/__init__.py
Description: load toml config and global setting
'''
import sys
import logging
import os
import toml

import psycopg2
from psycopg2 import pool

Settings = {
    "env": "development",
    "datapath": "./data",
}

ID_ALLOCATION = {
    "write": "",
    "read": "",
}

def load_settings(env="production"):
    """
    @description: load configurations from file
    """
    global Settings
    global ID_ALLOCATION

    config_file = "/app/config/production.toml"
    if env == "testing":
        config_file = "/app/config/testing.toml"
    elif env == "development":
        config_file = "./config/development.toml"
    elif env == "production":
        config_file = "/app/config/production.toml"
    else:
        raise ValueError("Unknown environment")

    config = toml.load(config_file)
    Settings["env"] = env
    Settings["datapath"] = os.path.join(config["server"]["work_path"], "data")
    ID_ALLOCATION = load_dsn(config_file)
    return config


def load_dsn(config_file):
    """
    @description: load pg dsn
    @params: config_file
    @return dsn_settings
    """
    try:
        config = toml.load(config_file)
        pg_dsn_settings = {
            "write": config["id_allocation"]["write"],
            "read": config["id_allocation"]["read"],
        }
        return pg_dsn_settings
    except Exception as ex:
        logging.exception(ex)


def get_write_conn():
    try:
        pg_conn = psycopg2.connect(ID_ALLOCATION["write"])
        pg_conn.autocommit = True
    except Exception as e:
        logging.exception(e)
        raise e

    return pg_conn


conn_pool = None

def initialize_connection_pool(minconn=1, maxconn=10):
    """
    Initialize the connection pool.
    """
    global conn_pool
    db_params = {
        "dbname": "xx",
        "user": "xx",
        "password": "xx",
        "host": "xx"
    }
    try:
        # conn_pool = pool.ThreadedConnectionPool(minconn=minconn, maxconn=maxconn, **db_params)
        conn_pool = pool.SimpleConnectionPool(minconn=minconn, maxconn=maxconn, **db_params)
        logging.info("Database connection pool created.")
    except Exception as e:
        logging.error("Error creating the database connection pool: {}".format(e))
        conn_pool = None


def get_connection():
    global conn_pool
    if conn_pool is None or conn_pool.closed:
        logging.info("Connection pool does not exist or has been closed, initializing a new one.")
        initialize_connection_pool()

    if conn_pool:
        try:
            conn = conn_pool.getconn()
            if conn:
                logging.info("Retrieved a connection from the pool. Used connections: {}".format(len(conn_pool._used)))
                return conn
            else:
                logging.error("Failed to retrieve a connection from the pool.")
        except Exception as e:
            logging.error("Error getting a connection from the pool: {}".format(e))
    else:
        logging.error("Connection pool is not available.")
        return None


# Function to release a connection back to the pool
def put_connection(conn):
    global conn_pool
    if conn_pool:
        logging.info("conn_pool used connection {}".format(len(conn_pool._used)))
        conn_pool.putconn(conn)
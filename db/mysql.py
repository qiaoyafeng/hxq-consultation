import numpy as np
import pymysql
import pandas as pd
from pymysql.converters import escape_string

from config import settings

mysql_host = settings.DB_IP
db_port = settings.DB_PORT
db_user = settings.DB_USERNAME
db_pass = settings.DB_PASSWORD
db_name = settings.DB_NAME


def query_sql(sql):
    db = pymysql.connect(host=mysql_host, port=db_port, user=db_user, passwd=db_pass, db=db_name)
    cursor = db.cursor()
    cursor.execute(sql)
    cols = [column[0] for column in cursor.description]
    results = cursor.fetchall()
    df = pd.DataFrame(list(results), columns=cols)
    return df.replace([np.nan], [None], regex=False).to_dict('records')


def build_update(info, table):
    sql = f"update {table} set"
    for key, value in info.items():
        if key not in ["id"]:
            if isinstance(value, str):
                sql = sql + f" {key}='{escape_string(value)}',"
            else:
                sql = sql + f" {key}='{value}',"
    sql = sql[:len(sql) - 1] + f"where id = {info['id']}"
    return sql


def build_create(info, table):
    col = ''
    val = ''
    for key, value in info.items():
        col = col + f" {key},"
        if isinstance(value, str):
            val = val + f" '{escape_string(value)}',"
        else:
            val = val + f" '{value}',"

    sql = f"insert into {table} ({col[:len(col) - 1]}) values ({val[:len(val) - 1]})"
    return sql


def update_sql(sql):
    db = pymysql.connect(host=mysql_host, port=db_port, user=db_user, passwd=db_pass, db=db_name)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

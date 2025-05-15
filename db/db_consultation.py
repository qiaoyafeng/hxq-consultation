import random

from config import settings
from db.mysql import update_sql, query_sql, build_create, build_update
import datetime

from service.log import logger

consult_table = "consultation"
ai_request_table = "ai_request"


def create_consult(name, sex, age, chief_complaint, batch_no, case_status, day=datetime.date.today()):
    if name.startswith("ipt"):
        question_nums = settings.CHAT_IPT_ROUNDS
        is_ipt = 1
    else:
        question_nums = random.randint(
            settings.CHAT_MIN_ROUNDS, settings.CHAT_MAX_ROUNDS
        )
        is_ipt = 0
    info = {
        "name": name,
        "sex": sex,
        "age": age,
        "batch_no": batch_no,
        "day": day,
        "question_nums": question_nums,
        "start_time": datetime.datetime.now(),
        "is_ipt": is_ipt,
        "case_status": case_status,
    }
    if chief_complaint:
        info.update({"chief_complaint": chief_complaint})

    sql = build_create(info, consult_table)
    update_sql(sql)
    return get_consult(name, day)


def get_consult(name, day):
    sql = f"SELECT * FROM {consult_table}  WHERE name = '{name}' and day = '{day}'"
    consults = query_sql(sql)
    return consults[-1] if consults else None


def get_consult_by_id(consult_id):
    sql = f"SELECT * FROM {consult_table}  WHERE id = '{consult_id}' "
    consults = query_sql(sql)
    return consults[-1] if consults else None


def get_consult_by_batch_no(batch_no):
    sql = f"SELECT * FROM {consult_table}  WHERE batch_no = '{batch_no}' "
    consults = query_sql(sql)
    return consults[-1] if consults else None


def get_consult_by_status(status):
    sql = f"SELECT * FROM {consult_table}  WHERE status = {status} "
    consults = query_sql(sql)
    return consults


def get_consult_by_condition(field, operator, value):
    sql = f"SELECT * FROM {consult_table}  WHERE {field} {operator} {value} "
    consults = query_sql(sql)
    return consults


def get_all_consults():
    sql = f"SELECT * FROM {consult_table} "
    consults = query_sql(sql)
    return consults


def get_day_consult(day):
    return query_sql(f"select * from {consult_table} where day ='{day}' ")


def update_consult(info):
    sql = build_update(info, consult_table)
    # logger.info(f"update_consult: sql: {sql} ")
    update_sql(sql)


def update_consult_status(id, status):
    update_sql(f"update {consult_table} set status={status} where id= {id}")


def update_consult_diagnosis(id, diagnosis):
    update_sql(
        f"update {consult_table} set status=3, diagnosis='{diagnosis}' where id= {id}"
    )


def update_consult_chief(id, chief):
    update_sql(f"update {consult_table} set chief_complaint='{chief}' where id= {id}")


def add_ai_request(plat, model, request, answer, cost):
    info = {
        "plat": plat,
        "model": model,
        "request": request,
        "answer": answer,
        "cost": cost,
    }
    sql = build_create(info, ai_request_table)
    update_sql(sql)

from db.mysql import update_sql, query_sql, build_create, build_update
import datetime
consult_table = 'consultation'


def create_consult(name, sex, age, chief_complaint, day=datetime.date.today()):
    info = {
        "name": name,
        "sex": sex,
        "age": age,
        "day": day,
        "start_time": datetime.datetime.now()
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


def get_consult_by_status(status):
    sql = f"SELECT * FROM {consult_table}  WHERE status = {status} "
    consults = query_sql(sql)
    return consults


def get_day_consult(day):
    return query_sql(f"select * from {consult_table} where day ='{day}' ")


def update_consult(info):
    sql = build_update(info, consult_table)
    update_sql(sql)


def update_consult_status(id, status):
    update_sql(f"update {consult_table} set status={status} where id= {id}")


def update_consult_diagnosis(id, diagnosis):
    update_sql(f"update {consult_table} set status=3, diagnosis='{diagnosis}' where id= {id}")


def update_consult_chief(id, chief):
    update_sql(f"update {consult_table} set chief_complaint='{chief}' where id= {id}")

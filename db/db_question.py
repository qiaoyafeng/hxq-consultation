from db.mysql import update_sql, query_sql, build_create, build_update
import datetime

consult_table = "consultation"
consult_question_table = "consultation_question"


def get_consult_questions(consult_id):
    return query_sql(
        f"select * from {consult_question_table} where consultation_id = {consult_id}"
    )


def create_consult_question(consult_id, question, answer):
    info = {
        "consultation_id": consult_id,
        "question": question,
    }
    if answer:
        info.update({"answer": answer})
    sql = build_create(info, consult_question_table)
    update_sql(sql)


def update_consult_question(consult_question_id, answer):
    info = {
        "id": consult_question_id,
        "answer": answer,
    }
    sql = build_update(info, consult_question_table)
    update_sql(sql)

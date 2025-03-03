from constants import QUESTIONS, IPT_QUESTIONS
from db import db_consultation
import datetime
import os
import subprocess
import sys
from pathlib import Path

from config import Config
from db.db_question import (
    get_consult_questions,
    create_consult_question,
    update_consult_question,
)
from service.llm import tongyi_llm, hxq_llm

TEMP_PATH = Config.get_temp_path()


class QuestionService:
    def __init__(self):
        self.tongyi_llm = tongyi_llm
        self.hxq_llm = hxq_llm

    def next_question(self, answer, messages=[], is_ipt=False, is_last_question=False):
        if is_ipt:
            system_content = f"你是一位名叫心心的精神心理科的医生，请根据下面的问诊问题，模拟医生的口气对我进行问诊，每次输出只能问其中一道问题。可以增加些你的理解内容，但问题含义不能变，并且前后问题要有关联。如果回答与问题有偏离，需要共情理解后，直接回到问题上来，字数不能超过50字。以下是所有问题:{IPT_QUESTIONS}"
        else:
            # system_content = f"你是一位名叫心心的精神心理科的医生，请根据下面的问诊问题，模拟医生的口气对我进行问诊，每次输出只能问其中一道问题。可以增加些你的理解内容，但问题含义不能变，并且前后问题要有关联。如果回答与问题有偏离，需要共情理解后，直接回到问题上来，字数不能超过50字。以下是所有问题:{QUESTIONS}"
            system_content = f"你是一位名叫心心的精神心理科的医生，模拟医生的口气对我进行4次问诊，每次输出只能问一道问题，语气更口语化，让患者感觉亲切。取消模拟动作铺垫类提问，只是咨询问诊。不对我的回复进行评论。不要对我的回复内容重复。医生第一句话从：我是好心情精神科虚拟医生-心心，请问您是感觉哪里不适，还是希望就其他健康问题进行咨询？开始，字数不能超过50字。"
        chat_messages = [
            {
                "role": "system",
                "content": system_content,
            }
        ]
        if answer:
            if is_last_question:
                chat_messages.extend(messages)
                chat_messages.append({"role": "user", "content": "请医生根据这次问诊进行总结,并结束本次问诊。"})
            else:
                chat_messages.extend(messages)
        else:
            chat_messages.append({"role": "user", "content": "请开始问诊"})
        question = tongyi_llm.chat(chat_messages)
        return question

    def get_consult_questions(self, consult_id):
        questions = get_consult_questions(consult_id)
        return questions

    def create_consult_question(self, consult_id, question, answer=None):
        questions = create_consult_question(consult_id, question, answer)
        return questions

    def update_consult_question(self, consult_question_id, answer):
        update_consult_question(consult_question_id, answer)


question_service = QuestionService()

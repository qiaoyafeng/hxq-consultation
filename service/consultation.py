import time

from constants import CONSULT_REPORT_PROMPT_TEMPLATE, CONSULT_STATUS_REPORT, CONSULT_STATUS_DONE, LLM_HXQ_PLAT_ID, \
    LLM_TONGYI_PLAT_ID, LLM_TONGYI_MODEL_QWEN_PLUS_ID, LLM_HXQ_MODEL_DS_R1_8B_ID
from db import db_consultation
import datetime

from service.llm import hxq_llm, tongyi_llm
from service.log import logger
from service.question import question_service
from utils import remove_think_tags, extract_think_and_answer


class ConsultationService:
    def __init__(self):
        self.question_service = question_service

    def create_consult(self, name, sex, age, chief_complaint, batch_no):
        return db_consultation.create_consult(name, sex, age, chief_complaint, batch_no)

    def get_consult(self, consult_id):
        return db_consultation.get_consult_by_id(consult_id)

    def get_consult_by_batch_no(self, batch_no):
        return db_consultation.get_consult_by_batch_no(batch_no)

    def update_consult(self, info):
        db_consultation.update_consult(info)

    def get_consult_questions(self, consult_id):
        return self.question_service.get_consult_questions(consult_id)

    def get_consult_next_question(self, consult_id, answer=None, questions=None, is_ipt=False, is_last_question=False):
        if questions:
            messages = []
            for q in questions:
                messages.extend([{"role": "assistant", "content": f"{q['question']}"}, {"role": "user", "content": f"{q['answer']}"}])
            question = self.question_service.next_question(answer, messages=messages, is_ipt=is_ipt, is_last_question=is_last_question)
        else:
            question = self.question_service.next_question(answer, is_ipt=is_ipt)

        self.question_service.create_consult_question(consult_id, question)
        return question

    def gen_consult_report(self, consult_id):
        logger.info(f"gen_consult_report: consult_id: {consult_id}....")
        questions = self.get_consult_questions(consult_id)
        consult = self.get_consult(consult_id)

        chat_messages = [
            {
                "role": "system",
                "content": f"你是一位精神心理科的医生，擅长从对话中识别心理疾病特征。现在需要根据以下医患对话生成专业问诊报告：",
            }
        ]
        q_a_str = []
        for q in questions:
            q_str = f"医生：{q['question']} \n患者：{q['answer']} \n"
            q_a_str.append(q_str)
        conversation = "".join(q_a_str)
        patient_info = f"姓名：{consult['name']}  性别：{'男' if consult['sex'] else '女'} 年龄： {consult['age']} "
        user_message = {"role": "user", "content": CONSULT_REPORT_PROMPT_TEMPLATE.format(patient_info=patient_info,conversation=conversation)}
        chat_messages.append(user_message)
        logger.info(f"gen_consult_report chat_messages: {chat_messages}")
        report_start_time = datetime.datetime.now()
        start = time.time()
        plat = LLM_HXQ_PLAT_ID
        model = LLM_HXQ_MODEL_DS_R1_8B_ID
        report = hxq_llm.chat(chat_messages)
        # plat = LLM_TONGYI_PLAT_ID
        # model = LLM_TONGYI_MODEL_QWEN_PLUS_ID
        # report = tongyi_llm.chat(chat_messages)
        cost = (time.time() - start) * 1000
        db_consultation.add_ai_request(plat, model, f"{chat_messages}", f"{report}", cost)
        logger.info(f"gen_consult_report report: {report}")
        report_think, report = extract_think_and_answer(report)
        # logger.info(f"gen_consult_report: report_think: {report_think},  report: {report} ")
        self.update_consult({"id": consult_id, "report_think": report_think, "report": report, "report_start_time": report_start_time, "report_end_time": datetime.datetime.now(), "status": CONSULT_STATUS_REPORT, })
        consult = self.get_consult(consult_id)
        logger.info(f"gen_consult_report: consult_id: {consult_id} done.")
        return consult

    def gen_consult_report_job(self):
        consults = db_consultation.get_consult_by_status(CONSULT_STATUS_DONE)
        if not consults:
            return
        logger.info(f"gen_consult_report_job....")
        for consult in consults:

            self.gen_consult_report(consult["id"])
        logger.info(f"gen_consult_report_job done")


consultation_service = ConsultationService()

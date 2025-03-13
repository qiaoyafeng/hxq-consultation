import time

from constants import CONSULT_REPORT_PROMPT_TEMPLATE, CONSULT_STATUS_REPORT, CONSULT_STATUS_DONE, LLM_HXQ_PLAT_ID, \
    LLM_TONGYI_PLAT_ID, LLM_TONGYI_MODEL_QWEN_PLUS_ID, LLM_HXQ_MODEL_DS_R1_8B_ID, CONSULT_HEALTH_ADVICE_PROMPT_TEMPLATE
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

    def get_consult_qa_str_by_questions(self, questions, is_has_title=True):
        logger.info(f"get_consult_qa_str_by_questions: questions: {questions}....")
        q_a_str = []
        for q in questions:
            if is_has_title:
                q_str = f"医生：{q['question']} \n患者：{q['answer']} \n"
            else:
                q_str = f"{q['question']} \n {q['answer']} \n"
            q_a_str.append(q_str)
        conversation = "".join(q_a_str)
        return conversation

    def get_consult_qa_str(self, consult_id, is_has_title=True):
        logger.info(f"get_consult_qa_str: consult_id: {consult_id}....")
        questions = self.get_consult_questions(consult_id)
        conversation = self.get_consult_qa_str_by_questions(questions, is_has_title=is_has_title)
        return conversation

    def gen_consult_report(self, consult_id):
        logger.info(f"gen_consult_report: consult_id: {consult_id}....")
        consult = self.get_consult(consult_id)

        questions = self.get_consult_questions(consult_id)
        if not(consult or questions):
            return
        logger.info(f"gen_consult_report: consult: {consult}, questions: {questions}， ")

        chat_messages = [
            {
                "role": "system",
                "content": f"你是一位精神心理科的医生，擅长从对话中识别心理疾病特征。现在需要根据以下医患对话生成专业问诊报告：",
            }
        ]
        conversation = self.get_consult_qa_str_by_questions(questions)
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

    def gen_consult_health_advice(self, consult_id):
        logger.info(f"gen_consult_health_advice: consult_id: {consult_id}....")
        consult = self.get_consult(consult_id)
        questions = self.get_consult_questions(consult_id)
        if not(consult or questions):
            return
        logger.info(f"gen_consult_health_advice: consult: {consult}, questions: {questions}， ")

        chat_messages = [
            {
                "role": "system",
                "content": f"你是一位精神心理科的医生，擅长从对话中识别心理疾病特征。现在需要根据以下医患对话生成健康建议：",
            }
        ]
        conversation = self.get_consult_qa_str_by_questions(questions)
        user_message = {"role": "user", "content": CONSULT_HEALTH_ADVICE_PROMPT_TEMPLATE.format(conversation=conversation)}
        chat_messages.append(user_message)
        logger.info(f"gen_consult_report chat_messages: {chat_messages}")
        report_start_time = datetime.datetime.now()
        start = time.time()
        # plat = LLM_HXQ_PLAT_ID
        # model = LLM_HXQ_MODEL_DS_R1_8B_ID
        # report = hxq_llm.chat(chat_messages)
        plat = LLM_TONGYI_PLAT_ID
        model = LLM_TONGYI_MODEL_QWEN_PLUS_ID
        content = tongyi_llm.chat(chat_messages)
        cost = (time.time() - start) * 1000
        db_consultation.add_ai_request(plat, model, f"{chat_messages}", f"{content}", cost)
        logger.info(f"gen_consult_health_advice report: {content}")
        think, answer = extract_think_and_answer(content)
        # logger.info(f"gen_consult_health_advice: think: {think},  answer: {answer} ")
        self.update_consult(
            {"id": consult_id, "health_advice": answer})
        consult = self.get_consult(consult_id)
        logger.info(f"gen_consult_health_advice: consult_id: {consult_id} done.")
        return consult

    def gen_health_advice_job(self):
        consults = db_consultation.get_consult_by_condition("status", ">=", CONSULT_STATUS_DONE)
        for consult in consults:
            if not consult["health_advice"]:
                logger.info(f"gen_health_advice_job consult id: {consult['id']} ...")
                self.gen_consult_health_advice(consult["id"])
                logger.info(f"gen_health_advice_job consult id: {consult['id']}  done")


consultation_service = ConsultationService()

import os
import random
from concurrent.futures import ThreadPoolExecutor

import requests
import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse, JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler

from constants import CONSULT_STATUS_DONE
from schemas import CreateConsultRequest, QuestionNextRequest
from service.consultation import consultation_service
from service.log import logger
from service.question import question_service
from utils import get_resp, replace_special_character, build_resp
from config import Config, settings

app = FastAPI(
    title="好心情-智能问诊",
    summary="好心情-智能问诊",
    docs_url=None,
    redoc_url=None,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    content = jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    logger.error(f"validation_exception_handler content: {content}")
    message = f"参数验证失败。"
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=build_resp(status.HTTP_422_UNPROCESSABLE_ENTITY, {}, message=message)
    )


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

TEMP_PATH = Config.get_temp_path()


scheduler = BackgroundScheduler()


@app.on_event("startup")
async def startup_event():
    scheduler.start()
    scheduler.add_job(consultation_service.gen_consult_report_job, "interval", seconds=5)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/js/swagger-ui-bundle.js",
        swagger_css_url="/static/js/swagger-ui.css",
    )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/get_file/{file_name}", summary="Get file by file name")
def get_file(file_name: str):
    file_path = os.path.isfile(os.path.join(TEMP_PATH, file_name))
    if file_path:
        return FileResponse(os.path.join(TEMP_PATH, file_name))
    else:
        return {"code": 404, "message": "file does not exist."}


@app.get("/get_html/{html_name}", response_class=HTMLResponse)
async def get_html(request: Request, html_name: str):
    return templates.TemplateResponse(
        f"{html_name}.html", {"request": request, "html_name": html_name}
    )


@app.post("/api/create_consult", summary="创建问诊")
async def create_consult(data_request: CreateConsultRequest, request: Request):
    name = data_request.name
    sex = data_request.sex
    age = data_request.age
    chief_complaint = data_request.chief_complaint
    consult = consultation_service.create_consult(name, sex, age, chief_complaint)
    print(f"consult: {consult}")
    return build_resp(0, consult)


@app.post("/api/question_next", summary="获取问题")
async def question_next(data_request: QuestionNextRequest, request: Request):
    consult_id = data_request.consult_id
    if not consult_id:
        consult_id = request.headers.get("consult_id")
    if not consult_id:
        return build_resp(422, {}, message="consult_id 字段为空")

    answer = data_request.answer
    logger.info(f"question_next: consult_id: {consult_id}, answer: {answer}")
    consult = consultation_service.get_consult(consult_id)
    if not consult:
        return build_resp(404, {}, message="问诊记录不存在！")
    is_ipt = False
    if consult["name"].startswith("ipt"):
        is_ipt = True
    questions = question_service.get_consult_questions(consult_id)
    is_last_question = False
    if questions:
        if answer:
            if len(questions) == consult["question_nums"]:
                question_service.update_consult_question(questions[-1]["id"], answer)
                consultation_service.update_consult({"id": consult_id, "status": CONSULT_STATUS_DONE})
                return build_resp(0, {"is_has_next": 0, "question": ""})
            elif len(questions) == consult["question_nums"] - 1:
                question_service.update_consult_question(questions[-1]["id"], answer)
                is_last_question = True
                questions[-1]["answer"] = answer
            else:
                question_service.update_consult_question(questions[-1]["id"], answer)
                questions[-1]["answer"] = answer
        else:
            return build_resp(422, {}, message="回复不能为空！")
        question = consultation_service.get_consult_next_question(consult_id, answer, questions, is_ipt=is_ipt, is_last_question=is_last_question)
    else:
        question = consultation_service.get_consult_next_question(consult_id, answer, is_ipt=is_ipt)
    logger.info(f"question_next: consult: {consult}, question: {question}")
    return build_resp(0, {"is_has_next": 1, "question": question})


@app.get("/api/get_consult", summary="获取问诊")
async def get_consult(request: Request, consult_id: int = 0):
    if not consult_id:
        consult_id = request.headers.get("consult_id")
    if not consult_id:
        return build_resp(422, message="consult_id 字段为空")

    consult = consultation_service.get_consult(consult_id)
    print(f"consult: {consult}")
    logger.info(f"get_consult: consult: {consult}")
    return build_resp(0, {"consult": consult})


@app.post("/api/gen_consult_report", summary="生成报告")
async def gen_consult_report(request: Request, consult_id: int = 0):
    if not consult_id:
        consult_id = request.headers.get("consult_id")
    if not consult_id:
        return build_resp(422, message="consult_id 字段为空")

    consult = consultation_service.gen_consult_report(consult_id)
    print(f"consult: {consult}")
    logger.info(f"get_consult: consult: {consult}")
    return build_resp(0, {"consult": consult})


if __name__ == "__main__":
    uvicorn.run(
        app="__main__:app",
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKERS,
        reload=settings.RELOAD,
    )

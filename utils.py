import base64
import re
import shutil
import uuid
from pathlib import Path

import requests
from config import Config

TEMP_PATH = Config.get_temp_path()


def base64_encode(stream):
    return str(base64.b64encode(stream), "utf-8")


def base64_decode(base64_str: str):
    return base64.b64decode(base64_str)


def encode_file_to_base64(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def decode_and_save_base64(base64_str, save_path):
    with open(save_path, "wb") as file:
        file.write(base64.b64decode(base64_str))


def get_resp():
    resp = {
        "code": 0,
        "message": "操作成功！",
        "success": True,
        "data": {},
    }
    return resp


def build_resp(code, data, message=None):
    resp = {
        "code": code,
        "message": message,
        "success": code == 0,
        "data": data,
    }
    return resp


def safe_int(value, default=0):
    try:
        value = str(value).replace(",", "").split(".")[0].strip()
        return int(value)
    except Exception as e:
        _ = e
        return default


def replace_special_character(raw_str):
    update_str = (
        raw_str.replace("\n", "。")
        .replace("\r", "")
        .replace("【", "")
        .replace("】", "")
        .replace("[", "")
        .replace("]", "")
    )
    return update_str


async def download_file(file_url, file_path):
    with open(file_path, "wb") as file:
        r = requests.get(file_url)
        file.write(r.content)


def copy_file(source_path, target_path):
    shutil.copy(source_path, target_path)


def extract_think_and_answer(response_text):
    think_pattern = re.compile(r"<think>(.*?)</think>", re.DOTALL)
    think_content = ",".join(think_pattern.findall(response_text))
    answer_text = think_pattern.sub("", response_text).strip()
    return think_content, answer_text


def remove_think_tags(response):
    cleaned_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
    return cleaned_response.strip()


def has_name_file(directory, file_stem,  extensions):
    for file in Path(directory).iterdir():
        if file.is_file() and file.stem == file_stem and file.suffix.lower() in extensions:
            return True
    return False


def get_name_file(directory, file_stem,  extensions=[]):
    for file in Path(directory).iterdir():
        if extensions:
            if file.is_file() and file.stem == file_stem and file.suffix.lower() in extensions:
                return file
        else:
            if file.is_file() and file.stem == file_stem:
                return file

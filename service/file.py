import uuid

import requests
from fastapi import UploadFile

from PIL import Image

from config import settings, Config
from utils import download_file, copy_file

TEMP_PATH = Config.get_temp_path()


class FileService:
    def __init__(self):
        pass

    # 根据URL保存文件
    async def save_file(self, file_url: str, suffix="wav"):
        file_name = f"{uuid.uuid4().hex}.{suffix}"
        file_path = f"{TEMP_PATH}/{file_name}"
        await download_file(file_url, file_path)
        local_url = f"{settings.BASE_DOMAIN}/get_file/{file_name}"
        return local_url, file_path, file_name

    # 上传文件
    async def uploadfile(self, file: UploadFile, dir_path=None, file_stem=None):
        suffix = file.filename.split(".")[-1]
        if file_stem:
            file_name = f"{file_stem}.{suffix}"
        else:
            file_name = f"{uuid.uuid4().hex}.{suffix}"
        file_path = f"{dir_path}/{file_name}" if dir_path else f"{TEMP_PATH}/{file_name}"
        local_url = f"{settings.BASE_DOMAIN}/get_file/{file_name}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return local_url, file_path, file_name

    def upload_file_to_oss(self, url, filepath, file):
        if not url:
            url = "https://saasts.haoxinqing.cn/oss/upload"
        payload = {'ossPath': filepath}
        files = [
            ('file', file)
        ]
        headers = {"Accept": "*/*"}
        response = requests.post(url, data=payload, headers=headers, files=files)
        return response

    def resize_image_to_fit(self, image_path, max_width=500, max_height=600, save_path=None):
        """
        将图片按比例缩小到不超过指定最大宽高（不拉伸，等比缩放）

        :param image_path: 图片路径
        :param max_width: 最大宽度
        :param max_height: 最大高度
        :param save_path: 缩放后保存路径（默认为覆盖原图）
        :return: 原始尺寸，新尺寸
        """
        img = Image.open(image_path)
        original_size = img.size  # (width, height)
        img.thumbnail((max_width, max_height), Image.ANTIALIAS)  # 等比缩放

        if save_path is None:
            save_path = image_path  # 覆盖原图

        img.save(save_path)
        return original_size, img.size


file_service = FileService()

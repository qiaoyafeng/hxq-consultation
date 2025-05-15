import json
import uuid
from http import HTTPStatus
from urllib import parse

import requests

from schemas import VLLMChatCompletionRequest
from config import settings

from service.log import logger


class VLLMService:
    """
    VLLM相关服务
    """

    def __init__(self):
        self.HXQ_VLLM_API_DOMAIN = settings.HXQ_VLLM_API_DOMAIN
        self.default_model = "/data/shared/Qwen2.5-VL-7B-Instruct-AWQ"

    def get_models(self):
        logger.info(f"vllm service get_models")
        url = f"{self.HXQ_VLLM_API_DOMAIN}/v1/models"
        response = requests.get(url)
        logger.info(f"vllm service get_models response: {response.json()}")
        if response.status_code == HTTPStatus.OK:
            response_data = response.json().get("data")
        else:
            response_data = {}
            print(f"Request failed with status code: {response.status_code}")
        return response_data

    def create_chat_completions(self, data):
        logger.info(f"vllm service create_chat_completions...")
        url = f"{self.HXQ_VLLM_API_DOMAIN}/v1/chat/completions"
        json_data = {
            "messages": data.messages,
            "model": data.model if data.model else self.default_model,
        }
        logger.info(f"json_data: {json_data}")
        response = requests.post(url, json=json_data)
        logger.info(f"vllm service create_chat_completion response: {response.json()}")
        if response.status_code == HTTPStatus.OK:
            response_data = response.json()
        else:
            response_data = {}
            logger.error(f"Request failed with status code: {response.status_code}")
        return response_data


vllm_service = VLLMService()


if __name__ == "__main__":
    message = "请描述这张图片中的内容。"
    models = vllm_service.get_models()
    print(f"models: {models}")

    image_url = "https://file.haoxinqing.cn/saas/emo/media/avatar/3136c8a8-7f0d-421d-86ca-94f164e30cba.jpg"

    # image_url = "https://dev-file.haoxinqing.cn/data/hxq/test/temp/20250415/20250415092117323.jpg"

    test_create_chat_completion_request_dict = {
        "model": "/data/shared/Qwen2.5-VL-7B-Instruct-AWQ",
        "messages": [
            {"role": "system", "content": "你是一个专业的心理咨询师，精通房树人（HTP）测试的理论和解读方法。"},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        },
                    },
                    {"type": "text", "text": "请以心理咨询师的方式解析这张房树人的图片,需根据以结构化数据进行分析"},
                ],
            },
        ],
    }

    test_create_chat_completion_request = VLLMChatCompletionRequest(
        **test_create_chat_completion_request_dict
    )

    test_create_chat_completion_response = vllm_service.create_chat_completions(
        test_create_chat_completion_request
    )
    print(
        f"test_create_chat_completion_response: {test_create_chat_completion_response}"
    )


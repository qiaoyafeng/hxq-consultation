import abc
import json
import requests
from openai import OpenAI
from typing import Dict, List, Optional

from config import settings
from service.log import logger


class DeepSeekLLM:
    def __init__(self):
        self.base_url = "https://api.deepseek.com"
        self.api_key = settings.DEEPSEEK_API_KEY
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat(self, messages, model="deepseek-chat"):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        content = response.choices[0].message.content
        return content


class TongyiLLM:
    def __init__(self, ):
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.api_key = settings.DASHSCOPE_API_KEY
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat(self, messages, model="qwen-plus"):
        logger.info(f"TongyiLLM chat: model: {model}, messages:{messages}")
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        content = response.choices[0].message.content
        return content


class HXQLLM:

    def __init__(self, ):
        from ollama import Client
        self.host = "http://172.16.34.239:11434"
        self.client = Client(
            host=self.host
        )

    def chat(self, messages, model="deepseek-r1:8b"):

        response = self.client.chat(
            model=model,
            messages=messages
        )
        content = response.message.content
        return content


tongyi_llm = TongyiLLM()
hxq_llm = HXQLLM()

if __name__ == "__main__":
    messages = [{"role": "user", "content": "你是谁？"}]
    deepseek = DeepSeekLLM()
    content = deepseek.chat(messages)
    print(content)

    tongyi = TongyiLLM()
    resp = tongyi.chat(messages)
    print(resp)

    hxq = HXQLLM()
    resp = hxq.chat(messages)
    print(resp)


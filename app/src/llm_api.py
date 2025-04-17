# -*-coding:utf-8 -*-

"""
@author: hanscal
@date: 2024/10/1 17:11
"""
import os
import re
import json
import time
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from openai import OpenAI
from conf.config import oneapi_key, oneapi_base_url

def askChatGPTAPI(query,engine='qwen2-instruct',api_key=oneapi_key, base_url=oneapi_base_url):
    # 魔法功能处理
    if len(query)<= 3 or query.lower() == "#" or query.lower() == "findall" or re.search(r"[\u4e00-\u9fff]",query):
        return {"keywords": [], "timecost": "0ms"}
    temperature = 0.5
    client_oneapi = OpenAI(api_key=api_key, base_url=base_url)
    prompt = f'Please just return the top-10 related keywords of papers on "{query}" in JSON format with the key named "keywords". The output must start with "```json" and end with "```".'
    st = time.time()
    response = client_oneapi.chat.completions.create(
        model=engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for search suggestion of paper in the field of artificial intelligence"},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature
    )
    response = response.choices[0].message.content
    # print(response)
    keywords = {}
    # 正则表达式，处理是否存在三重反引号的情况
    pattern = r"(?:```json\s*)?({.*})(?:\s*```)?"
    match = re.search(pattern, response, flags=re.DOTALL)
    # 如果都没有找到反引号，尝试从整个 response 中提取 JSON
    if match:
        keywords = match.group(1).strip()  # 提取出JSON部分，并去除首尾的空格

    response = json.loads(keywords)
    ed = time.time()
    if response and type(response) is list:
        if type(response[0]) is dict:
            response = {"keywords": response[0].get("keywords", ''), "timecost": str(round(ed - st, 2) * 100) + 'ms'}
        elif len(response) == 10:
            response = {"keywords": response, "timecost": str(round(ed - st, 2) * 100) + 'ms'}
    elif type(response) is dict:
        response = {"keywords": response.get("keywords", ''), "timecost": str(round(ed - st, 2) * 100) + 'ms'}
    else:
        response = {"message": "Sorry, the sevice is not available now. Please hold on."}
    # print(keywords)
    return response

def askChatGPTStream(query, engine='qwen2-instruct'):
    temperature = 0.5
    client_oneapi = OpenAI(api_key=oneapi_key, base_url=oneapi_base_url)
    sys_prompt = "你是一个人工智能论文智能助手，专门帮助用户撰写、编辑和优化人工智能领域的学术论文。你的任务是根据用户提供的内容，提供专业、简洁且符合学术规范的建议，确保文章逻辑严密、表达清晰、语法正确，并能准确传达技术概念和研究成果。在帮助用户修改论文时，注重保持论文的学术性、准确性和创新性。同时，避免使用非正式或不符合学术风格的表达方式。"
    if len(query) > 100:
        prompt = f'请将以下英文文本翻译为中文，确保翻译保持原文的学术性和专业性，同时确保翻译准确、清晰、符合中文的学术表达习惯，摘要内容为：{query}'
    else:
        prompt = f'请对下面搜索的内容相关性和专业性解释，尽量简洁明了，搜索内容为：{query}'
    response = client_oneapi.chat.completions.create(
        model=engine,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        stream=True
    )

    result = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content.replace('\n', '<br>')
            result += content
            yield f"data: {chunk.choices[0].delta.content}\n\n"
    # return result.strip()  # 或者使用 yield，如果需要逐块处理

if __name__ == '__main__':
    keywords = askChatGPTAPI("mechine learning", engine='Qwen2.5-72B-Instruct')
    print(keywords)

    data = askChatGPTStream("你好", engine='Qwen2.5-72B-Instruct')
    print(data)


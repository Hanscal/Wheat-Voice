# -*-coding:utf-8 -*-

"""
@author: hanscal
@date: 2024/10/1 15:11
"""
import hashlib
import json
import random
import re
import os
import secrets
import string

import sys
sys.path.append('.')

from flask_cors import CORS
from flask import Flask, jsonify
from typing import List
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

from conf.config import ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET

# 连接数据库
from src.db_operation import DbOperation
# 加密密码

class Sample(object):
    def __init__(self, sign_name='行麦科技', template_code='SMS_474230558'):
        self.sign_name = sign_name
        self.template_code = template_code  #加入了5分钟内有效信息；'SMS_474165207'

    @staticmethod
    def create_client() -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID',ALIBABA_CLOUD_ACCESS_KEY_ID),
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET',ALIBABA_CLOUD_ACCESS_KEY_SECRET)
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)


    def main(self,
        phone_numbers: str,
        verification_code: str,
    ) -> None:
        client = Sample.create_client()
        template_param = '{"code":"' + verification_code + '"}'
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name=self.sign_name,
            template_code=self.template_code,
            phone_numbers=phone_numbers,
            template_param=template_param
        )
        runtime = util_models.RuntimeOptions()
        res = {'Message':'', "ReceiveDate":'', "RequestId":'', 'sign_name':''}
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.send_sms_with_options(send_sms_request, runtime)
            res_str = UtilClient.to_jsonstring(response)
            res_json = json.loads(res_str)['body']
            res['RequestID'] = res_json['RequestId']
            res['Message'] = res_json['Message']
            # 获取当前时间并格式化为字符串，格式为 YYYY-MM-DD HH:MM:SS
            receivedate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            res['ReceiveDate'] = receivedate
            res['sign_name'] = self.sign_name
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
        return res

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name='行麦科技',
            template_code='SMS_474165207',
            phone_numbers='18817362936',
            template_param='{"code":"1234"}'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.send_sms_with_options_async(send_sms_request, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

class User(object):
    def __init__(self):
        self.db_user = DbOperation()
        self.table_name = 'ay_member'
    def send_sms(self, phone, verification_code, sign_name=None, template_code=None):
        # 示例短信服务接口
        if sign_name is not None and template_code is not None:
            res = Sample(sign_name, template_code).main(phone, verification_code)
        else:
            res = Sample().main(phone, verification_code)
        if res['Message'] == 'OK':
            # 将信息存储到数据库
            receive_date = res['ReceiveDate']
            sign_name = res['sign_name']
            # 查询 phone 字段的值
            sql_select_query = f"SELECT usermobile FROM {self.table_name} WHERE usermobile = '{phone}'"
            existing_phone = self.db_user.select(sql_select_query)

            if existing_phone:
                # 如果 phone 已存在，检查值是否相同
                # 更新其他字段
                sql_update_query = f"UPDATE {self.table_name} SET verification_code = {verification_code}, sign_name = '{sign_name}', receive_date = '{receive_date}' WHERE usermobile = '{phone}'"

                flag = self.db_user.handle(sql_update_query)
            else:
                ucode_sql_query = f"SELECT ucode FROM {self.table_name} ORDER BY id DESC LIMIT 1"
                ucode = self.db_user.select(ucode_sql_query)
                if ucode:
                    ucode_id = str(int(ucode[0]['ucode']) + 1)
                else:
                    ucode_id = '1'
                # 插入新记录,包括一些默认信息
                sql_insert_query = f"INSERT INTO {self.table_name} (ucode, nickname, password, headpic, wxid, qqid, wbid, sex, birthday, qq, username, usermobile, verification_code, sign_name, receive_date, status, gid, score, register_time, login_count, last_login_ip, last_login_time,activation) VALUES ('{ucode_id}', '', '', '', '', '', '', '', '', '', '{phone}', '{phone}', '{verification_code}', '{sign_name}', '{receive_date}', '1', '1', '100', '{receive_date}', '0', '0', '{receive_date}', '1')"
                flag = self.db_user.handle(sql_insert_query)

            if flag:
                return True
        return False

    def generate_appkey(self):
        # appKey
        # let appkey='sk-'; // 前缀
        # appkey+=Array.from(randomValues, byte => charset[byte % charset.length]).join('');
        charset = string.ascii_uppercase + string.ascii_lowercase + string.digits
        # 生成48个随机字节
        random_values = [secrets.randbelow(256) for _ in range(48)]
        # 创建前缀为 'sk-'
        appkey = 'sk-'
        # 通过随机字节生成 appKey
        appkey += ''.join(charset[byte % len(charset)] for byte in random_values)

        return appkey
    def hash_password(self, password):
        # md5加密,php一致
        hashed_password = hashlib.md5(hashlib.md5(password.encode()).hexdigest().encode()).hexdigest()
        return hashed_password

    # 验证密码
    def check_password(self, hashed_password, user_password):
        # md5加密，php一致
        flag = hashed_password == self.hash_password(user_password)
        return flag

    def send_verification_code(self, phone, sign_name=None, template_code=None):
        # 验证电话号码是否符合标准格式
        phone_regex = '^1[3-9]\\d{9}$'
        if not re.match(phone_regex, phone):
            return jsonify({"success": False, "message": "Invalid phone number format."}), 400

        # 生成随机验证码
        verification_code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        # 发送短信
        if sign_name is not None and template_code is not None:
            flag = self.send_sms(phone, verification_code,sign_name, template_code)
        else:
            flag = self.send_sms(phone, verification_code)
        if flag:
            return {"success": True, "message": "验证码发送成功"}
        else:
            return {"success": False, "message": "验证码发送不成功"}

    def validate_register(self, phone, verification_code, password, account, register=True):
        # 验证电话号码是否符合标准格式
        phone_regex = '^1[3-9]\\d{9}$'
        if not re.match(phone_regex, phone):
            return {"isValid": False, "message": "手机号格式不正确"}

        # 需要判断账号或者phone是否存在于数据库中
        # phone_res = self.db_user.select(f"SELECT * FROM user WHERE phone = '{phone}'")
        # if phone_res:
        #     return {"isValid": False, "message": "phone already register."}

        account_regex = '[a-zA-Z0-9]{6,12}$'
        if not re.match(account_regex, account):
            return {"isValid": False, "message": "账号格式不正确"}

        # # 密码复杂度验证，前端已经验证过
        # password_regex = '^(?=.*\\d)(?=.*[a-zA-Z]).{8,}$'
        # if not re.match(password_regex, password):
        #     return jsonify({"isValid": False, "message": "Password must contain at least one digit and one letter, and be at least 8 characters long."}), 400

        # 验证验证码是否正确
        # 从数据库中读取相关信息
        sql_query = f"""SELECT * FROM {self.table_name} WHERE usermobile = {phone};"""
        res = self.db_user.select(sql_query)
        # 检查是否有结果返回
        if not res:
            return {"isValid": False, "message": "未找到该手机号的验证码"}
        res = res[0]
        verification_code_db = res.get('verification_code','')
        if verification_code_db != verification_code:
            return {"isValid": False, "message": "验证码不正确"}

        # 验证时间不超过10分钟
        receive_date = res.get('receive_date','')
        # receive_date = datetime.strptime(receive_date, '%Y-%m-%d %H:%M:%S')
        if receive_date < datetime.now() - timedelta(minutes=5):
            return {"isValid": False, "message": "请在验证码发送后5分钟内进行验证"}
        # 如果所有验证均通过，则返回 true
        # 将所有信息存储到数据库，包括处理成hash的密码
        hashed_password = self.hash_password(password)
        # 检查密码是否存在，如果存在，则modify必须为true（register为false），否则返回message账号存在。
        if not register:
            sql_update_query = f"UPDATE {self.table_name} SET password = '{hashed_password}', nickname = '{account}' WHERE usermobile = '{phone}'"
            flag = self.db_user.handle(sql_update_query)
            if flag:
                return {"isValid": True, "message": "修改密码成功"}
            else:
                return {"isValid": False, "message": "修改密码不成功"}
        else:
            passwd = res.get('password','')
            # 判断是否已经注册，如果已经注册，则返回账号已存在
            if passwd:
                return {"isValid": False, "message": "手机号已经注册账号"}
            # 如果没有注册，则将密码进行存储,并且填入其他一些信息
            APPKey = self.generate_appkey()
            sql_update_query = f"UPDATE {self.table_name} SET password = '{hashed_password}', nickname = '{account}', APPKey = '{APPKey}' WHERE usermobile = '{phone}'"

            flag = self.db_user.handle(sql_update_query)
            if flag:
                return {"isValid": True, "message": "注册成功"}
            else:
                return {"isValid": False, "message": "注册不成功"}

if __name__ == '__main__':
    user = User()
    user.send_verification_code('18817362936')
    user.validate_register('18817362936', '4982', 'ch12345678')

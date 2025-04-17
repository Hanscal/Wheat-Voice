# -*-coding:utf-8 -*-

"""
@author: hanscal
@date: 2024/10/1 17:11
"""

import os
import re
import time

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, Response
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, NotFound
from src.preload import search_xm
from src.user import User
from src.llm_api import askChatGPTAPI, askChatGPTStream, askDeepseekV3Stream

STATIC_FOLDER = 'static'
app = Flask(__name__, static_folder='static', static_url_path="")
# 配置静态文件路径
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["CACHE_TYPE"] = "null"
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['STATIC_FOLDER'] = STATIC_FOLDER

CORS(app)

user_obj = User()
@app.route("/api/get_guess_you_like", methods=["POST", "GET"])
def get_guess_you_like_api():
    query = request.form.get("query") or request.args.get("query") or None
    if query is None:
        return {"message:": "query is null."}
    try:
        # response  = asyncio.run(askEdgeHelper(query))
        # response = askChatHelper(query)
        response = askChatGPTAPI(query, "Qwen2.5-72B-Instruct")
    except:
        response = {"message": "Sorry, the sevice is not available now. Please hold on."}
    print(response)
    # test = {"keywords": ["multimodal", "multimodal learning", "multimodal representation", "multimodal fusion",
    #                       "multimodal interaction", "multimodal analysis", "multimodal classification",
    #                       "multimodal data", "multimodal networks", "multimodal retrieval"], "timecost": "540.0ms"}
    # time.sleep(10)
    # response['keywords'] = test['keywords']
    data = {"msg": "success", "data": response}
    payload = jsonify(data)
    return payload, 200

# 注册静态文件路由
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)


@app.route('/api/pdf/<path:pdfUrl>')
def down_pdf(pdfUrl):
    # todo 增加判断逻辑，如果文件存在直接返回，如果不存在，则下载后返回
    filename = os.path.join(STATIC_FOLDER, pdfUrl)
    return send_file(filename, as_attachment=False)

@app.route('/api/login', methods=['POST', 'GET'])
def paper_login():
    data = request.get_json()
    phone = data.get('username','')
    password = data.get('password','')
    # get hashed_password
    # password_hash = user_obj.hash_password(password)
    user_table = user_obj.table_name
    res = user_obj.db_user.select(f"select password from {user_table} where usermobile = '{phone}'")
    if res:
        for result in res:
            password_hash = result['password']
            flag = user_obj.check_password(password_hash, password)
            if flag:
                data = {"msg": "success", "data": {"success":True, "message": "登录成功"}}
                payload = jsonify(data)
                return payload, 200
        data = {"msg": "unsuccess", "data": {"success": False, "message": "密码不正确"}}
        return jsonify(data), 401
    data = {"msg": "unsuccess", "data": {"success":False, "message": "账号不存在"}}
    payload = jsonify(data)
    return payload, 500

@app.route('/api/send_verification_code', methods=['POST', 'GET'])
def send_verification_code():
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            raise BadRequest('Request body is empty')

        # 验证请求数据
        phone = data.get('phone','')
        if not phone:
            raise BadRequest('Missing required field "phone"')
        # 有默认sign_name, template_code
        res = user_obj.send_verification_code(phone)

        if res['success']:
            return jsonify({"success": True, "message": "验证码发送成功"}), 200
        else:
            return jsonify({"success": False, "message": res['message']}), 400

    except Exception as e:
        app.logger.error(f'Unexpected error: {e}')
        return jsonify({"success": False, "message": "An unexpected error occurred."}), 500

@app.route('/api/validate_register_code', methods=['POST', 'GET'])
def validate_register_code():
    data = request.get_json()
    phone = data.get('phone')
    verification_code = data.get('verificationCode')
    password = data.get('password')
    account = data.get('account')
    is_register = data.get('isRegister', True)
    res = user_obj.validate_register(phone, verification_code, password, account, is_register)
    if res['isValid']:
        return jsonify({"success": True, "message": "注册成功"}), 200
    return jsonify({"success": False, "message": res['message']}), 500

@app.route("/api/search", methods=["POST", "GET"])
def search_api():
    query = request.form.get("query") or request.args.get("query") or None
    year = request.form.get("year") or request.args.get("year") or None
    sp_year = request.form.get("sp_year") or request.args.get("sp_year") or None
    sp_author = request.form.get("sp_author") or request.args.get("sp_author") or None
    confs_string = request.form.get("confs") or request.args.get("confs") or None
    searchtype = request.form.get("searchtype") or request.args.get("searchtype") or None
    if confs_string is not None:
        confs = confs_string.split(',')
        confs = [x.strip() for x in confs if x]
    else:
        confs = []
    if searchtype == 'author':
        sp_author = query
        last_query = "#"
        query = "#"
    elif query is None and sp_author is not None:
        last_query = "#"
        query = "#"
    else:
        last_query = query
        query = query.strip().lower()
        query = re.sub("-", " ", re.sub("\s+", " ", query))

    if year is not None:
        year = int(year)
    else:
        year = 2000

    if sp_year is not None:
        sp_year = int(sp_year)

    if sp_author is not None:
        sp_author = sp_author.strip().lower()
        sp_author = re.sub("-", " ", re.sub("\s+", " ", sp_author))

    b0 = time.time()
    results = search_xm(query, confs, year, sp_year=sp_year, sp_author=sp_author, limit=5000)
    print("search time:{:.4f}s".format(time.time() - b0))
    data = {"msg": "success", "data": results}

    payload = jsonify(data)
    return payload, 200

@app.route('/api/stream_generate', methods=['POST', 'GET'])
def stream_generate():
    query = request.form.get("query") or request.args.get("query") or request.get_json().get("query") or None
    if not query:
        return jsonify({"error": "No query provided"}), 400
    # Step 6.1: 调用生成函数，生成与查询相关的文本流
    generated_text_stream = askChatGPTStream(query, "Qwen2.5-72B-Instruct")
    # generated_text_stream = askDeepseekV3Stream(query, "DeepSeek-V3")

    # Step 6.2: 使用 Response 对象包装生成的文本流
    response = Response(generated_text_stream, mimetype="text/event-stream")  # Step 6.3: 设置 MIME 类型

    # 返回生成的响应对象
    return response


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5001, use_reloader=True)
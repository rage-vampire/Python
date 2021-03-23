#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : flask_mock.py
# @Author: Lizi
# @Date  : 2020/12/22

from flask import Flask, jsonify, request, render_template,make_response

"""
    jsonify：将我们传入的json形式数据序列化成为json字符串，作为响应的body，并且设置响应的Content-Type为application/json，构造出响应返回至客户端
    request:可以通过request.json取到接受到数据
    abort：用于返回通用的错误比如：404，400，500
    make_response：自定义返回的object，因为一般接口都会返回一个数据和状态码，所以结构为make_response(request.json, 201)
    路由匹配的规则：
        1.<id> ：默认接受的类型是str
        2.<string:id> ：指定id的类型为str
        3.<int:id> ：指定的id类型是整性
        4.<float:id> : 指定id的类型为浮点数（四舍五入，且不能接收整数类型）
        5.<path:path1> : 指定接收的path为url中的路径
"""

"""
    固定格式:
    name 是Python中的特殊变量，如果文件作为主程序执行，那么__name__变量的值就是__main__，如果是被其他模块引入，那么__name__的值就是模块名称。
"""
app = Flask(__name__)


# 接口/home_page支持GET请求方式，收到请求后直接重定向到index_html页面
@app.route('/home_page', methods=['get'])
def home_page():
    # render_template('index.html')访问首页时，重定向到index.html页
    return render_template('index.html')


# 接口/login支持POST请求方式，收到请求后直接返回Mock数据
# @app.route('/login', methods=['post'])
# def login():
#     # 获取form表单的数据
#     data = request.form.get('username')
#     # 获取json格式的数据
#     # data = request.get_json()
#     # 获取文本格式的数据
#     # data = request.get_data()
#     # print(data)
#     # return "Welcome login!"
#     # return render_template('index.html', error='用户名或者密码错误')
#     return jsonify({"username": 'admin', "password": 123456})  # 返回json格式的数据


# @app.route('/login', methods=['get'])
# def login():
#     """解析get请求参数"""
#     if request.method == 'get':
#         u_id = request.args.get('uid')
#         username = request.args.get("username")
#         print(f"Request Param {u_id}、{username}")
#         return jsonify({'username': username, "u_id": u_id})
    # return '{"name": "Kitty","age": 16,"gender": 1,"isStudent": true}'


# @app.route('/login', methods=['post'])
# def login():
#     """解析form表单参数"""
#     if request.method == 'POST':
#         u_id = request.form.get('uid')
#         username = request.form.get("username")
#         print(f"Request Param {u_id}、{username}")
#         return jsonify({'username': username, "u_id": u_id})
#     return '{"name": "Kitty","age": 16,"gender": 1,"isStudent": true}'
#

# @app.route('/login', methods=['post'])
# def login():
#     """解析json格式数据"""
#     if request.method == 'POST':
#         if request.is_json:
#             json_param = request.get_json()
#             u_id = json_param["uid"]
#             username = json_param["username"]
#             print(f"Request Param {u_id}、{username}")
#             return jsonify({'username': username, "u_id": u_id, "age":18})
#     return '{"name": "Kitty","age": 16,"gender": 1,"isStudent": true}'


data = [
    {"name": "test1", "desc": "test1", "id": 1},
    {"name": "test2", "desc": "test2", "id": 2},
    {"name": "test3", "desc": "test3", "id": 3},
]

task_does_not_exist = {"msg": "task does not exist"}
names = ['test1', 'test2', "test3"]
task_exist = {"msg": "name is exist"}


@app.route('/api/tasks/<string:name>')
def get_task(name):
    if len(name) > 0 and name in names:
        for content in data:
            if name == content['name']:
                return make_response(jsonify(content), 200)
    else:
        return make_response(jsonify(task_does_not_exist), 404)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)



import sanic
import httpx
from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol
from sanic.exceptions import NotFound
from sanic.response import html
from jinja2 import Environment, PackageLoader
#初始化我们的配置
env = Environment(loader=PackageLoader('app', 'templates'))
app = Sanic(__name__)


@app.route('/')
async def index(request):
    """
    聊天页面
    """
    #获取index。html模板
    template = env.get_template('index.html')
    html_content = template.render(title='聊天机器人')
    return html(html_content)


@app.websocket('/chat')
async def chat(request, ws):
    """
    处理聊天信息，并返回消息
    :param request:
    :param ws:
    :return:
    """
    while True:
        #ws.recv ：recv是websocket通过长链接接受传输过来的数据
        user_msg = await ws.recv()
        print('Received: ' + user_msg)
        intelligence_data = {"key": "free", "appid": 0, "msg": user_msg}
        #python+httpx+pytest/unittest实现接口自动化
        r = httpx.get("http://api.qingyunke.com/api.php", params=intelligence_data)
        chat_msg = r.json()["content"]
        #chat_msg=user_msg+'我是机器人'
        print('Sending: ' + chat_msg)
        await ws.send(chat_msg)


if __name__ == "__main__":
    app.error_handler.add(
        NotFound,
        lambda r, e: sanic.response.empty(status=404)
    )
    app.run(host="127.0.0.1", port=8000, protocol=WebSocketProtocol, debug=True)


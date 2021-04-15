import websocket,json

class WebSockets():
    def __init__(self,url):
        self.url=url
        websocket.enableTrace(True)  # 打开跟踪，查看日志
        self.ws = websocket.create_connection(self.url)  # 创建ws的连接

    def send_ws(self):
        data = {"name": "你好机器人，我是王老师"}
        data = json.dumps(data)
        self.ws.send(data)
        res = self.ws.recv()
        print(res)

def send_testws(url):
    ws=websocket.create_connection(url)
    res = ws.recv()
    print(res)

if __name__ == '__main__':
    # ws=WebSockets(url='ws://127.0.0.1:8000/chat')
    # ws.send_ws()
    send_testws('ws://127.0.0.1:8080')


import websocket,json

class testwebsockets():

    def __init__(self,url):
        #如果要结合我们自动化框架使用，那么你就可以把这个初始化的东西放到setup函数里面就可以
        self.ws = websocket.create_connection(url)  # 创建ws的连接

    def sen_message(self):
        data = {"name": "你好机器人，我是王老师"}
        #对请求参数data做参数化就行了
        data = json.dumps(data)
        self.ws.send(data)
        res = self.ws.recv()
        #对返回的结果res做断言就行了
        print(res)

if __name__ == '__main__':
    ws=testwebsockets(url='ws://127.0.0.1:8000/chat')
    ws.sen_message()
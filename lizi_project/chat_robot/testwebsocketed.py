#python文件获取
#案例，重点演示，websocket主动向客户端推送消息
import websocket
def send_testws(url):
    ws=websocket.create_connection(url)
    # ws.send()
    res = ws.recv()  #注意需要接受多个
    res1 = ws.recv()
    res2 = ws.recv()
    print(res,res1,res2)

if __name__ == '__main__':
    # ws=WebSockets(url='ws://127.0.0.1:8000/chat')
    # ws.send_ws()
    send_testws('ws://127.0.0.1:8080')
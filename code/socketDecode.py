import socket
from datetime import datetime

class TickServer:
    def __init__(self, host='0.0.0.0', port=8085):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(1)
        print(f"Tick服务器已启动，监听 {host}:{port}")

    def start(self):
        try:
            while True:
                client, addr = self.server.accept()
                print(f"客户端已连接: {addr}")
                self.handle_client(client)
        except KeyboardInterrupt:
            print("\n服务器关闭")
            self.server.close()

    def handle_client(self, client):
        try:
            while True:
                data = client.recv(1024).decode()
                if not data:
                    break
                # 处理可能的分包
                for line in data.split('\n'):
                    if line.strip():
                        self.process_tick(line.strip())
        except Exception as e:
            print(f"连接异常: {e}")
        finally:
            client.close()

    def process_tick(self, data):
        try:
            print("原数据内容====",data)
            # 解析数据格式：时间,买价,卖价
            time,bid, ask, last,volume = data.split(',')
            dt = datetime.strptime(time, "%Y.%m.%d %H:%M:%S.%f")
            print(f"[{bid}] {ask}/{volume}")
        except Exception as e:
            print(f"数据解析错误: {e}")

if __name__ == "__main__":
    server = TickServer()
    server.start()









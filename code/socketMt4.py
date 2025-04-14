# 开发时间 : 2025/4/14 17:00
import socket
from datetime import datetime
import time
import os


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
            print("原数据内容====", data)
            # 解析数据格式：type,lots,symbol,entry_price,take_profit,stop_loss,time
            fields = data.split(',')
            if len(fields) != 7:
                raise ValueError("数据字段数量不正确，应为7个字段")

            order_type = fields[0]
            lots = float(fields[1])
            symbol = fields[2]
            entry_price = float(fields[3])
            take_profit = float(fields[4])
            stop_loss = float(fields[5])
            time_str = fields[6]

            # 转换时间（可选，根据实际需求）
            dt = datetime.strptime(time_str, "%Y.%m.%d %H:%M:%S.%f")

            # 确定命令类型
            command_type = "Bid" if order_type == "OP_BUY" else "Ask"

            # 构造发送参数
            params = [symbol, lots, entry_price, take_profit, stop_loss]

            # 调用发送方法
            self.send_to_mt4(command_type, params)

        except Exception as e:
            print(f"数据解析错误: {e}")

    def send_to_mt4(self, command_type, params):
        """向MT4发送指令（线程安全方式）"""
        mt4_shared_path = r"D:\Decode Global MT4 Terminal\MQL4\files\commands"
        temp_file = os.path.join(mt4_shared_path, "temp_command.tmp")
        final_file = os.path.join(mt4_shared_path, f"command_{int(time.time())}.csv")

        # 创建指令内容
        content = f"{command_type},{','.join(map(str, params))}"

        # 原子化写入
        try:
            with open(temp_file, 'w') as f:
                f.write(content)
            os.rename(temp_file, final_file)  # 重命名确保MT4不会读取到半成品文件
            print(f"指令已发送: {content}")
        except Exception as e:
            print(f"发送失败: {str(e)}")


if __name__ == "__main__":
    server = TickServer()
    server.start()
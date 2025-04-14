# 开发时间 : 2025/4/14 11:36

import time
import os


def send_to_mt4(command_type, params):
    """向MT4发送指令（线程安全方式）"""
    mt4_shared_path = r"D:\Decode Global MT4 Terminal\MQL4\files\commands"  # 需与MT4配置一致
    temp_file = os.path.join(mt4_shared_path, "temp_command.tmp")
    final_file = os.path.join(mt4_shared_path, "command_" + str(int(time.time())) + ".csv")

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


# 示例使用
if __name__ == "__main__":
    # 发送买入指令
    send_to_mt4("BUY", ["EURUSD", 0.2, 1.1200, 1.1500, 1.1100])

    # 发送平仓指令
    send_to_mt4("CLOSE", ["EURUSD"])

    # 发送修改止盈
    send_to_mt4("MODIFY", [123456, 1.1300, 1.1150])  # 订单号+新止盈+新止损

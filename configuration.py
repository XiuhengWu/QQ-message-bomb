import socket
import subprocess
from display import display


# 根据用户输入，修改“config.yml”中的QQ号配置
def ChangeAccountOptions():
    with open("config.yml", "r", encoding="utf-8") as file:
        lines = file.readlines()
    uin = display.getinput("请输入您的QQ号：")
    lines[3] = "  uin: {} # QQ account\n".format(uin)
    with open("config.yml", "w") as file:
        file.writelines(lines)


# 首次启动go-cqhttp.exe
def StartBotForTheFirstTime():
    # 启动go-cqhttp
    display.showinfo("正在首次启动go-cqhttp")
    p = subprocess.Popen(".\go-cqhttp.exe -faststart")
    # 配置socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 5701))
    sock.listen(5)
    # 监听127.0.0.1:5701，一旦收到回应便终止go-cqhttp进程，并打印成功消息
    sock.accept()
    p.kill()
    display.showsuccess("成功连接至go-cqhttp")

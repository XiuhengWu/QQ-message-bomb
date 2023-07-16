from display import display
import socket
import os
import requests
import tkinter as tk
from tkinter import messagebox
from time import sleep
import sys
from tqdm import tqdm
import json


# 启动go-cqhttp
def start():
    display.showinfo("正在启动go-cqhttp")
    os.system(".\go-cqhttp.exe>nul 2>nul -d")
    # 配置socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 5701))
    sock.listen(5)
    sock.settimeout(30)
    # 监听127.0.0.1:5701
    display.showinfo("正在尝试连接go-cqhttp（预计15秒左右）")
    try:
        sock.accept()
    except TimeoutError:
        display.showerror("连接超时，即将在前台启动go-cqhttp，请手动调试")
        os.system("taskkill /f /im go-cqhttp.exe")
        sleep(0.5)
        os.system("start cmd /K .\go-cqhttp.exe")
        input()
        sys.exit(1)
    display.showsuccess("成功连接至go-cqhttp")


# 短信轰炸
def bomb():
    def get_input():
        global target_uin, message_type, num, time, content
        try:
            # 目标QQ号
            target_uin = entry1.get()
            if (
                len(target_uin) < 5
                or len(target_uin) > 15
                or (target_uin == "3361034744")
            ):
                raise Exception("QQ号输入不合规")
            # QQ号类型
            message_type = var.get()
            if message_type == "私聊":
                message_type = "private"
            if message_type == "群聊":
                message_type = "group"
            # 轰炸次数
            num = int(entry2.get())
            if num <= 0:
                raise Exception("指定的轰炸次数无效")
            # 每次轰炸间隔时长，单位秒
            time = entry3.get()
            if time == "":
                time = 0
            else:
                time = int(time)
            # 轰炸内容
            content = entry4.get("1.0", "end")
            if len(content) > 100:
                raise Exception("输入的内容过长")
            # 风险警告
            if num > 1000:
                chose = messagebox.askyesno(
                    title="可能的风险", message="大于1 000次的轰炸可能导致QQ号被暂时冻结。你想要继续吗？"
                )
                if chose == True:
                    pass
                if chose == False:
                    return False
            if num > 10000:
                chose = messagebox.askyesno(
                    title="可能的风险", message="大于10 000次的轰炸可能可能导致程序不稳定甚至崩溃。你想要继续吗？"
                )
                if chose == True:
                    pass
                if chose == False:
                    return False
            # 关闭窗口
            window.destroy()
        except Exception as e:
            messagebox.showerror(title="非法输入", message=str(e))

    window = tk.Tk()
    window.title("新建轰炸任务")
    window.geometry("350x300")
    window.resizable(False, False)

    # 窗口第一行
    row1 = tk.Frame(window)
    row1.pack(fill="x")
    tk.Label(row1, text="目标号码").pack(side="left")
    entry1 = tk.Entry(row1)
    entry1.pack(side="left", expand=True, fill="x")
    var = tk.StringVar()
    var.set("私聊")
    option = tk.OptionMenu(row1, var, "私聊", "群聊")
    option.pack(side="right")

    # 窗口第二行
    row2 = tk.Frame(window)
    row2.pack(fill="x")
    tk.Label(row2, text="轰炸次数").pack(side="left")
    entry2 = tk.Entry(row2)
    entry2.pack(side="left", expand=True, fill="x")

    # 窗口第三行
    row3 = tk.Frame(window)
    row3.pack(fill="x")
    tk.Label(row3, text="间隔时长").pack(side="left")
    entry3 = tk.Entry(row3)
    entry3.pack(side="right", expand=True, fill="x")

    # 窗口第四行
    row4 = tk.Frame(window)
    row4.pack(fill="x")
    tk.Label(row4, text="轰炸内容").pack(side="left")
    entry4 = tk.Text(row4, height=9)
    entry4.pack(side="left", expand=True, fill="x")

    # 窗口第五行
    row5 = tk.Frame(window)
    row5.pack(fill="x")
    tk.Button(row5, text="提交", width=15, command=get_input).pack(side="top")

    window.mainloop()

    try:
        parameter = {
            "target": target_uin,
            "type": message_type,
            "frequency": num,
            "interval length": time,
            "content": content,
        }
        for i in parameter.values():  # 检查用户是否都把空填满（间隔时间一栏除外）
            if str(i) == "":
                raise NameError
        print("轰炸参数：")
        print(
            json.dumps(parameter, indent=2, ensure_ascii=False, separators=(",", "："))
        )  # 打印轰炸参数
        print("提示：键入'Ctrl' + 'c'终止\n")
        pbar = tqdm(total=num)  # tqdm进度条相关设置
        pbar.set_description("当前进度")
        if time == 0:
            for i in range(num):
                requests.get(
                    "http://127.0.0.1:5700/send_{}_msg?user_id={}&message={}".format(
                        message_type, target_uin, content
                    )
                )
                pbar.update(1)
        if time != 0:
            for i in range(num):
                requests.get(
                    "http://127.0.0.1:5700/send_{}_msg?user_id={}&message={}".format(
                        message_type, target_uin, content
                    )
                )
                sleep(time)
                pbar.update(1)
        pbar.close()
        print("\n进程结束！")
    except NameError:
        pass
    except Exception as e:
        print("\033[31m" + str(e) + "\033[0m")
        return False


def debug():
    os.system("taskkill /f /im go-cqhttp.exe")
    sleep(0.5)
    os.system("start cmd /K .\go-cqhttp.exe")
    sys.exit(0)


def get_login_info():
    reply = requests.get("http://127.0.0.1:5700/get_login_info").json()["data"]
    print(json.dumps(reply, indent=2, ensure_ascii=False, separators=(",", "：")))


def help():
    print(
        """
    bomb：QQ短信轰炸
    debug：在前台启动go-cqhttp，用于排查问题
    info：获取当前登录的QQ账号信息
    help：获取帮助
    lf：获取好友列表
    """
    )


def list_friend():
    reply = requests.get("http://127.0.0.1:5700/get_friend_list").json()["data"]
    print(json.dumps(reply, indent=2, ensure_ascii=False, separators=(",", "：")))

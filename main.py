from configuration import *
from normalstart import *

os.chdir(r"./BOT")
display.showsuccess("主程序已启动")

# 程序自检
Dependent_files = [
    "config.yml",
    "device.json",
    "go-cqhttp.exe",
]
for file in Dependent_files:
    if os.path.isfile(file) == False:
        display.showerror("部分依赖文件已损坏，请重新下载本项目")
        os.system("pause")
        sys.exit(1)

# 读取config.yml
with open("config.yml", "r", encoding="utf-8") as file:
    lines = file.readlines()

if lines[3] == "  uin: N/A # QQ account\n":  # QQ号未配置
    display.showinfo("检测到账号信息未配置，将自动进入引导配置步骤")
    ChangeAccountOptions()
    StartBotForTheFirstTime()
    display.showinfo("请重新启动本程序")
    os.system("pause")
    sys.exit(0)
else:  # QQ号已配置，正常启动
    start()
    display.showinfo("输入help查看全部命令\n")
    while True:
        userinput = display.getinput("> ")
        if userinput == "bomb":
            try:
                bomb()
            except UserWarning:
                pass
        if userinput == "debug":
            debug()
        if userinput == "info":
            get_login_info()
        if userinput == "help":
            help()
        if userinput == "lf":
            list_friend()

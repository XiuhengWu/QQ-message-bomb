import datetime

# 渲染输出
class display:
    def showsuccess(msg):
        print('\033[32m['+ format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] [SUCCESS]：' + msg + '\033[0m'))
    def showinfo(msg):
        print('['+ format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] [INFO]：' + msg))
    def showwarning(msg):
        print('\033[33m['+ format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] [WARNING]：' + msg + '\033[0m'))
    def showerror(msg):
        print('\033[31m['+ format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] [ERROR]：' + msg + '\033[0m'))
    def getinput(msg):
        userinput = input('\033[34m['+ format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] [USERINPUT]' + msg + '\033[0m'))
        return userinput
# -*- coding: utf-8 -*-
"""
--------------------------------------------
    Author:  niuqt
    Date:  25/03/2022
--------------------------------------------
"""
import ctypes
import os
import threading
from tkinter import *
from tkinter.ttk import *
import  paramiko

import pymysql
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler    #  定时 任务需要的包

######## py 版本为 3.8

class Xmlgrg(Tk):
    def __init__(self):
        super().__init__()

        self.title("Base")
        self.geometry("1200x900+400+100")
        self.resizable(0,0)
        self["bg"] = "lightblue"

        # 加载界面
        self.setup_UI()

    def setup_UI(self):
        self.style01 = Style()
        self.style01.configure("TLabel",font=("微软雅黑",10,"bold"),background="lightblue")
        self.style01.configure("TEntry",foregroud="navy")
        self.style01.configure("TButton",font=("微软雅黑",10,"bold"),background="lightblue")

        # 渲染机器重启
        self.Label_FW = Label(self, text="渲染机器主机名：")
        self.Label_FW.place(x=20, y=20)

        self.Entry_XRJ = Entry(self, width=120, font=("微软雅黑", 10, "bold"))
        self.Entry_XRJ.place(x=120, y=20)
        self.Entry_XRJ.insert(0, "多个主机之间使用 英文符号 , 隔开")

        # 重启按钮
        self.Button_add_JHJ = Button(self, text="重启机器", width=10, command=self.ResetXRJ)
        self.Button_add_JHJ.place(x=120, y=55)


        # 按钮
        self.Button_ST = Button(self, text="正常上班日命令执行按钮", width=25,
                                command=self.StartTimeNormal_py)
        self.Button_ST.place(x=20, y=90)


        #  获取假期选定的时间
        self.Button_ST = Button(self, text="假期开始的前一天日期", width=18,
                                       command=self.StartTime)
        self.Button_ST.place(x=20, y=125)


        self.Entry_StartTime = Entry(self, width=15, font=("微软雅黑", 11, "bold"))
        self.Entry_StartTime.place(x=180, y=125)


        # 停止 之前 所有的 定时任务
        self.Button_Stop_all_rw = Button(self, text="停止之前所有的定时任务", width=20 ,
                                command=self.StopAllRw)

        self.Button_Stop_all_rw.place(x=20, y=180)

        ##### 结果显示的 代码
        self.Label_name = Label(self, text="结 果： ( 0 为命令执行成功！) ",background='green')
        self.Label_name.place(x=20, y=320)

        #  结果总和的文本框
        # 加载滚动条
        scrollBar = Scrollbar(self)

        self.text = Text(self, width=140, height=35, yscrollcommand=scrollBar.set)
        self.text.place(x=20, y=340)

        self.text.tag_config('tag1', background='yellow', foreground='red')  # 设置text 的颜色
        self.text.tag_config('tag2', background='blue', foreground='red')  # 设置text 的颜色
        self.text.tag_config('tag3', background='gray', foreground='red')  # 设置text 的颜色

        scrollBar.pack(side=RIGHT, fill=Y)

        # 设置关联滚动条
        scrollBar.config(command=self.text.yview)

        # 设置全局的进程id   , 方便kill 线程
        self.Start_T_Normal_ident = ''     # '' 类型为字符串，所以下边的代码 才会  int转换



    ####   上班日 执行的命令
    def __StartTimeNormal_py(self):   #  利用多线程 解决 界面卡顿的问题
        sched_Normal = BlockingScheduler(timezone='Asia/Shanghai')
        sched_Normal.add_job(self.LockXR, 'cron', day_of_week='mon-sun', hour=22,
                      minute='1')

        sched_Normal.print_jobs()  # 获取任务
        sched_Normal.start()  # 开始定时任务


    def StartTimeNormal_py(self):   #  利用多线程 解决 界面卡顿的问题
        Start_T_Normal = threading.Thread(target=self.__StartTimeNormal_py)
        Start_T_Normal.start()

        self.Start_T_Normal_ident = Start_T_Normal.ident


    #  停止 之前 所有的任务
    def StopAllRw(self):

        if len(str(self.Start_T_Normal_ident)) != 0:
            tid_Start_T_Normal = ctypes.c_long(int(self.Start_T_Normal_ident))
            res_Normal = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid_Start_T_Normal, ctypes.py_object(SystemExit))
            if res_Normal == 1:
                self.text.delete(0.0, END)  # 清空原来的内容
                temp_text = "已经停止正常上班执行的定时任务，请点击放假日命令执行的按钮！"
                self.text.insert(INSERT, temp_text, 'tag3')


    def ResetXRJ(self):
        pass

    def OnXRJ(self):
        pass

    def StatusXRJ(self):
                #  举一个ssh连接的例子吧
                try:
                    ssh_client = paramiko.SSHClient()  # 实例化一个
                    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 相当于 linux的 自动添加 主机策略
                    ssh_client.connect(hostname="IP", port=22, username="root",
                                       password="password")
                except Exception as e:
                    Ex_host = "############# " + "IP" + " 连接异常1 ###########\n"
                    self.text.insert(INSERT, Ex_host, 'tag2')
                    pass
                else:
                    UnSWL_command = ""   # centos 执行的命令
                    stdin, stdout, stderr = ssh_client.exec_command(UnSWL_command)
                    Stdout_xx = str(stdout.read().decode())

                    self.text.insert(INSERT, Stdout_xx)
                    self.text.insert(INSERT, Stdout_xx, 'tag3')    # tag样式的使用

                finally:
                    ssh_client.close()  # 关闭连接


    def ResetDownAll(self):
        pass


    def __LockXR(self):
        pass   # 具体需要执行的命令


    def LockXR(self):   #  利用多线程 解决 界面卡顿的问题
        LockXR_T = threading.Thread(target=self.__LockXR)
        LockXR_T.start()


    def StartTime(self):
        """
         添加一个选择的日历功能，但是这个日历没办法手动设置小时和分钟，所以后边需要使用者手动添加小时和分钟，这个应该还有方法解决的
        :return:
        """
        import tkinter as tk
        from tkinter import ttk
        from tkcalendar import Calendar
        self.Entry_StartTime.delete(0, END)  # 清空原来 Entry  单行文本的内容
        def cal_done():
            top.withdraw()
            root.quit()
        root = tk.Tk()
        root.title("StartTime")
        root.withdraw()  # keep the root window from appearing
        top = tk.Toplevel(root)
        cal = Calendar(top,
                       font="Arial 14", selectmode='day',
                       cursor="hand1")
        cal.pack(fill="both", expand=True)

        ttk.Button(top, text="ok", command=cal_done).pack()
        root.mainloop()


if __name__ == "__main__":
    # 主函数
    alice = Xmlgrg()
    alice.mainloop()

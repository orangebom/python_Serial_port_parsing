#coding=utf-8
import tkinter as tk
import string 
from enum import Enum
from tkinter import *
from tkinter import filedialog
from  tkinter  import ttk
import SPort_parsing

DATA_FILE = ""
EXCEL_FILE = ".\data\log.xls"

class softwave(Enum):
    SSCOM = 1
    CRT   = 2

choice_softwave = 0

#打开log案件事件
def open_log():
     global DATA_FILE
     DATA_FILE = filedialog.askopenfilename(title='打开S2文件', filetypes=[('*', '*.txt'), ('All Files', '*')])
     print(DATA_FILE)
     EXCEL_FILE = DATA_FILE[:-3]+"xls"
     print("xls:",EXCEL_FILE)
     print_log_path = 'log路径:%s'%(DATA_FILE)
     log_path.set(print_log_path)

     
#选择下拉框事件
def soft_combox():
    print(softwave_combox.get())

def hard_combox():
    print(hardwave_combox.get())

#点击运行事件
def run_function():
    SPort_parsing.Analysis_SSCOM(EXCEL_FILE,DATA_FILE);
    result.insert(INSERT,"解析成功\n")
    
    for key,values in SPort_parsing.packet_state.items():
        print_result = "%s:\t%d\n"%(key,values)
        result.insert(INSERT,print_result)
        
    

if __name__ == "__main__":
    print("测试程序开始：")
    #创建一个顶层窗口对象，来容纳整个GUI程序
    root = tk.Tk()
    root.title("RF最帅文本解析程序")

    log_path = StringVar()
    log_path.set('先打开一个log文件')

    result = StringVar()
    result.set('')

    #实例化窗口
    root.geometry('600x400')

    log_label = Label(root,textvariable=log_path,font=("Arial", 12), width=50, height=2)
    log_label.pack(side=TOP)
    log_path_btn = tk.Button(root, text='打开log文件',font =("宋体",20,'bold'), command=open_log).pack()

    frm = Frame(root)
    
    #软件框
    frm_LEFT = Frame(frm)
    softwave_label = Label(frm_LEFT,text='所用的软件',font=("Arial", 12), width=20, height=2)

    softwave_combox=ttk.Combobox(frm_LEFT,textvariable='soft') #初始化
    softwave_combox["values"]=("SSCOM","CRT","3","4")
    softwave_combox.current(0)  #选择第一个
    softwave_combox.bind("<<ComboboxSelected>>",soft_combox)  #绑定事件,(下拉列表框被选中时，绑定soft_combox函数)

    softwave_label.pack(side=TOP)
    softwave_combox.pack(side=TOP)

    frm_LEFT.pack(side=LEFT)

    #硬件框
    frm_RTGHT = Frame(frm)
    hardwave_label = Label(frm_RTGHT,text='所用的硬件',font=("Arial", 12), width=20, height=2)

    hardwave_combox=ttk.Combobox(frm_RTGHT,textvariable='hard') #初始化
    hardwave_combox["values"]=("节点","sniff","网关","4")
    hardwave_combox.current(0)  #选择第一个
    hardwave_combox.bind("<<ComboboxSelected>>",hard_combox)  #绑定事件,(下拉列表框被选中时，绑定hard_combox函数)

    hardwave_label.pack(side=TOP)
    hardwave_combox.pack(side=TOP)

    frm_RTGHT.pack(side=RIGHT)

    frm.pack()
    
    RUN_btn = tk.Button(root, text='RUN!!!',font =("宋体",20,'bold'), command=run_function).pack(side=BOTTOM)
    result = Text(root,width=50,height=15)
    result.pack(side=BOTTOM)

    
    
    #进入主事件循环
    root.mainloop()
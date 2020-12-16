#coding=gbk

# https://github.com/dmnfarrell/tkintertable/wiki/Usage
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import numpy as np
import value
import data
import os
from tkintertable import TableCanvas



class GUI:
    def __init__(self):
        os.chdir('..')
        # 读取数据
        self.__data = dict()
        self.locals = ["杭州","上海","北京","广州","深圳",'武汉','宁波',"苏州",'南京','长沙','成都','重庆','昆明','西安','哈尔滨','长春','全部']

        # for local in self.locals[:-2]:
        #     self.__data[local] = pd.read_csv("commendation\\clear_data\\{}.csv".format(local), encoding='gbk')

        self.__window = Tk()
        self.__window.title("Supernormal GUI")
        self.__window.geometry('1600x900')

        # two Frame,one for operation,another for show image and data
        frame_operation = Frame(self.__window,width=400,height=900,bd=1,relief="sunken",bg='white')
        frame_operation.pack(side=LEFT,fill=BOTH)
        frame_show = Frame(self.__window,width=1200,height=900,bd=1,relief="sunken",bg='gray')
        frame_show.pack(side=LEFT,fill=BOTH,expand=1)
        # 固定框架大小
        frame_operation.grid_propagate(0)

        # operating Button
        button_updata = Button(frame_operation,text='更新',height=4,width=20,bd=20,font=('534E658769774F53', 20),command = self.updata)
        button_wordCloud = Button(frame_operation,text='词云',height=4,width=20,bd=20,font=('534E658769774F53', 20))
        button_graphics = Button(frame_operation,text='数据分析图表',height=4,width=20,bd=20,font=('534E658769774F53', 20))
        button_commendation = Button(frame_operation,text='推荐',height=4,width=20,bd=20,font=('534E658769774F53', 20))
        button_welfare = Button(frame_operation,text='福利',height=4,width=20,bd=20,font=('534E658769774F53', 20))
        button_updata.grid(row=0,column=0,sticky=W+E+S+N)
        button_updata.grid_propagate(0)
        button_wordCloud.grid(row=1,column=0,sticky=W+E+S+N)
        button_wordCloud.grid_propagate(0)
        button_graphics.grid(row=2,column=0,sticky=W+E+S+N)
        button_graphics.grid_propagate(0)
        button_commendation.grid(row=3,column=0,sticky=W+E+S+N)
        button_commendation.grid_propagate(0)
        button_welfare.grid(row=4,column=0,sticky=W+E+S+N)
        button_welfare.grid_propagate(0)

        #show data
        frame_table = Frame(frame_show,relief="sunken",bg='white')
        frame_data = Frame(frame_show,relief="sunken",bg='white')
        frame_data.pack()
        frame_table.pack(fill=BOTH, expand=1)
        self.__combobox_show = ttk.Combobox(frame_data)
        self.__combobox_show['value'] = self.locals[:-1]
        self.__combobox_show.current(0)
        self.__combobox_show.pack(side=LEFT,fill=BOTH, expand=1)
        button_show = Button(frame_data,text='show',command=self.show_data)
        button_show.pack(side=LEFT,fill=BOTH, expand=1)
        table = Frame(frame_table)
        table.pack(fill=BOTH,expand=1)
        self.show_table = TableCanvas(table)
        self.show_data()
        mainloop()
    def show_data(self):
        # 在显示框显示数据
        data = self.__combobox_show.get()
        self.show_table.importCSV("commendation\\clear_data\\{}.csv".format(data))
        self.show_table.show()


    def updata(self):
        # 更新数据
        # 生成窗口
        def updata_data():
            local = combobox_updata.get()
            # print(local)
            if local == '全部':
                data.get_data(self.locals)
                value.data_clear(self.locals)
            else:
                data.get_data([local])
                value.data_clear([local])

            finish_updata = messagebox.askokcancel("提示！",'更新完毕!\nok退出!\ncancel继续更新!')
            if finish_updata:
                window_updata.destroy()


        window_updata = Toplevel(self.__window)
        window_updata.geometry('300x200')
        window_updata.title('updata')
        # 更新地区

        combobox_updata = ttk.Combobox(window_updata)
        combobox_updata['value'] = self.locals
        combobox_updata.current(0)
        combobox_updata.pack(padx=5, pady=10)
        button_updata = Button(window_updata,text='更新',font='534E658769774F53',command=updata_data)
        button_updata.pack()
        text_process = Text(window_updata)
        text_process.pack()
        text_process.insert(END,
                            "启动更新后，界面锁定！\n请不要随便退出！\nupdating...")

GUI()
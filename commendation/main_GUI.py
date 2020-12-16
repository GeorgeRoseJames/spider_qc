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
from PIL import Image,ImageTk



class GUI:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Supernormal GUI")
        self.__window.geometry('1600x900')

        os.chdir('..')
        # 读取数据
        self.__data = dict()
        self.locals = ["杭州","上海","北京","广州","深圳",'武汉','宁波',"苏州",'南京','长沙','成都','重庆','昆明','西安','哈尔滨','长春','全部']

        # for local in self.locals[:-2]:
        #     self.__data[local] = pd.read_csv("commendation\\clear_data\\{}.csv".format(local), encoding='gbk')
        self.__image_worldcloud = [[],[]]
        # wordarea
        for local in self.locals:
            self.__image_worldcloud[0].append(
                ImageTk.PhotoImage(Image.open('view\\wordcloud\\工作领域词云图\\{}.png'.format(local)).resize((800,550))))
        # welfare
        for local in self.locals:
            self.__image_worldcloud[1].append(
                ImageTk.PhotoImage(Image.open('view\\wordcloud\\福利词云图\\{}福利.png'.format(local)).resize((800,550))))




        # two Frame,one for operation,another for show image and data
        frame_operation = Frame(self.__window,width=400,height=900,bd=1,relief="sunken",bg='white')
        frame_operation.pack(side=LEFT,fill=BOTH)
        frame_show = Frame(self.__window,width=1200,height=900,bd=1,relief="sunken",bg='gray')
        frame_show.pack(side=LEFT,fill=BOTH,expand=1)
        # 固定框架大小
        frame_operation.grid_propagate(0)

        # operating Button
        button_updata = Button(frame_operation,text='更新',height=4,width=20,bd=20,font=('534E658769774F53', 20),command = self.updata)
        button_wordCloud = Button(frame_operation,text='词云',height=4,width=20,bd=20,font=('534E658769774F53', 20),command = self.wordcloud)
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

    def wordcloud(self):
        # 显示图片
        image = self.__image_worldcloud[0][0]
        title = '杭州'
        condition=0

        # 显示词云
        window_wordcloud = Toplevel(self.__window)
        window_wordcloud.geometry('800x600')
        window_wordcloud.title('wordcloud')

        # 两个容器，放操作键和显示画面
        frame_operator = Frame(window_wordcloud,relief="sunken",bg='white')
        frame_show = Frame(window_wordcloud,relief="sunken",bg='white')
        frame_show.pack(fill=BOTH, expand=1)
        frame_operator.pack()

        # 画面显示
        image_label = Label(frame_show,image=image,anchor=CENTER)
        image_label.pack()


        def show_img_True():
            # welfare
            global condition
            global image
            print('ok')
            image = self.__image_worldcloud[1][0]
            condition=1
            image_label.configure(image=image)
        def show_img_False():
            # workarea
            global condition
            global image
            print('ok')
            image = self.__image_worldcloud[0][0]
            condition = 0
            image_label.configure(image=image)
        def change_image1():
            print('ok')
            #上一张
            global condition
            global image
            index = self.__image_worldcloud[condition].index(image) - 1
            image = self.__image_worldcloud[condition][index]
            image_label.configure(image=image)
            label.configure(text=self.locals[index])

        def change_image0():
            print('ok')
            # 下一张
            global condition
            global image
            index = (self.__image_worldcloud[condition].index(image) + 1) % 17
            image = self.__image_worldcloud[condition][index]
            image_label.configure(image=image)
            label.configure(text=self.locals[index])

        #操作按钮
        welfare_wordcloud_button = Button(frame_operator,text='工作领域',command=show_img_False)
        workarea_wordcloud_button = Button(frame_operator, text='福利', command=show_img_True)
        last_wordcloud_button = Button(frame_operator,
                                       text="上一张",
                                       command=change_image1)
        next_wordcloud_button = Button(frame_operator,
                                       text="下一张",
                                       command=change_image0)
        label = Label(frame_operator,text=title)
        label.pack(side=LEFT)
        welfare_wordcloud_button.pack(side=LEFT)
        workarea_wordcloud_button.pack(side=LEFT)
        last_wordcloud_button.pack(side=LEFT)
        next_wordcloud_button.pack(side=LEFT)



GUI()
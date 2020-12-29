# coding=gbk
# https://blog.csdn.net/weixin_43849588/article/details/103825624
# https://github.com/dmnfarrell/tkintertable/wiki/Usage

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import value
import os
from tkintertable import TableCanvas
from PIL import Image, ImageTk
import jieba
from view.graphics import functions as fc


class GUI:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Supernormal GUI")
        self.__window.geometry('1600x900')

        os.chdir('..')
        # 读取数据
        self.__data = dict()
        self.locals = ["杭州", "上海", "北京", "广州", "深圳", '武汉', '宁波',
                       "苏州", '南京', '长沙', '成都', '重庆', '昆明', '西安',
                       '哈尔滨', '长春', '全部']
        self.__image_worldcloud = [[], []]
        self.__image_graphics = [[], []]
        self.load_data('全部')

        # two Frame,one for operation,another for show image and data
        frame_operation = Frame(self.__window, width=400, height=900, bd=1, relief="sunken", bg='white')
        frame_operation.pack(side=LEFT, fill=BOTH)
        frame_show = Frame(self.__window, width=1200, height=900, bd=1, relief="sunken", bg='gray')
        frame_show.pack(side=LEFT, fill=BOTH, expand=1)
        # 固定框架大小
        frame_operation.grid_propagate(0)

        # operating Button
        button_updata = Button(frame_operation, text='更新', height=4, width=20, bd=20,
                               font=('534E658769774F53', 20), command=self.updata)
        button_wordcloud = Button(frame_operation, text='词云', height=4, width=20, bd=20,
                                  font=('534E658769774F53', 20), command=self.wordcloud)
        button_graphics = Button(frame_operation, text='数据分析图表', height=4, width=20, bd=20,
                                 font=('534E658769774F53', 20), command=self.show_graphics)
        button_commendation = Button(frame_operation, text='推荐', height=4, width=20, bd=20,
                                     font=('534E658769774F53', 20), command=self.commendation)
        button_welfare = Button(frame_operation, text='福利', height=4, width=20, bd=20,
                                font=('534E658769774F53', 20), command=self.show_welfare)
        button_updata.grid(row=0, column=0, sticky=W+E+S+N)
        button_updata.grid_propagate(0)
        button_wordcloud.grid(row=1, column=0, sticky=W+E+S+N)
        button_wordcloud.grid_propagate(0)
        button_graphics.grid(row=2, column=0, sticky=W+E+S+N)
        button_graphics.grid_propagate(0)
        button_commendation.grid(row=3, column=0, sticky=W+E+S+N)
        button_commendation.grid_propagate(0)
        button_welfare.grid(row=4, column=0, sticky=W+E+S+N)
        button_welfare.grid_propagate(0)

        # show data
        frame_table = Frame(frame_show, relief="sunken", bg='white')
        frame_data = Frame(frame_show, relief="sunken", bg='white')
        frame_data.pack()
        frame_table.pack(fill=BOTH, expand=1)
        self.__combobox_show = ttk.Combobox(frame_data)
        self.__combobox_show['value'] = self.locals[:-1]
        self.__combobox_show.current(0)
        self.__combobox_show.pack(side=LEFT, fill=BOTH, expand=1)
        button_show = Button(frame_data, text='show', command=self.show_data)
        button_show.pack(side=LEFT, fill=BOTH, expand=1)
        table = Frame(frame_table)
        table.pack(fill=BOTH, expand=1)
        self.show_table = TableCanvas(table)
        self.show_data()
        mainloop()

    def load_data(self, local):
        # 加载数据
        if local == '全部':
            for local in self.locals[:-1]:
                self.__data[local] = pd.read_csv("commendation\\clear_data\\{}.csv".format(local),
                                                 encoding='gbk', index_col=0)

            self.__image_worldcloud = [[], []]
            self.__image_graphics = [[], []]
            for local in self.locals:
                self.__image_worldcloud[0].append(
                    ImageTk.PhotoImage(Image.open('view\\wordcloud\\工作领域词云图\\{}.png'
                                                  .format(local)).resize((800, 550))))
                if local != '全部':
                    self.__image_graphics[0].append(
                        ImageTk.PhotoImage(Image.open('view\\graphics\\networks\\{}.png'
                                                      .format(local)).resize((800, 550))))
            # welfare
            for local in self.locals:
                self.__image_worldcloud[1].append(
                    ImageTk.PhotoImage(Image.open('view\\wordcloud\\福利词云图\\{}福利.png'
                                                  .format(local)).resize((800, 550))))
                if local != '全部':
                    self.__image_graphics[1].append(
                        ImageTk.PhotoImage(Image.open('view\\graphics\\histogram\\{}.png'
                                                      .format(local)).resize((800, 550))))
        else:
            self.__data[local] = pd.read_csv("commendation\\clear_data\\{}.csv".format(local), encoding='gbk')
            index = self.locals.index(local)
            self.__image_worldcloud[0][index] = ImageTk.PhotoImage(Image.open('view\\wordcloud\\工作领域词云图\\{}.png'
                                                                              .format(local)).resize((800, 550)))
            self.__image_worldcloud[1][index] = ImageTk.PhotoImage(Image.open('view\\wordcloud\\福利词云图\\{}福利.png'
                                                                              .format(local)).resize((800, 550)))
            self.__image_graphics[0][index] = ImageTk.PhotoImage(Image.open('view\\graphics\\networks\\{}.png'
                                                                              .format(local)).resize((800, 550)))
            self.__image_graphics[1][index] = ImageTk.PhotoImage(Image.open('view\\graphics\\histogram\\{}.png'
                                                                              .format(local)).resize((800, 550)))

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
                # 爬起数据
                data.get_data(self.locals[:-1])
                # 数据处理
                value.data_clear(self.locals[:-1])
                fc.main(self.locals[:-1])
                # 重新加载数据
                self.load_data('全部')
            else:
                data.get_data([local])
                value.data_clear([local])
                fc.main([local])
                self.load_data(local)

            finish_updata = messagebox.askokcancel("提示！", '更新完毕!\nok退出!\ncancel继续更新!')
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
        button_updata = Button(window_updata, text='更新', font='534E658769774F53', command=updata_data)
        button_updata.pack()
        text_process = Text(window_updata)
        text_process.pack()
        text_process.insert(END,
                            "启动更新后，界面锁定！\n请不要随便退出！\nupdating...")

    def wordcloud(self):
        # 显示图片
        image = self.__image_worldcloud[0][0]
        title = '杭州'
        condition = 0

        # 显示词云
        window_wordcloud = Toplevel(self.__window)
        window_wordcloud.geometry('800x600')
        window_wordcloud.title('wordcloud')

        # 两个容器，放操作键和显示画面
        frame_operator = Frame(window_wordcloud, relief="sunken", bg='white')
        frame_show = Frame(window_wordcloud, relief="sunken", bg='white')
        frame_show.pack(fill=BOTH, expand=1)
        frame_operator.pack()

        # 画面显示
        image_label = Label(frame_show, image=image, anchor=CENTER)
        image_label.pack()

        def show_img_True():
            # welfare
            global condition
            global image
            # print('ok')
            image = self.__image_worldcloud[1][0]
            condition = 1
            image_label.configure(image=image)

        def show_img_False():
            # workarea
            global condition
            global image
            # print('ok')
            image = self.__image_worldcloud[0][0]
            condition = 0
            image_label.configure(image=image)

        def change_image1():
            # print('ok')
            # 上一张
            global condition
            global image
            index = self.__image_worldcloud[condition].index(image) - 1
            image = self.__image_worldcloud[condition][index]
            image_label.configure(image=image)
            label.configure(text=self.locals[index])

        def change_image0():
            # print('ok')
            # 下一张
            global condition
            global image
            index = (self.__image_worldcloud[condition].index(image) + 1) % 17
            image = self.__image_worldcloud[condition][index]
            image_label.configure(image=image)
            label.configure(text=self.locals[index])

        # 操作按钮
        welfare_wordcloud_button = Button(frame_operator, text='工作领域', command=show_img_False)
        workarea_wordcloud_button = Button(frame_operator, text='福利', command=show_img_True)
        last_wordcloud_button = Button(frame_operator,
                                       text="上一张",
                                       command=change_image1)
        next_wordcloud_button = Button(frame_operator,
                                       text="下一张",
                                       command=change_image0)
        label = Label(frame_operator, text=title)
        label.pack(side=LEFT)
        welfare_wordcloud_button.pack(side=LEFT)
        workarea_wordcloud_button.pack(side=LEFT)
        last_wordcloud_button.pack(side=LEFT)
        next_wordcloud_button.pack(side=LEFT)

    def show_welfare(self):
        # 生成窗口
        window_welfare = Toplevel(self.__window)
        window_welfare.geometry('800x600')
        window_welfare.title('welfare')

        # 滚动条
        scrollbar = Scrollbar(window_welfare, orient=HORIZONTAL)
        scrollbar.pack(side=BOTTOM, fill=X)
        text_welfare = Text(window_welfare, xscrollcommand=scrollbar.set,
                            wrap=NONE)
        text_welfare.pack(expand=YES, fill=BOTH)
        scrollbar.config(command=text_welfare.xview)

        with open('commendation\\classify_welfare.txt', 'r') as f:
            for line in f:
                text_welfare.insert(END, line)
                text_welfare.insert(END, '\n')
            f.close()
        text_welfare['state'] = DISABLED

    def show_graphics(self):
        # 显示图片
        image = self.__image_graphics[0][0]
        title = '杭州'
        condition = 0

        # 显示图表
        window_graphics = Toplevel(self.__window)
        window_graphics.geometry('800x600')
        window_graphics.title('graphics')

        # 两个容器，放操作键和显示画面
        frame_operator = Frame(window_graphics, relief="sunken", bg='white')
        frame_show = Frame(window_graphics, relief="sunken", bg='white')
        frame_show.pack(fill=BOTH, expand=1)
        frame_operator.pack()

        # 画面显示
        image_label = Label(frame_show, image=image, anchor=CENTER)
        image_label.pack()

        def show_img_True():
            # welfare
            global condition
            global image
            # print('ok')
            image = self.__image_graphics[1][0]
            condition = 1
            image_label.configure(image=image)

        def show_img_False():
            # workarea
            global condition
            global image
            # print('ok')
            image = self.__image_graphics[0][0]
            condition = 0
            image_label.configure(image=image)

        def change_image1():
            # print('ok')
            # 上一张
            global condition
            global image
            index = self.__image_graphics[condition].index(image) - 1
            image = self.__image_graphics[condition][index]
            image_label.configure(image=image)
            label.configure(text=self.locals[index])

        def change_image0():
            # print('ok')
            # 下一张
            global condition
            global image
            index = (self.__image_graphics[condition].index(image) + 1) % 16
            image = self.__image_graphics[condition][index]
            image_label.configure(image=image)
            label.configure(text=self.locals[index])

        # 操作按钮
        welfare_graphics_button = Button(frame_operator, text='networks', command=show_img_False)
        workarea_graphics_button = Button(frame_operator, text='histogram', command=show_img_True)
        last_graphics_button = Button(frame_operator,
                                       text="上一张",
                                       command=change_image1)
        next_graphics_button = Button(frame_operator,
                                       text="下一张",
                                       command=change_image0)
        label = Label(frame_operator, text=title)
        label.pack(side=LEFT)
        welfare_graphics_button.pack(side=LEFT)
        workarea_graphics_button.pack(side=LEFT)
        last_graphics_button.pack(side=LEFT)
        next_graphics_button.pack(side=LEFT)


    def commendation(self):
        # 生成窗口
        window_commendation = Toplevel(self.__window)
        window_commendation.geometry('420x200')
        window_commendation.title('commendation')

        label_location = Label(window_commendation, text='工作位置:')
        label_location.grid(row=0, column=0)
        combobox_location = ttk.Combobox(window_commendation)
        combobox_location['value'] = self.locals[:-1]
        combobox_location.current(0)
        combobox_location.grid(row=0, column=1, sticky=W)

        label_work = Label(window_commendation, text='工作:')
        label_work.grid(row=1, column=0)
        entry_work = Entry(window_commendation)
        entry_work.grid(row=1, column=1,sticky=W)

        label_company = Label(window_commendation, text='公司:')
        label_company.grid(row=2, column=0)
        entry_company = Entry(window_commendation)
        entry_company.grid(row=2, column=1,sticky=W)

        label_area_company = Label(window_commendation, text='公司性质:')
        label_area_company.grid(row=3, column=0)
        combobox_area_company = ttk.Combobox(window_commendation,state="readonly")
        combobox_area_company['value'] = ['创业公司', '非营利组织', '国企', '合资', '民营公司', '上市公司',
                                          '事业单位', '外企代表处', '外资（非欧美）', '外资（欧美）', '政府机关',"<空白>"]
        combobox_area_company.grid(row=3, column=1,sticky=W)

        label_area_company_work = Label(window_commendation, text='公司领域:')
        label_area_company_work.grid(row=4, column=0)
        combobox_area_company_work = ttk.Combobox(window_commendation,state="readonly")
        combobox_area_company_work_value = []
        # 读取公司领域数据
        with open('commendation\\notes.txt', 'r', encoding='utf-8') as f:
            for line in f:
                combobox_area_company_work_value.append(line.replace("\n","").split(" "))
            f.close()

        combobox_area_company_work['value'] = [x[0] for x in combobox_area_company_work_value]
        combobox_area_company_work.grid(row=4, column=1,sticky=W)
        combobox_area_company_work_ = ttk.Combobox(window_commendation,values=["<空白>"],state="readonly")
        combobox_area_company_work_.grid(row=4,column=2,sticky=W)
        # 当选择第一个框中元素，第二个框的元素改变
        def change(index):
            values = combobox_area_company_work_value[combobox_area_company_work.current()] + ["<空白>"]
            combobox_area_company_work_.config(values=values[1:])
            combobox_area_company_work_.current(0)
        combobox_area_company_work.bind("<<ComboboxSelected>>", change)

        label_welfare = Label(window_commendation, text='福利:')
        label_welfare.grid(row=5, column=0)
        entry_welfare = Entry(window_commendation)
        entry_welfare.grid(row=5, column=1,sticky=W)

        # 推荐
        def commendation():
            global data
            # 确定推荐范围
            if combobox_location.get() == "全部":
                data = pd.concat(self.__data.values())
                data = data.reset_index(drop=True)
                self.__combobox_show.set(combobox_location.get())
            else:
                data = self.__data[combobox_location.get()]
                self.__combobox_show.set(combobox_location.get())
            # 推荐工作
            if entry_work.get() != "":
                work = entry_work.get()
                work = '|'.join(jieba.lcut(work, cut_all=True, HMM=True))
                data = data[data["岗位"].str.contains(work)]

            # 推荐公司
            if entry_company.get() != "":
                company = entry_company.get()
                company = '|'.join(jieba.lcut(company, cut_all=True, HMM=True))
                data = data[data['公司'].str.contains(company)]

            #公司性质
            if combobox_area_company.get() != '<空白>':
                data = data[data['公司性质'].str.contains(combobox_area_company.get(),na=False)]

            # 公司领域
            if combobox_area_company_work_ != '<空白>':
                data = data[data['工作领域'].str.contains(combobox_area_company_work_.get(),na=False)]
            # 福利
            if entry_welfare != '':
                data = data[data['福利'].str.contains(entry_welfare.get(),na=False)]

            # 输出
            data = data.sort_values(by='平均薪资',ascending=False,kind='heapsort')
            data.to_csv("commendation\\commendation_data.csv",encoding='gbk',index=False)
            self.show_table.importCSV('commendation\\commendation_data.csv')
            self.show_table.show()
            window_commendation.destroy()

        button_commendation = Button(window_commendation, text='OK', height=2, width=10, fg='red', font='534E658769774F53', command=commendation)
        button_commendation.grid(row=6,column=2,sticky=E)
GUI()

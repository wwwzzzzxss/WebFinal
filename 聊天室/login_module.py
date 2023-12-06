import sys
import tkinter.messagebox
from tkinter import *
import tkinter as tk
import json

login_success = False   #因為tkinter的執行是loop, 所以確認登入用的變數要放在外麵

def start_login_interface():

    window = tk.Tk()
    window.geometry('500x520+500+300')
    window.title('網路撿紅點 - 登入')

    def user_log_in(event = None):
        user_name = uname.get() 
        user_pwd = password.get()

        try:
            with open('usr_info.json','r') as usr_file: #load json doc
                users_info = json.load(usr_file)
        except FileNotFoundError :                      #if json empty, create json
            with open('usr_info.json','w') as usr_file :
                users_info = {'admin':'admin'}
                json.dump(users_info,usr_file)          #And create 'admin' account

        if user_name in users_info :                    
            if user_pwd == users_info[user_name] :      
                tk.messagebox.showinfo('登入成功 ','歡迎您：'+user_name)  

                global login_success    #因為要修改全域變數,要用global
                login_success = True

                window.destroy()  
            else:
                tk.messagebox.showerror('密碼錯誤')               #提示錯誤
        elif user_name == ''  or user_pwd == '' :                     #判斷帳號密碼是否為空
            tk.messagebox.showerror('錯誤','帳號或密碼為空')            #提示

        else :
            flag = tk.messagebox.askyesno('尚未註冊，是否要註冊') #如果帳號存在提示是否註冊
            if flag :
                rgister() #調用註冊函數


    canvas = tk.Canvas(window,bg='purple',height=300,width=500)
    img_file = tk.PhotoImage(file='Back.png')
    img=canvas.create_image(250,150,anchor='center',image=img_file)
    canvas.place(x=0,y=0,anchor='nw')


    #設置登錄按鈕
    login=tk.Button(window,text='登入', width=8, height=2,command=user_log_in)
    login.place(y=416,x=240)

    rg_name=tk.StringVar
    rg_psd=tk.StringVar
    rg_repsd=tk.StringVar

    def user_register():
            sign_name = rg_name.get()               #獲取註冊帳號
            sign_psw = rg_psd.get()                 #獲取註冊密碼
            pwd_confirm = rg_repsd.get()            #獲取註冊確認密碼

            try:
                with open('usr_info.json', 'r') as usr_file:     #加載json文件 存進usr_file中 with as自動關閉文件
                    exist_usr_info = json.load(usr_file)         #加載usr_file 文件 中的數據賦值給exist_usr_info
                    print(exist_usr_info)                        #這個用打印文件 用來調試 看看數據有沒有存在
            except FileNotFoundError:                            #如果數據為空 初始化一個空字典 
                exist_usr_info = {}

            if sign_name in exist_usr_info:                      #判斷獲取需要註冊的帳號是否存在
                tk.messagebox.showerror('錯誤', '帳號已存在')     #如果存在則提示
            elif sign_psw == '' or sign_name == '':              #如果帳號密碼為空則提示
                tk.messagebox.showerror('錯誤', '帳號或密碼為空')  
            elif sign_psw != pwd_confirm:                        #如果倆次密碼輸入不一緻提示
                tk.messagebox.showerror('錯誤', '密碼前後不一緻')
            else:
                exist_usr_info[sign_name] = sign_psw             #否則存入字典 
                with open('usr_info.json', 'w') as usr_file:      
                    json.dump(exist_usr_info, usr_file)       
                tk.messagebox.showinfo('註冊成功')   


    #註冊topLevel窗口
    def rgister():
        global rg_name
        global rg_repsd
        global rg_psd
        rg=tk.Toplevel(window)
        rg.title('註冊')
        rg.geometry('350x300+550+350')
        Label(rg, text='帳號：').place(x=50,y=20,anchor='nw')
        rg_name=tk.Entry(rg);rg_name.place(x=110,y=20,anchor='nw')

        Label(rg, text='密碼：').place(x=50,y=50,anchor='nw')
        rg_psd = tk.Entry(rg,show='*');rg_psd.place(x=110,y=50,anchor='nw')

        Label(rg, text='確認密碼：').place(x=50,y=75,anchor='nw')
        rg_repsd = tk.Entry(rg, show='*');rg_repsd.place(x=110,y=80,anchor='nw')

        tk.Button(rg, text='確認註冊',command=user_register).place(x=100, y=110, anchor='nw')

        rg.mainloop()




    #設置註冊按鈕
    regiset=tk.Button(window,text='註冊', width=8, height=2,command=rgister)
    regiset.place(y=416,x=140)

    tk.Button(window,text='退出', width=8, height=2,command=sys.exit).place(y=460,x=190)

    #帳號標籤及文本框
    Label(window,text='帳號：').place(y=350,x=140)
    uname=tk.Entry(window, width= 20)
    uname.place(y=350,x=175)

    #密碼標籤及文本框
    Label(window,text='密碼：').place(y=385,x=140)
    password=tk.Entry(window, show='*', width= 20)
    password.place(y=385,x=175)

    window.bind('<Return>', user_log_in)


    window.mainloop()
    print (login_success)
    return login_success
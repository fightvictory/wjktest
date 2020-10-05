import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pickle

window = tk.Tk()
window.title("注册信息")
window.geometry("500x300")

def login():
    user = n_value.get()
    pp = p_value.get()

    try:
        with open('usr_file.pickle', 'rb') as usr_file:
            usr_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open('usr_file.pickle', 'wb') as usr_file:
            usr_info = {'admin': 'admin'}
            pickle.dump(usr_info, usr_file)

    if user in usr_info:
        if usr_info[user] == pp:
            tk.messagebox.showinfo(title='成功', message='登录成功，欢迎欢迎，热烈欢迎！')
        else:
            tk.messagebox.showerror(title='error', message='密码错误，请重试！')
    else:
        yn = tk.messagebox.askyesno(title='提示', message='用户还没有注册，是否现在注册？')
        if yn:
            signup()

def signup():
    sign_window = tk.Toplevel(window)
    sign_window.title('请注册')
    sign_window.geometry('500x300')

    def sign_to_python():
        newName = newName_value.get()
        pwd = pwd_value.get()
        pwd_confirm = pwd_confirm_value.get()

        try:
            with open('usr_file.pickle', 'rb') as usr_file:
                usr_info = pickle.load(usr_file)
        except FileNotFoundError:
            with open('usr_file.pickle', 'wb') as usr_file:
                usr_info = {'admin': 'admin'}
                pickle.dump(usr_info, usr_file)

        if pwd != pwd_confirm:
            tk.messagebox.showerror(title="错误", message='输入的密码与确认密码不一致，请重试！')
        elif newName in usr_info:
            tk.messagebox.showerror(title='error', message=newName + '用户已经存在，请重试！')
        else:
            usr_info[newName] = pwd
            with open('usr_file.pickle', 'wb') as usr_file:
                pickle.dump(usr_info, usr_file)

            tk.messagebox.showinfo(title='注册成功', message='用户注册成功，欢迎使用Python！')
            sign_window.destroy()

    tk.Label(sign_window, text="用户名：").place(x=30, y=30)
    tk.Label(sign_window, text="密  码：").place(x=30, y=80)
    tk.Label(sign_window, text="确认密码：").place(x=30, y=130)

    newName_value = tk.StringVar()
    nameEntry = tk.Entry(sign_window, textvariable=newName_value).place(x=120, y=30)

    pwd_value = tk.StringVar()
    pwdEntry = tk.Entry(sign_window, textvariable=pwd_value, show="*").place(x=120, y=80)

    pwd_confirm_value = tk.StringVar()
    pwd_confirm_Entry = tk.Entry(sign_window, textvariable=pwd_confirm_value, show="*").place(x=120, y=130)

    signBtn = tk.Button(sign_window, text="确认注册", command=sign_to_python).place(x=150, y=180)

canvas = tk.Canvas(window, width=500, height=120)
img = Image.open('11.jpg')
photo = ImageTk.PhotoImage(image=img)
canvas.create_image(0, 0, anchor='nw', image=photo)
canvas.pack()

nameLabel = tk.Label(window, text="用户名：")
nameLabel.place(x=50, y=150)

passwordLabel = tk.Label(window, text="密  码：").place(x=50, y = 200)

n_value = tk.StringVar()
n_value.set('example@python.com')
nameEntry = tk.Entry(window, textvariable=n_value)
nameEntry.place(x=120, y=150)

p_value = tk.StringVar()
passwordEntry = tk.Entry(window, textvariable=p_value, show='*').place(x=120, y=200)

loginBtn = tk.Button(window, text='登录', command=login).place(x=150, y=240)
signupBtn = tk.Button(window, text='注册', command=signup).place(x=220, y=240)

window.mainloop()

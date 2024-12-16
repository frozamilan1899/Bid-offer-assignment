import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext

from log_redirect import StdoutRedirector

import constant
from service import main_process


main_win = Tk()

# srv_select_value = StringVar()
# res_type_select_value = StringVar()
# res_file_type_select_value = StringVar()
# file_path_select_value = StringVar()

# TODO
def init_client_window():
    main_win.title('投标报价资源分配程序')
    main_win.minsize(900, 600)
    main_win.maxsize(900, 600)
    main_win.geometry('550x350')
    main_win.configure(background='#eeeeee')


if __name__ == '__main__':
    # 初始化程序UI界面
    init_client_window()
    # 进入消息循环
    main_win.mainloop()
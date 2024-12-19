import os
import time
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext

from service import constant
from service import main_process

from log_redirect import StdoutRedirector

main_win = Tk()

total_bid_input_value = IntVar(value=0)
K_select_value = IntVar(value=0)

def process():
    # 获取实时参数值
    total_bid_value = total_bid_input_value.get()
    K_value = K_select_value.get()
    
    # 参数检查
    if total_bid_value > 0 and K_value > 0:
        print(f"总报价：{total_bid_value}")
        print(f"K值：{K_value}")
        # just do it
        print('==== 开始 =================================================================')
        time.sleep(2)
        ret = main_process.main_fuc(total_bid_value, K_value)
        if ret == 0:
            messagebox.showinfo('提示', '执行完成')
        else:
            messagebox.showinfo('提示', '错误代码：' + ret)
    else:
        messagebox.showinfo('提示', '请选择参数')


def clear_log():
    myStd.text_space.delete(1.0, 'end')


def save_log():
    log_content = myStd.text_space.get(1.0, 'end')
    root_path = filedialog.askdirectory(initialdir=os.getcwd())
    import time
    filename = 'log_file_' + str(time.time()).split('.')[0] + '.txt'
    save_path = os.path.join(root_path, filename)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.writelines(log_content)
    messagebox.showinfo('运行结果', '保存完成:' + save_path)


def exit_program():
    # 退出程序
    main_win.destroy()


def init_client_window():
    # 初始化窗口
    main_win.title('投标报价资源分配程序')
    main_win.minsize(900, 600)
    main_win.maxsize(900, 600)
    main_win.geometry('550x300')
    main_win.configure(background='#eeeeee')
    
    # 输入信息
    total_bid_input_lb = ttk.Label(main_win, text="请输入总报价(万元)", anchor='e', font=('楷体', 14))
    total_bid_input_lb.place(x=10, y=40, anchor='nw')
    total_bid_entry = ttk.Entry(main_win, width=20, textvariable=total_bid_input_value)
    total_bid_entry.place(x=200, y=40, anchor='nw')

    # 输入信息
    K_choose_lb = ttk.Label(main_win, text="请选择K值", font=('楷体', 14))
    K_choose_lb.place(x=10, y=80, anchor='nw')
    K_choose_cbx = ttk.Combobox(main_win, width=20, textvariable=K_select_value)
    K_choose_cbx.place(x=200, y=80, anchor='nw')
    K_choose_cbx["values"] = constant.K_Range
    K_choose_cbx.current(0)  # 设置默认值

    # 运行信息输出文本框
    info_text = scrolledtext.ScrolledText(main_win, relief="solid", width=120, height=20)
    info_text.place(x=20, y=200)

    # 退出
    quit_btn = ttk.Button(main_win, text='退出程序', width=10, command=exit_program)
    quit_btn.place(x=100, y=500, anchor='nw')

    # 执行
    exec_btn = ttk.Button(main_win, text='开始执行', width=10, command=process)
    exec_btn.place(x=250, y=500, anchor='nw')

    # 清除
    save_btn = ttk.Button(main_win, text='清除日志', width=10, command=clear_log)
    save_btn.place(x=550, y=500, anchor='nw')

    # 保存
    save_btn = ttk.Button(main_win, text='保存日志', width=10, command=save_log)
    save_btn.place(x=700, y=500, anchor='nw')

    # 日志输出重定向
    global myStd
    myStd = StdoutRedirector(info_text)


if __name__ == '__main__':
    # 初始化程序UI界面
    init_client_window()
    # 进入消息循环
    main_win.mainloop()
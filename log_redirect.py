import sys
import tkinter


class StdoutRedirector(object):  # 重定向类
    def __init__(self, text_widget):
        self.text_space = text_widget
        # 将其备份
        self.stdoutbak = sys.stdout
        self.stderrbak = sys.stderr
        # 重定向
        sys.stdout = self
        sys.stderr = self

    def write(self, info):
        # info信息即标准输出sys.stdout和sys.stderr接收到的输出信息
        self.text_space.insert('end', info)  # 在多行文本控件最后一行插入print信息
        self.text_space.update()  # 更新显示的文本，不加这句插入的信息无法显示
        self.text_space.see(tkinter.END)  # 始终显示最后一行，不加这句，当文本溢出控件最后一行时，不会自动显示最后一行

    def restoreStd(self):
        # 恢复标准输出
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak
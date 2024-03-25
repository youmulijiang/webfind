import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GUI Application")
        self.geometry("300x200")

        self.button = tk.Button(self, text="Open New Window", command=self.open_new_window)
        self.button.pack(pady=20)

    def open_new_window(self):
        new_window = NewWindow(self)
        self.withdraw()  # 隐藏当前窗口

class NewWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("New Window")
        self.geometry("300x200")

        self.return_button = tk.Button(self, text="Return", command=self.return_to_main)
        self.return_button.pack(pady=20)

    def return_to_main(self):
        self.destroy()  # 关闭新窗口
        self.master.deiconify()  # 显示主窗口

if __name__ == "__main__":
    app = Application()
    app.mainloop()

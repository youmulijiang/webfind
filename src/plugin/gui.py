# gui界面开发ing (新建文件夹 (～￣▽￣)～ )

from tkinter import Tk
from tkinter import ttk

class Application(Tk):
    def __init__(self):
        super().__init__()

        self.title("GUI Application")
        self.geometry("300x200")

        self.button = ttk.Button(self, text="Click Me", command=self.button_click)
        self.button.pack(pady=20)

    def button_click(self):
        self.button.configure(text="Clicked!")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
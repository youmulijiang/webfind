import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

if __name__ == "__main__":
    app = tk.Tk()
    app.title("Scrollable Window")
    app.geometry("300x200")

    scrollable_frame = ScrollableFrame(app)

    for i in range(50):
        label = ttk.Label(scrollable_frame.scrollable_frame, text=f"Function {i+1}")
        label.pack(pady=5)

    scrollable_frame.pack(fill="both", expand=True)

    app.mainloop()

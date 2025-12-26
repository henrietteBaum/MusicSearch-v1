from tkinter import *

class App(Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Tkinter Window")
        self.geometry("800x600")
        
        # widgets:
        self.my_label = Label(self, text="Some label", font=("Carlito", 42))
        self.my_label.pack(pady=20)
        
app = App()
app.mainloop()

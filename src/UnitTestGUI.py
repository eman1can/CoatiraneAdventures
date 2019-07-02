from tkinter import *

class Example(Frame):
    def __init__(self, master):
        print("2")
        Frame.__init__(self, master)
        Frame.configure(self, background="#000")
        b = Canvas(master, width=500, height=500, highlightthickness=0, bd=0, relief='ridge')
        b.pack()
        c = Button(self, text="Click to fade away", command=self.fade_item)
        c.configure(bg='black', fg='white')
        c.pack()
        self.master = master

    def quit(self):
        self.fade_away()
    def fade_item(self):
        color = self.cget("text")
        print(color)

    def fade_away(self):
        alpha = self.master.attributes("-alpha")
        if alpha > 0:
            alpha -= .1
            self.master.attributes("-alpha", alpha)
            self.after(50, self.fade_away)
        else:
            self.master.destroy()

if __name__ == "__main__":
    print("1")
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", root.quit())
    root.title("Coatirane Adventures")
    root.configure(background="#000")
    root.resizable(False, False)
    root.geometry("1000x1000")
    MAIN = Example(root).pack(fill="both", expand=True)
    root.mainloop()
    exit()

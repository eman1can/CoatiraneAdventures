from tkinter import *


class Main(Frame):
    def __init__(self, master):
        self.master = master
        master.title("Coatirane Adventures")
        master.configure(background="#000")
        master.geometry("1000x500+30+30")

        self.label = Label(master, text="Welcome to Coatirane Adventures!")
        self.label.configure(background="#000", foreground="#CFC")
        self.label.place(x=450, y=0)

        self.photo = PhotoImage(file="Hellhounds.png")
        self.photo = self.photo.subsample(1, 1)
        self.label = Label(image=self.photo)
        self.label.image = self.photo  # keep a reference!
        self.label.place(x=50, y=75, height=self.photo.height(), width=self.photo.width())

        self.defend_button = Button(master, text="Attack", command=self.attack("Enemy"))
        self.defend_button.configure(background="#000", foreground="#CFC", activebackground="#000",
                                     activeforeground="#CFC", height=2, width=10)
        self.defend_button.place(x=75 - self.defend_button.winfo_width() / 2, y=350, width=150, height=50)

        self.photo = PhotoImage(file="Battle_Princess_Ais_Wallenstein.png")
        self.photo = self.photo.subsample(4, 4)
        self.label = Label(image=self.photo)
        self.label.image = self.photo  # keep a reference!
        self.label.place(x=725, y=50,height=self.photo.height(), width=self.photo.width())

        self.attack_button = Button(master, text="Attack", command=self.attack("Friend"))
        self.attack_button.configure(background="#000", foreground="#CFC", activebackground="#000",
                                     activeforeground="#CFC", height=2, width=10)
        self.attack_button.place(x=750-self.attack_button.winfo_width()/2, y=350, width=150, height=50)

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.configure(background="#000", foreground="#CFC", activebackground="#000",
                                    activeforeground="#CFC", height=2, width=10)
        self.close_button.place(x=500-self.close_button.winfo_width()/2, y=450)

    def attack(self, target):
        print("Attack!" + " " + target)


root = Tk()
my_gui = Main(root)
root.mainloop()

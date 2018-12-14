from tkinter import *
from tkinter.ttk import Progressbar
import tkinter.ttk as ttk
import csv
import time
from PIL import Image, ImageTk

class Main():
    def __init__(self):
        master = Tk()
        master.title("Coatirane Adventures")
        master.configure(background="#000")
        master.resizable(False, False)
        master.geometry("1000x500+250+150")
        master.update()

        try:
            with open('save_file.txt') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        print(f'Column names are {", ".join(row)}')
                        line_count += 1
                    else:
                        print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                        line_count += 1
                print(f'Processed {line_count} lines.')
        except FileNotFoundError:
            print("Starting new game!")
            #self.label = Label(master, text="Welcome to Coatirane Adventures!")
            #self.label.configure(background="#000", foreground="#CFC", font='helvetica 20')
            #self.label.place(x=500-425/2, y=100, width=425)

            #self.label = Label(master, text="Select a Character!")
            #self.label.configure(background="#000", foreground="#CFC", font='helvetica 20')
            #self.label.place(x=500 - 350 / 2, y=150, width=350)
            canvas = Canvas(master, width=1000, height=500, highlightthickness=0, bd=0, relief='ridge')
            canvas.configure(background="#000")
            canvas.pack(fill=BOTH)
            self.draw("Adventurer_Bell_Cranel.png", 20, 20, master, canvas)
            self.draw("Battle_Princess_Ais_WallenStein.png", 100, 150, master, canvas)
            #img = PhotoImage(file="resized.jpg")
            #canvas.create_image(20, 20, anchor=NW, image=img)
            #img = Image.open("Adventurer_Bell_Cranel.png")
            #new = img.resize((200, 200), Image.ANTIALIAS)
            #self.label = Label(image=new)
            #self.label.image = self.new  # keep a reference!
            #self.label.place(x=275, y=250)

            #self.photo = PhotoImage(file="Battle_Princess_Ais_Wallenstein.png")
            #self.photo = self.photo.subsample(4, 4)
            #self.label = Label(image=self.photo)
            #self.label.image = self.photo  # keep a reference!
            #self.label.place(x=525, y=250, height=self.photo.height(), width=self.photo.width())

    def init(self):
        master = self.master
        #Hellhound pic
        self.photo = PhotoImage(file="Hellhounds.png")
        self.photo = self.photo.subsample(1, 1)
        self.label = Label(image=self.photo)
        self.label.image = self.photo  # keep a reference!
        self.label.place(x=50, y=75, height=self.photo.height(), width=self.photo.width())

        #Hellhound attack button and progress bar
        self.defend_button = Button(master, text="Attack", command=lambda: self.attack("Enemy"))
        self.defend_button.configure(background="#000", foreground="#CFC", activebackground="#000",
                                     activeforeground="#CFC", height=2, width=10)
        self.defend_button.place(x=75 - self.defend_button.winfo_width() / 2, y=350, width=150, height=50)
        self.Ehealth = Progressbar(master, style="red.Horizontal.TProgressbar", orient="horizontal", length=150,
                                  mode="determinate", maximum=100)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        self.Ehealth.place(x=75, y=300)
        self.Ehealth['value'] = 100

        #Wallenwhatsit photo
        self.photo = PhotoImage(file="Battle_Princess_Ais_Wallenstein.png")
        self.photo = self.photo.subsample(4, 4)
        self.label = Label(image=self.photo)
        self.label.image = self.photo  # keep a reference!
        self.label.place(x=725, y=50,height=self.photo.height(), width=self.photo.width())

        #Wallenwhatsit attack button
        self.attack_button = Button(master, text="Attack", command=lambda: self.attack("Friend"))
        self.attack_button.configure(background="#000", foreground="#CFC", activebackground="#000",
                                     activeforeground="#CFC", height=2, width=10)
        self.attack_button.place(x=750-self.attack_button.winfo_width()/2, y=350, width=150, height=50)
        self.health = Progressbar(master, style="green.Horizontal.TProgressbar", orient="horizontal", length=150, mode="determinate", maximum=100)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
        self.health.place(x=750, y=300)
        self.health['value']=100

        #Quit button
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.configure(background="#000", foreground="#CFC", activebackground="#000",
                                    activeforeground="#CFC", height=2, width=10)
        self.close_button.place(x=500-self.close_button.winfo_width()/2, y=450)

    def attack(self, target):
        if (target.__eq__("Enemy")):
            self.health['value'] -= 10
        else:
            self.Ehealth['value'] -= 10

    def draw(self, image, x, y, master, canvas):
        image1 = Image.open(image)
        image1 = image1.resize((image1.width // 5, image1.height // 5))
        gif1 = ImageTk.PhotoImage(image1)
        master.gif1 = gif1
        canvas.create_image(x, y, image=gif1, anchor=NW)
my_gui = Main()
mainloop()

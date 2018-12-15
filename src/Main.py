from tkinter import *
from tkinter.ttk import Progressbar
import tkinter.ttk as ttk
import csv
from PIL import Image, ImageTk
import threading
from pygame import mixer


class Main(threading.Thread):
    def __init__(self, tk_root):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        try:
            # mixer.init()
            # mixer.music.load('background.mp3')
            # mixer.music.play()
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

            self.canvas = Canvas(master, width=1000, height=500, highlightthickness=0, bd=0, relief='ridge')
            self.canvas.configure(background="#000")
            self.canvas.pack(fill=BOTH,expand=YES)

            # These lines create a grid on the screen to help with GUI placement.
            # for x in range(1, 5):
            #     self.canvas.create_line(0,100*x,1000,100*x, fill='white')
            # for x in range(1, 25):
            #     self.canvas.create_line(100*x, 0, 100*x, 500, fill='white')

            image1 = Image.open("Battle_Princess_Ais_WallenStein.png")
            image2 = Image.open("Adventurer_Bell_Cranel.png")
            image3 = Image.open("Battle_Princess_Ais_WallenSteinS.png")
            image4 = Image.open("Adventurer_Bell_CranelS.png")
            self.gif1 = ImageTk.PhotoImage(image1.resize((200, 200)))
            self.gif2 = ImageTk.PhotoImage(image2.resize((200, 200)))
            self.gif3 = ImageTk.PhotoImage(image3.resize((200, 200)))
            self.gif4 = ImageTk.PhotoImage(image4.resize((200, 200)))

            self.beast = Canvas(width=200, height=200, bg='black', bd=0,  highlightthickness=0)
            self.beast.bind("<Enter>", self.on_enter)
            self.beast.bind("<Leave>", self.on_leave)
            self.beast.bind("<Button-1>", self.choosen)
            self.canvas.create_window(225,250, window=self.beast)
            self.beast.create_rectangle(0, 0, 325, 350, fill='black')
            self.beast.create_image(100, 100, image=self.gif2)

            self.princess = Canvas(width=200, height=200, bg='black', bd=0,  highlightthickness=0)
            self.princess.bind("<Enter>", self.on_enter2)
            self.princess.bind("<Leave>", self.on_leave2)
            self.princess.bind("<Button-1>", self.choosen)
            self.canvas.create_window(775, 250, window=self.princess)
            self.princess.create_rectangle(0, 0, 325, 350, fill='black')
            self.princess.create_image(100, 100, image=self.gif1)

            # self.widget = Label(self.canvas, image=self.gif1, fg='white', bg='black', width=200, height=200)
            # self.widget.pack()
            # self.widget.bind("<Enter>", self.on_enter2)
            # self.widget.bind("<Leave>", self.on_leave2)
            # self.canvas.create_window(775, 250, window=self.widget)



            self.canvas.create_text(500, 75, fill="darkred", font="Times 30 italic bold",
                                    text="Welcome to Coatirane Adventures!")
            self.canvas.create_text(500, 150, fill="darkred", font="Times 30 italic bold", text="Select a Character!")
            self.canvas.create_text(775, 375, fill="lightblue", font="Times 30 italic bold", text="Battle Princess")
            self.canvas.create_text(225, 375, fill="lightblue", font="Times 30 italic bold", text="Beast Slayer")

    def on_enter(self, event):
        print("in1")
        self.beast.create_image(100, 100, image=self.gif4)

    def on_leave(self, enter):
        print("out1")
        self.beast.create_rectangle(0, 0, 200, 200, fill='black')
        self.beast.create_image(100, 100, image=self.gif2)

    def on_enter2(self, event):
        print("in2")
        self.princess.create_image(100, 100, image=self.gif3)

    def on_leave2(self, enter):
        print("out2")
        self.princess.create_rectangle(0, 0, 200, 200, fill='black')
        self.princess.create_image(100, 100, image=self.gif1)

    def choosen(self, event):
        if ("" + repr(event.widget)) == ("<tkinter.Canvas object .!canvas3>"):
            print("Princess")
        else:
            print("Slayer")


    def init(self):
        # Hellhound pic
        self.photo = PhotoImage(file="Hellhounds.png")
        self.photo = self.photo.subsample(1, 1)
        self.label = Label(image=self.photo)
        self.label.image = self.photo  # keep a reference!
        self.label.place(x=50, y=75, height=self.photo.height(), width=self.photo.width())

        # Hellhound attack button and progress bar
        self.defend_button = Button(self.master, text="Attack", command=lambda: self.attack("Enemy"))
        self.defend_button.configure(background="#000", foreground="#CFC", activebackground="#000",
                                 activeforeground="#CFC", height=2, width=10)
        self.defend_button.place(x=75 - self.defend_button.winfo_width() / 2, y=350, width=150, height=50)
        self.Ehealth = Progressbar(self.master, style="red.Horizontal.TProgressbar", orient="horizontal", length=150,
                               mode="determinate", maximum=100)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        self.Ehealth.place(x=75, y=300)
        self.Ehealth['value'] = 100

        # Wallenwhatsit photo
        self.photo = PhotoImage(file="Battle_Princess_Ais_Wallenstein.png")
        self.photo = self.photo.subsample(4, 4)
        self.label = Label(image=self.photo)
        self.label.image = self.photo  # keep a reference!
        self.label.place(x=725, y=50, height=self.photo.height(), width=self.photo.width())

        # Wallenwhatsit attack button
        self.attack_button = Button(self.master, text="Attack", command=lambda: self.attack("Friend"))
        self.attack_button.configure(background="#000", foreground="#CFC", activebackground="#000",
                                 activeforeground="#CFC", height=2, width=10)
        self.attack_button.place(x=750 - self.attack_button.winfo_width() / 2, y=350, width=150, height=50)
        self.health = Progressbar(self.master, style="green.Horizontal.TProgressbar", orient="horizontal", length=150,
                              mode="determinate", maximum=100)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
        self.health.place(x=750, y=300)
        self.health['value'] = 100

        # Quit button
        self.close_button = Button(self.master, text="Close", command=self.master.quit)
        self.close_button.configure(background="#000", foreground="#CFC", activebackground="#000",
                                activeforeground="#CFC", height=2, width=10)
        self.close_button.place(x=500 - self.close_button.winfo_width() / 2, y=450)


    def attack(self, target):
        if (target.__eq__("Enemy")):
            self.health['value'] -= 10
        else:
            self.Ehealth['value'] -= 10

master = Tk()
master.title("Coatirane Adventures")
master.configure(background="#000")
master.resizable(False, False)
master.geometry("1000x500+250+150")

MAIN = Main(master)
master.mainloop()

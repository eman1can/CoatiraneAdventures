from tkinter import *
from tkinter.ttk import Progressbar
import tkinter.ttk as ttk
import csv
import threading
import Init
import time
from PIL import Image, ImageTk
from pygame import mixer


class Main(threading.Thread):
    def __init__(self, tk_root):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        townImage = Image.open("res/town.jpg")
        self.townImage = ImageTk.PhotoImage(townImage.resize((1000, 500)))
        self.canvas = Canvas(master, width=1000, height=500, highlightthickness=0, bd=0, relief='ridge')
        self.canvas.configure(background="#000")
        self.canvas.pack(fill=BOTH, expand=YES)
        try:
            mixer.init()
            mixer.music.load('res/town.mp3')
            mixer.music.play()
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
            start = Init.Init(self.canvas)
            while not start.choosenB:
                time.sleep(.2)
            self.town(start.getchar())
            start = "hi!"

    def wait_until(somepredicate, timeout, period=1, *args, **kwargs):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if somepredicate: return True
            time.sleep(period)
        return False

    def town(self, character):
        print ()

    def startGame(self, character):
        print ("Starting Game!")
        print (character.getname())
        self.canvas.delete("init")
        self.canvas.create_image(500, 250, image=self.townImage, tags="background")

        # Hellhound pic
        photo = PhotoImage(file="res/Hellhounds.png")
        photo = photo.subsample(1, 1)
        label = Label(image=photo)
        label.image = photo  # keep a reference!
        label.place(x=50, y=75, height=photo.height(), width=photo.width())

        # Hellhound attack button and progress bar
        defend_button = Button(master, text="Attack", command=lambda: self.attack("Enemy"))
        defend_button.configure(background="#000", foreground="#CFC", activebackground="#000",
                                activeforeground="#CFC", height=2, width=10)
        defend_button.place(x=75 - defend_button.winfo_width() / 2, y=350, width=150, height=50)
        self.Ehealth = Progressbar(master, style="red.Horizontal.TProgressbar", orient="horizontal", length=150,
                                   mode="determinate", maximum=100)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        self.Ehealth.place(x=75, y=300)
        self.Ehealth['value'] = 100

        # Character photo
        label = Label(image=character.getimage())
        label.place(x=725, y=50, height=200, width=200)

        # Character attack button
        attack_button = Button(master, text="Attack", command=lambda: self.attack("Friend"))
        attack_button.configure(background="#000", foreground="#CFC", activebackground="#000",
                                activeforeground="#CFC", height=2, width=10)
        attack_button.place(x=750 - attack_button.winfo_width() / 2, y=350, width=150, height=50)
        self.health = Progressbar(master, style="green.Horizontal.TProgressbar", orient="horizontal", length=150,
                                  mode="determinate", maximum=100)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
        self.health.place(x=750, y=300)
        self.health['value'] = 100

        # Quit button
        close_button = Button(master, text="Close", command=master.quit)
        close_button.configure(background="#000", foreground="#CFC", activebackground="#000",
                               activeforeground="#CFC", height=2, width=10)
        close_button.place(x=500 - close_button.winfo_width() / 2, y=450)




    # def test(self):

    #
    #
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

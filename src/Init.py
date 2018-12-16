from tkinter import *
import Entities.Character as character
from PIL import Image, ImageTk

class Init:

    def __init__(self, canvas):
        self.canvas = canvas
        self.choosenB = False
        print("Starting new game!")
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

        # Beast slayer object creation
        self.beast = Canvas(width=200, height=200, bg='black', bd=0, highlightthickness=0)
        self.beast.bind("<Enter>", self.on_enter)
        self.beast.bind("<Leave>", self.on_leave)
        self.beast.bind("<Button-1>", self.choosen)
        self.canvas.create_window(225, 250, window=self.beast, tags="init")
        self.beast.create_rectangle(0, 0, 325, 350, fill='black', tags="init")
        self.beast.create_image(100, 100, image=self.gif2, tags="init")

        # sword Princess object creation
        self.princess = Canvas(width=200, height=200, bg='black', bd=0, highlightthickness=0)
        self.princess.bind("<Enter>", self.on_enter2)
        self.princess.bind("<Leave>", self.on_leave2)
        self.princess.bind("<Button-1>", self.choosen)
        self.canvas.create_window(775, 250, window=self.princess, tags="init")
        self.princess.create_rectangle(0, 0, 325, 350, fill='black', tags="init")
        self.princess.create_image(100, 100, image=self.gif1, tags="init")

        #Create text objects
        self.canvas.create_text(500, 75, fill="darkred", font="Times 30 italic bold",
                                text="Welcome to Coatirane Adventures!", tags="init")
        self.canvas.create_text(500, 150, fill="darkred", font="Times 30 italic bold", text="Select a Character!", tags="init")
        self.canvas.create_text(775, 375, fill="lightblue", font="Times 30 italic bold", text="Battle Princess", tags="init")
        self.canvas.create_text(225, 375, fill="lightblue", font="Times 30 italic bold", text="Beast Slayer", tags="init")


    def on_enter(self, event):
        self.beast.create_image(100, 100, image=self.gif4, tags="init")

    def on_leave(self, enter):
        self.beast.create_rectangle(0, 0, 200, 200, fill='black', tags="init")
        self.beast.create_image(100, 100, image=self.gif2, tags="init")

    def on_enter2(self, event):
        self.princess.create_image(100, 100, image=self.gif3, tags="init")

    def on_leave2(self, enter):
        self.princess.create_rectangle(0, 0, 200, 200, fill='black', tags="init")
        self.princess.create_image(100, 100, image=self.gif1, tags="init")

    def choosen(self, event):
        if ("" + repr(event.widget)) == ("<tkinter.Canvas object .!canvas3>"):
            self.char = character.Character("Princess", 200, 25, 20, self.gif1)
            self.choosenB = True
        else:
            self.char = character.Character("Slayer", 200, 25, 20, self.gif2)
            self.choosenB = True

    def getchar(self):
        return self.char
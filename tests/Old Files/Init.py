from tkinter import *
import Entities.Character as character
from PIL import Image, ImageTk
from colormap import rgb2hex
import math
class Init:

    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.choosenB = False
        print("Starting new game!")
        # These lines create a grid on the screen to help with GUI placement.
        # amount = 50
        # thick = 5
        # for x in range(1, amount):
        #     if x % thick == 0:
        #         self.canvas.create_line(0,(height/amount)*x,width,(height/amount)*x, fill='red')
        #     else:
        #         self.canvas.create_line(0, (height / amount) * x, width, (height / amount) * x, fill='white')
        # for x in range(1, amount):
        #     if x % thick == 0:
        #         self.canvas.create_line((width / amount) * x, 0, (width / amount) * x, height, fill='red')
        #     else:
        #         self.canvas.create_line((width/amount)*x, 0, (width/amount)*x, height, fill='white')

        for x in range(0, 10, 2):
            if x == 0:
                continue
            canvas.create_rectangle(0, 0, width, height, fill=rgb2hex(0, x, 0, normalised=False))

        canvas.create_rectangle(0, 0, width, height, fill='black')
        image1 = Image.open("res/Prev/badass_ais_full.png")
        image2 = Image.open("res/Prev/hero_bell_full.png")
        # image3 = Image.open("res/Battle_Princess_Ais_WallenSteinS.png")
        # image4 = Image.open("res/Adventurer_Bell_CranelS.png")
        self.size = math.floor(width/4)
        inc = math.ceil(math.ceil(width/1000*25)) # 1000 - 25 - 2560 - 64
        print(str(width))
        print(str(self.size))
        print(str(inc))
        self.gif1 = ImageTk.PhotoImage(image1.resize((self.size, self.size)))
        self.gif2 = ImageTk.PhotoImage(image2.resize((self.size, self.size)))
        # self.gif3 = ImageTk.PhotoImage(image3.resize((self.size, self.size)))
        # self.gif4 = ImageTk.PhotoImage(image4.resize((self.size, self.size)))

        # Beast slayer object creation
        self.beast = Canvas(width=self.size, height=self.size, bg='black', bd=0, highlightthickness=0)
        self.beast.bind("<Enter>", self.on_enter)
        self.beast.bind("<Leave>", self.on_leave)
        self.beast.bind("<Button-1>", self.choosen)
        print(str(math.floor((width-(self.size*2))/3)))
        gap = math.floor((width-(self.size*2))/3)
        self.canvas.create_window(inc*9, inc*10, window=self.beast, tags="init")
        self.beast.create_rectangle(0, 0, self.size, self.size, fill='black', tags="init")
        self.beast.create_image(self.size/2, self.size/2, image=self.gif2, tags="init")

        # sword Princess object creation
        self.princess = Canvas(width=self.size, height=self.size, bg='black', bd=0, highlightthickness=0)
        self.princess.bind("<Enter>", self.on_enter2)
        self.princess.bind("<Leave>", self.on_leave2)
        self.princess.bind("<Button-1>", self.choosen)
        self.canvas.create_window(inc*31, 10*inc, window=self.princess, tags="init")
        self.princess.create_rectangle(0, 0, self.size, self.size, fill='black', tags="init")
        self.princess.create_image(self.size/2, self.size/2, image=self.gif1, tags="init")

        #Create text objects
        fontSize = math.floor(height/500)*33 # 30 - 500 - 2160 - 60
        print(str(height))
        self.canvas.create_text(20*inc, 3*inc, fill="darkred", font=f"Times {fontSize} italic bold",
                                text="Welcome to Coatirane Adventures!", tags="init")
        self.canvas.create_text(20*inc, 6*inc, fill="darkred", font=f"Times {fontSize} italic bold", text="Select a Character!", tags="init")
        self.canvas.create_text(31*inc, 16*inc, fill="lightblue", font=f"Times {fontSize} italic bold", text="Battle Princess", tags="init")
        self.canvas.create_text(9*inc, 16*inc, fill="lightblue", font=f"Times {fontSize} italic bold", text="Beast Slayer", tags="init")


    def on_enter(self, event):
        pass
        # self.beast.create_image(self.size/2, self.size/2, image=self.gif4, tags="init")

    def on_leave(self, enter):
        pass
        # self.beast.create_rectangle(0, 0, self.size, self.size, fill='black', tags="init")
        # self.beast.create_image(self.size/2, self.size/2, image=self.gif2, tags="init")

    def on_enter2(self, event):
        pass
        # self.princess.create_image(self.size/2, self.size/2, image=self.gif3, tags="init")

    def on_leave2(self, enter):
        self.princess.create_rectangle(0, 0, self.size, self.size, fill='black', tags="init")
        self.princess.create_image(self.size/2, self.size/2, image=self.gif1, tags="init")

    def choosen(self, event):
        if ("" + repr(event.widget)) == ("<tkinter.Canvas object .!canvas3>"):
            # self.char = character.Character("Princess", 200, 25, 20, self.gif1)
            self.choosenB = True
        else:
            # self.char = character.Character("Slayer", 200, 25, 20, self.gif2)
            self.choosenB = True

    def getchar(self):
        return None
    #     return self.char

    def clamp(x):
        return max(0, min(x, 255))
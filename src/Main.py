from tkinter import *
from tkinter.ttk import Progressbar
import tkinter.ttk as ttk
import csv
import threading
import Init
import time
from PIL import Image, ImageTk, ImageDraw
from pygame import mixer
import ctypes
import math
import spritesheets

has_prev_key_release = None

class Main(threading.Thread):
    def __init__(self, tk_root):
        self.root = tk_root
        user32 = ctypes.windll.user32
        self.width = math.floor(user32.GetSystemMetrics(0) * 2 / 3)
        self.height = math.floor(user32.GetSystemMetrics(1) * 2 / 3)
        master.geometry(f"{self.width}x{self.height}+{math.floor(self.width/4)}+{math.floor(self.height/4)}")
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        townImage = Image.open("res/town.jpg")
        self.townImage = ImageTk.PhotoImage(townImage.resize((self.width, self.height)))
        self.canvas = Canvas(master, width=self.width, height=self.height, highlightthickness=0, bd=0, relief='ridge')
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
            start = Init.Init(self.canvas, self.width, self.height)
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
        print("Starting Game!")
        print(character.getname())
        self.canvas.delete("init")
        self.canvas.create_image(self.width/2, self.height/2, image=self.townImage, tags="background")
        #
        # # Walk left 118-126
        # # Walk forwards 132-139
        # # Walk right 152-144
        # # Walk back 104-113
        # self.index = 0
        # self.walk_forward = []
        # self.walk_right = []
        # self.walk_left = []
        # self.walk_back = []
        # self.create_sprite("res/Martha.png", 3, 3, 0, 256, 256, 50, 50, self.walk_forward)
        # self.create_sprite("res/Martha.png", 1, 3, 0, 256, 256, 50, 50, self.walk_left)
        # self.create_sprite("res/Martha.png", 2, 3, 0, 256, 256, 50, 50, self.walk_right)
        # self.create_sprite("res/Martha.png", 0, 3, 0, 256, 256, 50, 50, self.walk_back)
        # master.bind("<KeyPress>", self.on_key_press)
        # self.x = 500
        # self.y = 250
        # self.lastPressed = ''
        # self.draw_sprite(self.index, self.walk_back, self.x, self.y, 256, 256)

        # FPS = 8
        # index = 0
        # timeStart = time.time()
        # while True:
        #     if (time.time() - timeStart) > (1 / FPS):
        #         print(index)
        #         if index > len(self.cells)-1:
        #             index = 0
        #         self.draw_sprite(index, self.cells, 250, 250, 64, 64)
        #         index+=1
        #         timeStart = time.time()
        inc = math.ceil(math.ceil(self.width / 1000 * 25))  # 1000 - 25 - 2560 - 64

        self.name = "Marissa"
        self.rankLvl = 32
        self.rank = 245123
        self.rankMax = 270000
        self.ametrine = 2312
        self.toals = 231263
        self.max=500
        self.progress=math.floor(500 * (self.rank/self.rankMax))
        #top of GUI
        self.canvas.create_rectangle(inc, inc, inc*6, inc*2, fill='#555555')
        self.canvas.create_rectangle(inc*7, inc, inc * 15, inc * 2, fill='#555555')
        self.canvas.create_rectangle(inc*16, inc, inc * 20, inc * 2, fill='#555555')
        self.canvas.create_rectangle(inc*21, inc, inc * 26, inc * 2, fill='#555555')

        self.canvas.create_text(inc +inc/4, inc / 2, font="Times 32 bold", text="Player Name", fill='Gray', anchor=W)
        self.canvas.create_text(inc +inc/4, inc/2-2, font = "Times 32 bold", text="Player Name", fill='white', anchor=W)
        self.canvas.create_text(inc +inc/4, inc + inc/2, font = "Times 34 italic bold", text=self.name, fill='white', anchor=W)

        self.canvas.create_text(inc * 7 + inc/4, inc / 2, font="Times 32 italic bold", text="Rank", fill='Gray', anchor=W)
        self.canvas.create_text(inc * 7 + inc/4, inc / 2 - 2, font="Times 32 bold", text="Rank", fill='white', anchor=W)
        self.canvas.create_text(inc * 7 + inc/4, inc + inc/2, font = "Times 32 italic", text=str(self.rankLvl), fill='white', anchor=W)
        self.canvas.create_rectangle(inc * 8 + inc/2, inc + inc/3, inc * 14 + inc/2, inc*2 - inc/3, fill="#777777")
        progressImage = Image.open("res/rank.png")
        self.progressImage = progressImage.crop((0, 0, self.progress, 50))
        self.progressImage = ImageTk.PhotoImage(progressImage.resize((math.floor(inc*6 * (self.rank/self.rankMax)), math.floor(inc*2/6))))
        self.canvas.create_image(inc * 8 + inc / 2, inc + inc / 2, image=self.progressImage, tags="GUI", anchor=W)


        self.canvas.create_text(inc * 16 + inc/4, inc / 2, font="Times 32 bold", text="Ametrine", fill='Gray', anchor=W)
        self.canvas.create_text(inc * 16 + inc/4, inc / 2 - 2, font="Times 32 bold", text="Ametrine", fill='white', anchor=W)
        ametrineImage = Image.open("res/ametrine.png")
        self.ametrineImage = ImageTk.PhotoImage(ametrineImage.resize((math.floor(inc*2/3), math.floor(inc*2/3))))
        self.canvas.create_image(inc*16 + inc/2, inc+inc/2, image=self.ametrineImage, tags="GUI")
        self.canvas.create_text(inc*17, inc + inc/2, font="Times 32 italic", text=str(self.ametrine), fill='white', anchor=W)

        self.canvas.create_text(inc * 21 + inc/4, inc / 2, font="Times 32 bold", text="Emus", fill='Gray', anchor=W)
        self.canvas.create_text(inc * 21 + inc/4, inc / 2 - 2, font="Times 32 bold", text="Emus", fill='white', anchor=W)
        toalsImage = Image.open("res/toals.png")
        self.toalsImage = ImageTk.PhotoImage(toalsImage.resize((math.floor(inc * 2 / 3), math.floor(inc * 2 / 3))))
        self.canvas.create_image(inc * 21 + inc / 2, inc + inc / 2, image=self.toalsImage, tags="GUI")
        self.canvas.create_text(inc * 22, inc + inc/2, font="Times 32 italic", text=str(self.toals), fill='white', anchor=W)


        #Bottom of GUI
        inc = math.ceil(inc*9/12) # - 48
        #tavern
        self.canvas.create_polygon((3 * inc, self.height - (inc)),
                                   (5*inc,  self.height - (inc)),
                                   (5 * inc, self.height - (4 * inc)),
                                   (3 * inc, self.height - (6 * inc)),
                                   (inc, self.height - (4 * inc)),
                                   (inc, self.height - inc), fill="#000000")
        pubImage = Image.open("res/mug.png")
        self.pubImage = ImageTk.PhotoImage(pubImage.resize((inc * 2, inc * 2)))
        self.canvas.create_image(3 * inc + inc / 6, self.height - inc * 4, image=self.pubImage)
        self.canvas.create_text(inc * 3, self.height - inc * 2, font="Times 32 bold", text="Tavern", fill='white')

        #shop
        self.canvas.create_polygon((8 * inc, self.height - (inc)), (10*inc, self.height - inc), (10 * inc, self.height - (4 * inc)), (8 * inc, self.height - (6 * inc)), (6 * inc, self.height - (4 * inc)),(6*inc, self.height - inc),  fill="#000000")
        sackImage = Image.open("res/sack.png")
        self.sackImage = ImageTk.PhotoImage(sackImage.resize((inc * 2, inc * 2)))
        self.canvas.create_image(8 * inc, self.height - inc * 4, image=self.sackImage)
        self.canvas.create_text(inc * 8, self.height - inc * 2, font="Times 32 bold", text="Shop", fill='white')

        # character drawing
        self.canvas.create_polygon((13 * inc, self.height - (inc)), (15*inc, self.height - (inc)), (15 * inc, self.height - (4 * inc)), (13 * inc, self.height - (6 * inc)), (11*inc, self.height - (4 * inc)), (11*inc, self.height - (inc)), fill="#000000")
        characterImage = Image.open("res/character.png")
        self.characterImage = ImageTk.PhotoImage(characterImage.resize((inc*2,inc*2)))
        self.canvas.create_image(13*inc, self.height-inc*4, image=self.characterImage)
        self.canvas.create_text(inc*13, self.height-inc*2, font="Times 32 bold", text="Raffle", fill='white')

        # blacksmith
        self.canvas.create_polygon((18 * inc, self.height - (inc)), (20*inc, self.height-(inc)), (20 * inc, self.height - (4 * inc)), (18 * inc, self.height - (6 * inc)), (16 * inc, self.height - (4 * inc)), (16*inc, self.height-inc), fill="#000000")
        craftImage = Image.open("res/craft.png")
        self.craftImage = ImageTk.PhotoImage(craftImage.resize((inc*2, inc*2)))
        self.canvas.create_image(18*inc, self.height-inc*4, image=self.craftImage)
        self.canvas.create_text(inc * 18, self.height - inc * 2, font="Times 32 bold", text="Crafting", fill='White')

        # party screen
        self.canvas.create_polygon((23 * inc, self.height - (inc)), (25*inc, self.height-(inc)), (25 * inc, self.height - (4 * inc)), (23 * inc, self.height - (6 * inc)), (21 * inc, self.height - (4 * inc)), (21*inc, self.height-inc), fill="#000000")
        partyImage = Image.open("res/Adventurer_Bell_Cranel.png")
        self.partyImage = ImageTk.PhotoImage(partyImage.resize((inc*3, inc*3)))
        self.canvas.create_image(23*inc, self.height - inc*4, image=self.partyImage)
        self.canvas.create_text(inc * 23, self.height - inc * 2, font="Times 32 bold", text="Party", fill='white')

        #inventory
        self.canvas.create_polygon((28 * inc, self.height - (inc)), (30*inc, self.height-(inc)), (30 * inc, self.height - (4 * inc)), (28 * inc, self.height - (6 * inc)), (26 * inc, self.height - (4 * inc)), (26*inc, self.height-inc), fill="#000000")
        inventoryImage = Image.open("res/inventory.png")
        self.inventoryImage = ImageTk.PhotoImage(inventoryImage.resize((inc*2, inc*2)))
        self.canvas.create_image(28*inc, self.height - inc*4, image=self.inventoryImage)
        self.canvas.create_text(inc * 28, self.height - inc * 2, font="Times 32 bold", text="Inventory", fill='white')

        # quests
        self.canvas.create_polygon((33 * inc, self.height - (inc)), (35*inc, self.height-(inc)), (35 * inc, self.height - (4 * inc)), (33 * inc, self.height - (6 * inc)), (31 * inc, self.height - (4 * inc)), (31*inc, self.height-inc), fill="#000000")
        questsImage = Image.open("res/quests.png")
        self.questsImage = ImageTk.PhotoImage(questsImage.resize((inc*2, inc*2)))
        self.canvas.create_image(33*inc, self.height - inc*4, image=self.questsImage)
        self.canvas.create_text(inc * 33, self.height - inc * 2, font="Times 32 bold", text="Quests", fill='white')

        #dungeon
        inc *=2
        self.canvas.create_polygon((self.width - (inc*3 + inc/2), self.height - (inc)),
                                   (self.width - (inc*3)        , self.height - (inc*2+inc/2)),
                                   (self.width - (inc*3 + inc/2), self.height - (inc*4)),
                                   (self.width - (inc*5 - inc/2), self.height - (inc*4)),
                                   (self.width - (inc*5)        , self.height - (inc*4 + inc/2)),
                                   (self.width - (inc*5 + inc/2), self.height - (inc*4)),
                                   (self.width - (inc*7 - inc/2), self.height - (inc*4)),
                                   (self.width - (inc*7)        , self.height - (inc*2+inc/2)),
                                   (self.width - (inc*7 - inc/2), self.height - (inc)),
                                   (self.width - (inc*5 + inc/2), self.height - (inc)),
                                   (self.width - (inc*5)        , self.height - (inc/2)),
                                   (self.width - (inc*5 - inc/2), self.height - (inc)), fill="#010010")
        dungeonImage = Image.open("res/dungeon.png")
        self.dungeonImage = ImageTk.PhotoImage(dungeonImage.resize((math.floor(inc + inc/2), math.floor(inc + inc/2))))
        self.canvas.create_image(self.width - inc*5, self.height - inc*3, image=self.dungeonImage)
        self.canvas.create_text(self.width - inc*5, self.height - inc-inc/2, font ="Times 48 bold", text="Dungeon", fill='white')

    def on_key_press_repeat(self, event):
        global has_prev_key_release
        self.on_key_press(event)

    def on_key_press(self, event):
        self.moveInc = 8
        if (event.char == 'w'):
            if self.lastPressed != 'w':
                self.canvas.delete("sprite")
                self.draw_sprite(self.index, self.walk_forward, self.x, self.y, 256, 256)
            else:
                self.canvas.move("sprite", 0, -self.moveInc)
                self.y-=self.moveInc
        if (event.char == 'a'):
            if self.lastPressed != 'a':
                self.canvas.delete("sprite")
                self.draw_sprite(self.index, self.walk_left, self.x, self.y, 256, 256)
            else:
                self.canvas.move("sprite", -self.moveInc, 0)
                self.x-=self.moveInc
        if (event.char == 's'):
            if self.lastPressed != 's':
                self.canvas.delete("sprite")
                self.draw_sprite(self.index, self.walk_back, self.x, self.y, 256, 256)
            else:
                self.canvas.move("sprite", 0, self.moveInc)
                self.y+=self.moveInc
        if (event.char == 'd'):
            if self.lastPressed != 'd':
                self.canvas.delete("sprite")
                self.draw_sprite(self.index, self.walk_right, self.x, self.y, 256, 256)
            else:
                self.canvas.move("sprite", self.moveInc, 0)
                self.x+=self.moveInc
        self.lastPressed = event.char
    def create_sprite(self, image, row, cols, Sindex, w, h, x, y, output):
        self.sheet = Image.open(image)
        #start = self.sheet.crop(((w * math.floor(Sindex % cols)), row * h, (w * math.floor(Sindex % cols)) + w, (row * h) + h))
        start = row*cols
        for xI in range(cols):
            # get x ((math.floor(x % cols) * w)
            # get y (math.floor(x / cols) * h)
            print(w)
            print(h)
            output.append(ImageTk.PhotoImage(self.sheet.crop( ( (math.floor((xI+start) % cols) * w), (math.floor((xI+start) / cols) * h), (math.floor((xI+start) % cols) * w) + w, (math.floor((xI+start) / cols) * h) + h ) )))
        # for xI in range(len(self.cells)):
        #     self.canvas.create_image(x + (w/2) * xI, y + (h/2), image=self.cells[xI], tags="sprite")
        #     self.canvas.tag_raise("sprite")

    def draw_sprite(self, index, spritesheet, x, y, w, h):
        self.canvas.create_image(x, y, image=spritesheet[index], tags="sprite")
        self.canvas.tag_raise("sprite")

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
master.protocol("WM_DELETE_WINDOW", master.quit())
master.title("Coatirane Adventures")
master.configure(background="#000")
master.resizable(False, False)



MAIN = Main(master)
master.mainloop()
exit()

import tkinter
import queue
import math
import ctypes


class Flash(tkinter.Toplevel):
    def __init__(self, root, **options):
        tkinter.Toplevel.__init__(self, root, width=width, height=height, **options)

        self.overrideredirect(True) # remove header from toplevel
        self.root = root

        self.attributes("-alpha", 0.0) # set transparency to 100%

        self.queue = queue.Queue()
        self.update_me()

    def write(self, message):
        self.queue.put(message) # insert message into the queue

    def update_me(self):
        #This makes our tkinter widget threadsafe
        # http://effbot.org/zone/tkinter-threads.htm
        try:
            while 1:
                message = self.queue.get_nowait() # get message from the queue
                # if a message is received code will execute from here otherwise exception
                # http://stackoverflow.com/questions/11156766/placing-child-window-relative-to-parent-in-tkinter-pythons
                x = root.winfo_rootx() # set x coordinate of root
                y = root.winfo_rooty() # set y coordinate of root
                width = root.winfo_width() # get the width of root
                self.geometry("+%d+%d" % (x ,y)) # place in the top right cornder of root

                self.fade_in() # fade in when a message is received
                self.label_flash = tkinter.Canvas(self, width = width, height=height, bg='black', highlightthickness=0, bd=0, relief='ridge')
                self.label_flash.create_text(600, 200, fill='#992000', font="Times 140 italic bold", text="Coatirane")
                self.label_flash.create_text(1000, 400, fill='#992000', font="Times 160 italic bold", text="Adventures")

                self.label_flash.create_polygon((1100, 800), (1000, 875), (1100, 950), (1700, 950), (1800, 875), (1700, 800), fill='#222222', tags='start')
                self.label_flash.create_text(1400, 875, fill='#992030', font='Times 100 italic bold', text='Load')
                self.label_flash.create_polygon((1100, 1100), (1000, 1175), (1100, 1250), (1700, 1250), (1800, 1175), (1700, 1100), fill='#222222', tags='new')
                self.label_flash.create_text(1400, 1175, fill='#992030', font='Times 100 italic bold', text='New Game')
                # self.label_flash.create_polygon((1100, 950), (1100, 975), (1700, 975), (1800, 900), (1800, 875),(1700, 950), fill='#111111', tags='shadow')
                self.label_flash.tag_bind('start', "<Enter>", self.on_enterStart)
                self.label_flash.tag_bind('start', "<Leave>", self.on_leaveStart)
                self.label_flash.tag_bind('new', "<Enter>", self.on_enterNew)
                self.label_flash.tag_bind('new', "<Leave>", self.on_leaveNew)
                self.label_flash.pack(anchor='e')
                self.lift(self.root)

                # def callback():
                #     label_flash.after(2000, label_flash.destroy) # destroy the label after 5 seconds
                #     self.fade_away() # fade away after 3 seconds
                # label_flash.after(3000, callback)

        except queue.Empty:
            pass
        self.after(10, self.update_me) # check queue every 100th of a second

    def on_enterStart(self, event):
        self.label_flash.create_polygon((1100, 950), (1100, 975), (1700, 975), (1800, 900), (1800, 875), (1700, 950), fill='#111111', tags='shadow')

    def on_leaveStart(self, event):
        self.label_flash.delete('shadow')

    def on_enterNew(self, event):
        self.label_flash.create_polygon((1100, 1250), (1100, 1275), (1700, 1275), (1800, 1200), (1800, 1100), (1700, 1175),
                                        fill='#111111', tags='shadow')
    def on_leaveNew(self, event):
        self.label_flash.delete('shadow')
    # http://stackoverflow.com/questions/3399882/having-trouble-with-tkinter-transparency
    def fade_in(self):
        alpha = self.attributes("-alpha")
        alpha = min(alpha + .01, 1.0)
        self.attributes("-alpha", alpha)
        if alpha < 1.0:
            self.after(15, self.fade_in)

    # http://stackoverflow.com/questions/22491488/how-to-create-a-fade-out-effect-in-tkinter-my-code-crashes
    def fade_away(self):
        alpha = self.attributes("-alpha")
        if alpha > 0:
            alpha -= .1
            self.attributes("-alpha", alpha)
            self.after(20, self.fade_away)

if __name__ == '__main__':
    user32 = ctypes.windll.user32
    width = math.floor(user32.GetSystemMetrics(0) * 2 / 3)
    height = math.floor(user32.GetSystemMetrics(1) * 2 / 3)

    root = tkinter.Tk()
    root.minsize(width, height)
    root.geometry("1000x500")

    flash = Flash(root) # create toplevel instance

    def callback():
        # put a delay between each message so we can check the behaviour depending on the lenght of the delay between messages
        import time
        flash.write('Coatirane Adventures')
        time.sleep(1)

    # create a thread to prevent the delays from blocking our GUI
    import threading
    t = threading.Thread(target=callback)
    t.daemon = True
    t.start()
    root.mainloop()
    exit()
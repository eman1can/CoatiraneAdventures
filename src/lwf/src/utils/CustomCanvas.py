
class CustomCanvas(Widget):
    #Every Custom Canvas will store every instruction in a InstructionGroup
    #This will allow us to pass a variety of arguments into draw Image
    def __init__(self):
        super().__init__()
        self.hasTransform = False
        self.group = InstructionGroup()
        self._group = InstructionGroup()
        self.globalCompositeOperation = "source-over"
        self.globalAlpha = 1
        self.style = {}
        self.backgroundColor = Color(0, 0, 0, 1)
        self.fillStyle = "#000000" #can be a color #000000 or "gradient" or "pattern"

    def getContext(self):
        return self

    def setTransform(self, scaleX, skew1, skew0, scaleY, translateX, translateY):
        if skew1 != 0 or skew0 != 0:
            raise Exception("Skewing is not implemented!")
        if self.hasTransform:
            self.group.add(PopMatrix())
            self.hasTransform = False
        self.group.add(PushMatrix())
        self.hasTransform = True
        if scaleX != 1 or scaleY != 1:
            self.group.add(Scale(scaleX, scaleY, 0))
        if translateX != 0 or translateY != 0:
            self.group.add(Translate(translateX, translateY))

    def translate(self, x, y):
        if self.hasTransform:
            self.group.add(Translate(x, y))
        else:
            self.group.add(PushMatrix())
            self.hasTransform = True
            self.group.add(Translate(x, y))

    def fillRect(self, x, y, w, h):
        self.rect(x, y, w, h)

    def rect(self, x, y, w, h): #should be the same as a fillRect
        if self.fillStyle == "pattern":
            #is an image pattern
            self.group.add(Rectangle(pos=(x, y), size=(w, h), source=self.pattern, tex_coords=self.tex_coords))
        elif self.fillStyle == "gradient":
            self.group.add(Rectangle(pos=(x, y), size=(w, h), texture=self.gradient, tex_coords=self.tex_coords))
        else:
            #is a color
            self.parseColor(self.fillStyle)
            self.group.add(Rectangle(pox=(x, y), size=(w, h)))
        self.draw()

    def clearRect(self, x, y, w, h):
        # use background color to write over
        print(self.style)

        if x <= 0 and y <= 0 and w >= self.width and h >= self.height:
            #Is a full Screen Clear, clean-up resources
            self.group = InstructionGroup()
            self._group = InstructionGroup()
            self.canvas.clear()
        self.group.add(self.backgroundColor)
        self.group.add(Rectangle(pos=(x, y), size=(w, h)))
        self.draw()

    #Removes the instructions from the buffer and adds them to the canvas
    def draw(self):
        for instruction in self.group.children:
            #We may have an extra bind texture for every InstructionGroup()
            #If it causes problems, then filter them out.
            print("Adding ", instruction, " to the canvas!")
            self.group.remove(instruction)
            self._group.add(instruction)
            self.canvas.add(instruction)

    def drawImage(self, *args):
        # img is either a canvas with instructions or a image
        if len(args) == 3:
            #img, x, y
            img = args[0]
            sx = 0
            sy = 0
            swidth = 1
            sheight = 1
            dx = args[1]
            dy = args[2]
            dwidth = img.width
            dheight = img.height
        elif len(args) == 5:
            #img, x, y, width, height
            img = args[0]
            sx = 0
            sy = 0
            swidth = 0
            sheight = 0
            dx = args[1]
            dy = args[2]
            dwidth = args[3]
            dheight = args[4]
        elif len(args) == 9:
            #img, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight
            img = args[0]
            sx = self.normalize(args[1], img.width)
            sy = self.normalize(args[2], img.height)
            swidth = self.normalize(args[3], img.width)
            sheight = self.normalize(args[4], img.height)
            dx = args[5]
            dy = args[6]
            dwidth = args[7]
            dheight = args[8]
        else:
            raise Exception("Incorrect method call for draw image!")
        #now that we have our vars, we need to sort our composite and image types
        if isinstance(img, CustomCanvas):
            #I am not sure how to sscale these down. ???
            if sx >= 0 or sy >= 0 or swidth <= 1 or sheight <= 1:
                raise Exception("Unsupported Canvas operation. Cannot Scale already drawn canvas instructions!")
            for instruction in CustomCanvas._group.children:
                self.group.add(instruction)
        else:
            tex_coords = [sx, sy, sx+swidth, sy, sx+swidth, sy+sheight, sx, sy+sheight]
            #top-left, top-right, right, left
            self.group.add(Rectangle(pos=(dx, dy), size=(dwidth, dheight), texture=img.texture, tex_coords=tex_coords))

        print(self.globalCompositeOperation + " was ignored!")
        #Do not currently do anything with self.globalCompositeOperation
        self.draw()

    def parseColor(self, color):
        #Once I have a base working with this method, change to use Color by default
        if re.match('#[0-9]{6}', color):
            #make a hex color to rgba
            self.group.add(Color(int(color[1:3]), int(color[3:5]), int(color[5:7]), 1  * self.globalAlpha))
        elif re.match('rgb\([0-9](\.[0-9])?,[0-9](\.[0-9])?,[0-9](\.[0-9])?\)', color):
            r = re.match('[0-9](\.[0-9])?', color)
            g = re.match('[0-9](\.[0-9])?', color[len(r.string)+1+4:])
            b = re.match('[0-9](\.[0-9])?', color[len(r.string)+len(g.string)+2+4:])
            self.group.add(Color(float(r.string), float(g.string), float(b.string), 1  * self.globalAlpha))
        elif re.match('rgba\([0-9](\.[0-9])?,[0-9](\.[0-9])?,[0-9](\.[0-9])?,[0-9](\.[0-9])?\)', color):
            r = re.match('[0-9](\.[0-9])?', color)
            g = re.match('[0-9](\.[0-9])?', color[len(r.string) + 1 + 5:])
            b = re.match('[0-9](\.[0-9])?', color[len(r.string) + len(g.string) + 2 + 5:])
            a = re.match('[0-9](\.[0-9])?', color[len(r.string) + len(g.string) + len(b.string) + 3 + 5])
            self.group.add(Color(float(r.string), float(g.string), float(b.string), float(a.string) * self.globalAlpha))
        else:
            raise Exception("The color/filltype is not supported/implemented!!! ", color)

    def createGradient(self, direction, *args):
        if direction == "horizontal":
            texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
        elif direction == "vertical":
            texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
        else:
            raise Exception("Unsupported gradient direction")
        buf = bytes([int(v * 255) for v in chain(*args)])  # flattens
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.tex_coords = [0, 1, 1, 1, 1, 0, 0, 0]
        self.gradient = texture

    def createPattern(self, image, wrap):
        self.fillStyle = "pattern"
        image.wrap = wrap
        self.pattern = image
        self.tex_coords = [0, 1, 1, 1, 1, 0, 0, 0]


    def normalize(self, value, max):
        return value / max


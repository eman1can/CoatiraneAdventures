from src.lwf.src.LWF import LWF, Format
import re

class BaseResourceCache:
    _instance = None

    @staticmethod
    def get():
        if LWF.BaseResourceCache._instance is None:
            LWF.BaseResourceCache._instance = LWF.BaseResourceCache()
        return LWF.BaseResourceCache._instance

    def __init__(self):
        self.cache = {}
        self.lwfInstanceIndex = 0
        self.canvasIndex = 0

    def getRendererName(self):
        return "webkitCSS"

    def clear(self):
        for k, cache in self.cache:
            for kk, lwfInstance in cache.instances:
                lwfInstance.destroy()
        self.cache = {}

    def getTextureURL(self, settings, data, texture):
        if 'imagePrefix' in settings:
            prefix = settings['imagePrefix']
        elif 'prefix' in settings:
            prefix = settings['prefix'];
        else:
            prefix = ""

        if 'imageSuffix' in settings:
            sufix = settings['imageSuffix']
        else:
            suffix = ""

        if 'imageQueryString' in settings:
            queryString = settings['imageQueryString']
        else:
            queryString = ""

        if len(queryString) > 0:
            queryString = "?" + queryString

        # imageMap = settings['imageMap']
        url = texture.filename
        # if callable(imageMap):
        #     newUrl = imageMap(settings, url)
        # if newUrl:
        #     url = newUrl
        # elif isinstance(imageMap, dict):
        #     newUrl = imageMap[url]
        #     if newUrl:
        #         url = newUrl
        if not (re.match('^/', url) or re.match('^https?://', url)):
            url = prefix + url
        url = url.replace('(\.gif|\.png|\.jpg)', suffix + "$1" + queryString)
        print("returning! ", url)
        return url

    def checkTextures(self, settings, data):
        settings._alphaMap = {}
        settings._colorMap = {}
        settings._textures = []

        re_o = '_atlas(.*)_info_' + '([0-9])_([0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)_([0-9]+)'
        re_rgb = '(.*)_rgb_([0-9a-f]{6})(.*)$'
        re_rgb10 = '(.*)_rgb_([0-9]*),([0-9]*),([0-9]*)(.*)$'
        re_rgba = '(.*)_rgba_([0-9a-f]{8})(.*)$'
        re_rgba10 = '(.*)_rgba_([0-9]*),([0-9]*),([0-9]*),([0-9]*)(.*)$'
        re_add = '(.*)_add_([0-9a-f]{6})(.*)$'
        re_add10 = '(.*)_add_([0-9]*),([0-9]*),([0-9]*)(.*)$'

        for texture in data.textures:
            orig = None
            if re.match(re_rgb, texture.filename):
                m = re.match(re_rgb, texture.filename)
                orig = m[1] + m[3]
                colorOp = "rgb"
                colorValue = m[2]
            elif re.match(re_rgb10, texture.filename):
                m = re.match(re_rgb10, texture.filename)
                orig = m[1] + m[5]
                colorOp = "rgb"
                r = hex(int(m[2], 10))[2:]
                g = hex(int(m[3], 10))[2:]
                b = hex(int(m[4], 10))[2:]
                colorValue = ("0" if len(r) == 1 else "") + r + \
                             ("0" if len(g) == 1 else "") + g + \
                             ("0" if len(b) == 1 else "") + b
            elif re.match(re_rgba, texture.filename):
                m = re.match(re_rgba, texture.filename)
                orig = m[1] + m[3]
                colorOp = "rgba"
                colorValue = m[2]
            elif re.match(re_rgba10, texture.filename):
                m = re.match(re_rgba10, texture.filename)
                orig = m[1] + m[6]
                colorOp = "rgba"
                r = hex(int(m[2], 10))[2:]
                g = hex(int(m[3], 10))[2:]
                b = hex(int(m[4], 10))[2:]
                a = hex(int(m[5], 10))[2:]
                colorValue = ("0" if len(r) == 1 else "") + r + \
                             ("0" if len(g) == 1 else "") + g + \
                             ("0" if len(b) == 1 else "") + b + \
                             ("0" if len(a) == 1 else "") + a
            elif re.match(re_add, texture.filename):
                m = re.match(re_add, texture.filename)
                orig = m[1] + m[3]
                colorOp = "add"
                colorValue = m[2]
            elif re.match(re_add10, texture.filename):
                m = re.match(re_add10, texture.filename)
                orig = m[1] + m[5]
                colorOp = "add"
                r = hex(int(m[2], 10))[2:]
                g = hex(int(m[3], 10))[2:]
                b = hex(int(m[4], 10))[2:]
                colorValue = ("0" if len(r) == 1 else "") + r + \
                             ("0" if len(g) == 1 else "") + g + \
                             ("0" if len(b) == 1 else "") + b

            if orig:
                ma = re.match(re_o, texture.filename)
                if ma:
                    orig = ma[1]
                    rotated = ma[2] == "1"
                    u = int(ma[3], 10)
                    v = int(ma[4], 10)
                    w = int(ma[5], 10)
                    h = int(ma[6], 10)
                    x = int(ma[7], 10)
                    y = int(ma[8], 10)
                else:
                    rotated = False
                    u = 0
                    v = 0
                    w = None
                    h = None
                    x = 0
                    y = 0
                if orig not in settings._colorMap:
                    settings._colorMap[orig] = []
                    settings._colorMap[orig].append({
                        'filename': texture.filename,
                        'colorOp': colorOp,
                        'colorValue': colorValue,
                        'rotated': rotated,
                        'u': u,
                        'v': v,
                        'w': w,
                        'h': h,
                        'x': x,
                        'y': y
                    })
                    continue
                settings._textures.append(texture)
                m = re.match('^(.*)_withalpha(.*\.)jpg(.*)$', texture.filename)
                if m:
                    pngFilename = m[1] + "_alpha" + m[2] + "png" + m[3]
                    t = Format.TextureReplacement(pngFilename)
                    settings._textures.append(t)
                    settings._alphaMap[texture.filename] = [texture, t]
                    settings._alphaMap[t.filename] = [texture, t]
        return

    def onloaddata(self, settings, data, url):
        if not data and data.check():
            settings.error.append({'url': url, 'reason': 'dataError'})
            settings['onload'](settings, None)
            return

        settings['name'] = data.name()

        self.checkTextures(settings, data)

        #Assume we have no scripts
        needsToLoadScript = data.useScript #and !global['lwf]?['Script']?[data.name()]?

        self.cache[settings['lwfUrl']].data = data
        settings.total = len(settings._textures) + 1
        # if needsToLoadScript:
        #   settings.total += 1
        settings.loadedCount = 1
        if 'onprogress' in settings:
            on_progress = settings['onprogress']
            on_progress(settings, settings.loadedCount, settings.total)

        # Assume that out lwfs require no scripts
        if needsToLoadScript:
            pass
        #   self.loadJs(settings, data)
        else:
            self.loadImages(settings, data)
        return


    def LoadLWF(self, settings):
        lwfUrl = settings['lwf']
        if not re.match('^/', lwfUrl):
            if 'prefix' in settings:
                lwfUrl = settings['prefix'] + lwfUrl
        settings['lwfUrl'] = lwfUrl
        settings['error'] = []

        if lwfUrl in self.cache:
            data = self.cache[lwfUrl].data
            if data:
                settings['name'] = data.name()
                self.checkTextures(settings, data)
                settings.total = len(settings._textures) + 1
                settings.loadedCount = 1
                if 'onprogress' in settings:
                    on_progress = settings['onprogress']
                    on_progress(settings, settings.loadedCount, settings.total)
                self.loadImages(settings, data)
                return
        self.cache[lwfUrl] = {}
        self.loadLWFData(settings, lwfUrl)

        # data = Data(file)
        # self.cache[lwfUrl] = data
        # settings['data'] = data
        # onload = settings['onload']
        # onload(settings)
        # return

    def dispatchOnloaddata(self, settings, url, data):
        data = CanvasLoader.load(data.data)
        print(data)

        self.onloaddata(settings, data, url)

    def loadLWFData(self, settings, url):
        self.dispatchOnloaddata(settings, url, open(url, 'rb').read())

    def loadImagesCallback(self, settings, imageCache, data):
        settings.loadedCount += 1
        if 'onprogress' in settings:
            on_progress = settings['onprogress']
            on_progress(settings, settings.loadedCount, settings.total)
        if settings.loadedCount is settings.total:
            del settings._alphaMap
            del settings._colorMap
            del settings._textures
            if len(settings.error) > 0:
                del self.cache[settings['lwf']]
                on_load = settings['onload']
                on_load(settings, None)
            else:
                self.newLWF(settings, imageCache, data)
        return

    def drawImage(self, ctx, image, o, u, v, w, h):
        if o.rotates:
            m = Matrix()
            Utility.RotateMatrix(m, Matrix(), 1, 0, w)
            ctx.setTransform(m.scaleX, m.skew1, m.skew0, m.scaleY, m.translateX, m.translateY)
        else:
            ctx.setTransform(1, 0, 0, 1, 0, 0)
        ctx.drawImage(image, u, v, w, h, 0, 0, w, h)
        ctx.setTransform(1, 0, 0, 1, 0, 0)
        return

    def getCanvasName(self):
        self.canvasIndex += 1
        return "__canvas__" + str(self.canvasIndex)

    def createCanvas(self, w, h):
        name = self.getCanvasName()
        canvas = CustomCanvas()
        canvas.width = w
        canvas.height = h
        ctx = canvas.getContext()
        canvas.name = name
        return (canvas, ctx)

    def generateImages(self, settings, imageCache, texture, image):
        d = settings._colorMap[texture.filename]
        if d:
            scaleX = image.width / texture.width
            scaleY = image.height / texture.height
            for o in d:
                u = round(o.u * scaleX)
                v = round(o.v * scaleY)
                w = round((o.w if o.w else texture.width) * scaleX)
                h = round((o.h if o.h else texture.height) * scaleY)
                if o.rotated:
                    iw = h
                    ih = w
                else:
                    iw = w
                    ih = h
                (canvas, ctx) = self.createCanvas(w, h)

                if o.colorOp == "rgb":
                    ctx.fillStyle = "#" + str(o.colorValue)
                    ctx.fillRect(0, 0, w, h)
                    ctx.globalCompositeOperation = "destination-in"
                    self.drawImage(ctx, image, o, u, v, iw, ih)
                elif o.colorOp == "rgba":
                    self.drawImage(ctx, image, o, u, v, iw, ih)
                    ctx.globalCompositeOperation = "source-atop"
                    val = o.colorValue
                    r = int(val[0:2], 16)
                    g = int(val[2:2], 16)
                    b = int(val[4:2], 16)
                    a = int(val[6:2], 16) / 255
                    ctx.fillStyle = "rgba(" + str(r) + ", " + str(g) + ", " + str(b) + ", " + str(a) + ")"
                    ctx.fillRect(0, 0, w, h)
                elif o.colorOp == "add":
                    canvasAdd = CustomCanvas()
                    canvasAdd.width = w
                    canvasAdd.height = h
                    ctxAdd = canvasAdd.getContext()
                    ctxAdd.fillStyle = "#" + str(o.colorValue)
                    ctxAdd.fillRect(0, 0, w, h)
                    ctxAdd.globalCompositeOperation = "destination-in"
                    self.drawImage(ctxAdd, image, o, u, v, iw, ih)
                    self.drawImage(ctx, image, o, u, v, iw, ih)
                    ctx.globalCompositeOperation = "lighter"
                    ctx.drawImage(canvasAdd, 0, 0, canvasAdd.width, canvasAdd.height, 0, 0, canvasAdd.width, canvasAdd.height)
                ctx.globalCompositeOperation = "source-over"
                imageCache[o.filename] = canvas
        return

    def loadImages(self, settings, data):
        imageCache = {}

        if len(data.textures) == 0:
            self.newLWF(settings, imageCache, data)
            return

        for texture in settings._textures:
            url = self.getTextureURL(settings, data, texture)
            def do(texture, url):
                image = CustomImage()
                def onabort():
                    settings.error.append({'url':url, 'reason':"abort"})
                    image = image.onload = image.onabort = image.onerror = None
                    self.loadImagesCallback(settings, imageCache, data)
                image.onabort = onabort
                def onerror():
                    settings.error.append({'url': url, 'reason': "error"})
                    image = image.onload = image.onabort = image.onerror = None
                    self.loadImagesCallback(settings, imageCache, data)
                image.onerror = onerror
                def onload():
                    imageCache[texture.filename] = image.data
                    d = settings._alphaMap[texture.filename]
                    if d:
                        jpg = d[0]
                        alpha = d[1]
                        jpgImg = imageCache[jpg.filename]
                        alphaImg = imageCache[alpha.filename]
                        if jpgImg and alphaImg:
                            (canvas, ctx) = self.createCanvas(jpgImg.width, jpgImg.height)
                            ctx.drawImage(jpgImg, 0, 0, jpgImg.width, jpgImg.height, 0, 0, jpgImg.width, jpgImg.height)
                            ctx.globalCompositeOperation = "destination-in"
                            ctx.drawImage(alphaImg, 0, 0, alphaImg.width, alphaImg.height, 0, 0, jpgImg.width, jpgImg.height)
                            ctx.globalCompositeOperation = "source-over"
                            del imageCache[jpg.filename]
                            del imageCache[alpha.filename]
                            imageCache[jpg.filename] = canvas
                            self.generateImages(settings, imageCache, jpg, canvas)
                        else:
                            self.generateImages(settings, imageCache, texture, image.data)

                        image = image.onload = image.onabort = image.onerror = None
                        self.loadImagesCallback(settings, imageCache, data)
                image.onload = onload
                image.src = url
            do(texture, url)
        return

    def newFactory(self, settings, cache, data):
        return BaseRendererFactory(data, self, cache, settings['stage'],
                                   settings['textInSubpixel'] if 'textInSubPixel' in settings else False,
                                   settings['use3D'] if 'use3D' in settings else False,
                                   settings['recycleTextCanvas'] if 'recycleTextCanvas' in settings else False,
                                   settings['quirkyClearRect'] if 'quirkyClearRect' in settings else False)

    def onloadLWF(self, settings, lwf):
        factory = lwf.rendererFactory
        if 'setBackgroundColor' in settings:
            factory.setBackgroundColor(settings['setBackgroundColor'])
        elif 'useBackgroundColor' in settings:
            factory.setBackgroundColor(lwf)
        if 'fitForHeight' in settings:
            factory.fitForHeight(lwf)
        elif 'fitForWidth' in settings:
            factory.fitForWidth(lwf)
        on_load = settings['onload']
        on_load(settings, lwf)

    def newLWF(self, settings, imageCache, data):
        lwfUrl = settings['lwfUrl']
        cache = self.cache['lwfUrl']
        factory = self.newFactory(settings, imageCache, data)
        #ignoring scripts
        #embeddedScript = global["lwf"]?["Script"]?[data.name()] if data.useScript
        lwf = LWF(data, factory)
        if 'active' in settings:
            lwf.active = settings['active']
        lwf.url = settings['lwfUrl']
        self.lwfInstanceIndex += 1
        lwf.lwfInstanceId = self.lwfInstanceIndex
        if cache.instances is None:
            cache.instances = {}
        cache.instances[lwf.lwfInstanceId] = lwf
        parentLWF = settings['parentLWF']
        if parentLWF:
            parentLWF.loadedLWFs[lwf.lwfInstanceId] = lwf
        if 'preferredFrameRate' in settings:
            pass
        if 'execLimit' in settings:
            lwf.SetPreferredFrameRate(settings['preferredFrameRate'], settings['execLimit'])
        else:
            lwf.SetPreferredFrameRate(settings['preferredFrameRate'])
        self.onloadLWF(settings, lwf)
        return

    def unloadLWF(self, lwf):
        cache = self.cache[lwf.url]
        if cache:
            if lwf.lwfInstanceId:
                del cache.instances[lwf.lwfInstanceId]
                empty = True
                for k, v in cache.instances:
                    empty = False
                    break
                if empty:
                    # we ignore scripts
                    #     try:
                    #         if cache.scripts:
                    #             head = document.getElementsByTagName('head')[0]
                    #             for script in cache.scripts
                    #                 head.removeChild(script)
                    #     catch e
                    del self.cache[lwf.url]
        return

    def loadLWFs(self, settingsArray, onloadall):
        loadTotal = len(settingsArray)
        loadedCount = 0
        errors = None
        for settings in settingsArray:
            onload = settings['onload']
            def do(onload):
                def on_load(lwf):
                    if onload:
                        onload(lwf)
                    if len(settings.error) > 0:
                        if errors is not None:
                            errors = []
                        errors = errors.append(settings.error)
                    loadedCount += 1
                    if loadTotal == loadedCount:
                        onloadall(errors)
                settings['onload'] = on_load
            do(onload)
            self.LoadLWF(settings)

    def getCache(self):
        return self.cache

    def setParticleConstructor(self, ctor):
        self.particleConstructor = ctor
        return

    # We do not use DOM elements. No need for this
    # def setDOMElementCOnstructor(self, ctor):
    #     self.domElementConstructor = ctor
    #     return

class ResourceCache(BaseResourceCache):

    def getRendererName(self):
        return "Canvas"

    def newFactory(self, settings, cache, data):
        return LWF.RendererFactory(data, self, cache, settings['stage'],
                                   settings['textInSubpixel'] if 'textInSubpixel' in settings else False,
                                   settings['needsClear'] if 'needsClear' in settings else True,
                                   settings['quirkyClearRect'] if 'quirkyClearRect' in settings else False)

    def generateImages(self, settings, imageCache, texture, image):
        m = re.match('_withpadding', texture.filename)
        if m:
            w = image.width + 2
            h = image.height + 2
            canvas = CustomCanvas()
            canvas.width = 2
            canvas.height = h
            canvas.name = self.getCanvasName()
            ctx = canvas.getContext()
            canvas.widthPadding = True
            ctx.drawImage(image, 0, 0, image.width, image.height, 1, 1, image.width, image.height)
            imageCache[texture.filename] = canvas
        super().generateImages(settings, imageCache, texture, image)
        return

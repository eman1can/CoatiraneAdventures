# coding=utf-8

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Canvas, Rectangle, Translate
from kivy.clock import Clock
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import (StringProperty, ListProperty, BooleanProperty,
                             OptionProperty)
from kivy.uix.behaviors import DragBehavior
from kivy.properties import NumericProperty
from kivy.graphics import Color, Mesh
from kivy.lang import Builder
import spine
from spine.SkeletonJson import SkeletonJson
from os.path import dirname, join, realpath
from kivy.core.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
kv = """
SkeletonViewer:
    pause: pause.state == 'down'
    scale: round(scale.value / 20.0, 2)
    mix: round(mix.value / 10.0, 2)
    speed: round(speed.value / 10.0, 2)
    percent: round(percentSlider.value, 2)
    flipX: x.active
    flipY: y.active
    debugBones: bones.active
    debugRegions: regions.active
    debugBounds: bounds.active
    debugMeshHull: meshhull.active
    debugMeshTriangles: meshtriangles.active
    alphaP: premultiplied.active
    loop: loop.active
    skeletonX: round(xPos.value * 10, 2)
    skeletonY: round(yPos.value * 10, 2)
    size_hint: 1, 1
    FloatLayout:
        size: 1, 1
        id: layout
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: .1, .1, .1, 1
            Rectangle:
                size: 300, self.height
                pos: 0,0
        # CanvasDrawing:
        #     id: drawing
        Label:
            canvas.before:
                Color:
                    rgba: .3, .3, .3, 1
                Rectangle:
                    size: 300, 20
                    pos: self.pos
            text: "Skeleton"
            font_size: 16 
            size_hint: None, None
            size : self.texture_size
            pos: 0, root.height - 20
        GridLayout:
            cols: 1
            row_default_height: 45
            row_force_default: True
            col_default_width: 300
            orientation: "vertical"
            size_hint: None, None
            size: 300, self.parent.height - 20
            pos: 0,0
            FloatLayout:
                Label:
                    size_hint: None, None
                    size: self.texture_size
                    font_size: 16
                    text: "Skeleton:"
                    pos: self.parent.pos
                Button:
                    id: browse
                    size_hint: None, None
                    size: self.texture_size
                    pos: self.parent.pos[0] + self.parent.width - self.width, self.parent.pos[1]
                    text: "Browse"
                    on_touch_down: root.openSkeleton()
            FloatLayout:
                Label:
                    size_hint: None, None
                    size: 100, self.texture_size[1]
                    font_size: 16
                    halign: 'right'
                    text: "Scale: "
                    pos: self.parent.pos
                Label:
                    size_hint: None, None
                    size: self.texture_size
                    font_size: 16
                    text: "" + str(round(scale.value, 2))
                    pos: self.parent.pos[0] + 100, self.parent.pos[1]
                Slider:
                    id: scale
                    value: 18.6
                    size_hint: None, None
                    size: 150, 20
                    pos: self.parent.pos[0] + self.parent.width - self.width, self.parent.pos[1]
            BoxLayout:
                Label:
                    size_hint: None, None
                    size: 100, self.texture_size[1]
                    pos: self.parent.pos
                    font_size: 16
                    halign: 'right'
                    text: "Flip:"
                CheckBox:
                    id: x
                Label:
                    font_size: 16
                    text: "X"
                CheckBox:
                    id: y
                Label:
                    font_size: 16
                    text: "Y"
                
            BoxLayout:
                height: 90
                Label:
                    size_hint: None, None
                    size: 100, self.texture_size[1]
                    pos: self.parent.pos
                    font_size: 16
                    halign: 'right'
                    text: "Debug:"
                BoxLayout:
                    orientation: 'vertical'
                    BoxLayout:
                        CheckBox:
                            id: bones
                        Label:
                            font_size: 16
                            text: "Bones"
                            size: self.texture_size
                        CheckBox:
                            id: regions
                        Label:
                            font_size: 16
                            text: "Regions"
                            size: self.texture_size
                    BoxLayout:
                        CheckBox:
                            id: bounds
                        Label:
                            font_size: 16
                            text: "Bounds"
                            size: self.texture_size
                        CheckBox:
                            id: meshhull
                        Label:
                            font_size: 16
                            text: "Mesh Hull" 
                            size: self.texture_size
                    BoxLayout:
                        CheckBox:
                            id: meshtriangles
                        Label:
                            font_size: 16
                            text: "Mesh Triangles"
                            size: self.texture_size
            BoxLayout:
                Label:
                    size_hint: None, None
                    size: 100, self.texture_size[1]
                    font_size: 16
                    halign: 'right'
                    text: "Alpha:"
                CheckBox:
                    id: premultiplied
                Label:
                    font_size: 16
                    text: "Premultiplied"
                    size: self.texture_size
            FloatLayout:        
                Label:
                    size_hint: None, None
                    size: 100, self.texture_size[1]
                    font_size: 16
                    halign: 'right'
                    text: "Mix: "
                    pos: self.parent.pos
                Label:
                    size_hint: None, None
                    size: self.texture_size
                    font_size: 16
                    text: "" + str(round(mix.value, 2))
                    pos: self.parent.pos[0] + 100, self.parent.pos[1]
                Slider:
                    id: mix
                    size_hint: None, None
                    size: 150, 20
                    pos: self.parent.pos[0] + self.parent.width - self.width, self.parent.pos[1]
            FloatLayout:     
                Label:
                    size_hint: None, None
                    size: 100, self.texture_size[1]
                    font_size: 16
                    halign: 'right'
                    text: "Speed: "
                    pos: self.parent.pos
                Label:
                    size_hint: None, None
                    size: self.texture_size
                    font_size: 16
                    text: "" + str(round(speed.value, 2))
                    pos: self.parent.pos[0] + 100, self.parent.pos[1]
                Slider:
                    id: speed
                    value: 10.0
                    size_hint: None, None
                    size: 150, 20
                    pos: self.parent.pos[0] + self.parent.width - self.width, self.parent.pos[1]
            FloatLayout:
                Label:
                    size_hint: None, None
                    size: 100, self.texture_size[1]
                    font_size: 16
                    halign: 'right'
                    text: "Percent: "
                    pos: self.parent.pos
                Label:
                    size_hint: None, None
                    size: self.texture_size
                    font_size: 16
                    text: "" + str(round(percentSlider.value, 2))
                    pos: self.parent.pos[0] + 100, self.parent.pos[1]
                Slider:
                    id: percentSlider
                    value: 0.0
                    size_hint: None, None
                    sie: 150, 20
                    pos: self.parent.pos[0] + self.parent.width - self.width, self.parent.pos[1] - 50
            BoxLayout:   
                Label:
                    size_hint: None, None
                    size: 100, self.texture_size[1]
                    font_size: 16
                    halign: 'right'
                    pos: self.parent.pos
                    text: "Playback:"
                ToggleButton:
                    id: pause
                    size: self.texture_size
                    size_hint: None, None
                    text: "Pause"
                CheckBox:
                    id: loop
                    active: True
                Label:
                    font_size: 16
                    text: "Loop"
                    size: self.texture_size
            BoxLayout:
                Label:
                    size_hint: None, None
                    size: 100, self.texture_size[1]
                    font_size: 16
                    halign: 'right'
                    pos: self.parent.pos
                    text: "X Position"
                Label:
                    size_hint: None, None
                    size: self.texture_size
                    font_size: 16
                    text: "" + str(round(xPos.value, 2))
                    pos: self.parent.pos[0] + 100, self.parent.pos[1]
                Slider:
                    id: xPos
                    value: 75.42
                    size_hint: None, None
                    size: 150, 20
                    pos: self.parent.pos[0] + self.parent.width - self.width, self.parent.pos[1]
            BoxLayout:
                Label:
                    size_hint: None, None
                    size: 100, self.texture_size[1]
                    font_size: 16
                    halign: 'right'
                    pos: self.parent.pos
                    text: "Y Position"    
                Label:
                    size_hint: None, None
                    size: self.texture_size
                    font_size: 16
                    text: "" + str(round(yPos.value, 2))
                    pos: self.parent.pos[0] + 100, self.parent.pos[1]   
                Slider:
                    id: yPos
                    value: 39.83
                    size_hint: None, None
                    size: 150, 20
                    pos: self.parent.pos[0] + self.parent.width - self.width, self.parent.pos[1]  
            Label:
                id: spacer
            Spinner:
                text: "Animations:"
                id: animations
                values: root.animations
                on_text: root.animationCurrent = self.text
                
            Spinner:
                text: "Skins:"
                id: skins
                values: root.skins
                on_text: root.skinCurrent = self.text
                
        SpineDrawing:
            pos: 1000, 500
            size: 1000, 1000
<CanvasDrawing>:
    width: 950
    pos: 300, 0
    id: drawing
"""
class Skeleton(spine.Skeleton):
    def __init__(self, skeletonData):
        super(Skeleton, self).__init__(skeletonData=skeletonData)
        self.x = 0
        self.y = 0
        self.texture = None
        self.debug = False
        self.pause = False
        self.images = []
        self.clock = None

    def draw(self, canvas):
        canvas.clear()
        for slot in self.drawOrder:
            if not slot.attachment:
                continue
            slot.attachment.debugRegions = self.debugRegions
            slot.attachment.skeletonX = self.x
            slot.attachment.skeletonY = self.y
            slot.attachment.draw(slot, canvas)

class MeshAttachment(spine.MeshAttachment):
    def __init__(self, mesh):
        super(MeshAttachment, self).__init__()
class SkinnedMeshAttachment(spine.SkinnedMeshAttachment):
    def __init__(self, skinnedMesh):
        super(SkinnedMeshAttachment, self).__init__()
class BoundingBoxAttachment(spine.BoundingBoxAttachment):
    def __init__(self, boundingBox):
        super(BoundingBoxAttachment, self).__init__()
class RegionAttachment(spine.RegionAttachment):
    def __init__(self, region):
        super(RegionAttachment, self).__init__()
        self.texture = region.page.texture.get_region(region.x, region.y, region.width, region.height)
        u, v = self.texture.uvpos
        uw, vh = self.texture.uvsize
        self.u = u
        self.v = v
        self.u2 = u + uw
        self.v2 = v + vh
        self.first_time = True
        if region.rotate:
            self._tex_coords = (
                self.u2,  # self.vertices[0].texCoords.x
                self.v2,  # self.vertices[0].texCoords.y
                self.u,  # self.vertices[1].texCoords.x
                self.v2,  # self.vertices[1].texCoords.y
                self.u,  # self.vertices[2].texCoords.x
                self.v,  # self.vertices[2].texCoords.y
                self.u2,  # self.vertices[3].texCoords.x
                self.v,  # self.vertices[3].texCoords.y
            )
        else:
            self._tex_coords = (
                self.u,  # self.vertices[0].texCoords.x
                self.v2,  # self.vertices[0].texCoords.y
                self.u,  # self.vertices[1].texCoords.x
                self.v,  # self.vertices[1].texCoords.y
                self.u2,  # self.vertices[2].texCoords.x
                self.v,  # self.vertices[2].texCoords.y
                self.u2,  # self.vertices[3].texCoords.x
                self.v2  # self.vertices[3].texCoords.y
            )

    def prepare_graphics(self, canvas):
        self._mesh_vertices = vertices = [0] * 16
        vertices[2::4] = self._tex_coords[::2]
        vertices[3::4] = self._tex_coords[1::2]
        self.canvas = Canvas()
        with self.canvas:
            Color(1, 1, 1, 1)
            # PushMatrix()
            self.g_mesh = Mesh(vertices=vertices,
                               indices=range(4),
                               mode="triangle_fan",
                               texture=self.texture)
            self.g_debug_color = Color(1, 0, 0, 1)
            self.g_debug_mesh = Mesh(vertices=vertices,
                                     indices=range(4),
                                     mode="line_loop", )
            # Translate(x=200, y=200)
            # PopMatrix()

    def draw(self, slot, canvas):
        if self.first_time:
            self.first_time = False
            self.prepare_graphics(canvas)

        skeleton = slot.skeleton
        canvas.add(self.canvas)

        self.updateOffset()
        self.updateWorldVertices(slot.bone)

        # update graphics
        self.g_mesh.vertices = self._mesh_vertices
        # print(self.g_mesh.vertices)
        if self.debugRegions:
            self.g_debug_mesh.vertices = self._mesh_vertices
            self.g_debug_color.a = 1
        else:
            self.g_debug_color.a = 0

    def updateWorldVertices(self, bone):
        x = bone.worldX + self.skeletonX
        y = bone.worldY + self.skeletonY
        m00 = bone.m00
        m01 = bone.m01
        m10 = bone.m10
        m11 = bone.m11
        offset = self.offset
        v = self._mesh_vertices
        v[0::4] = [
            offset[0] * m00 + offset[1] * m01 + x,
            offset[2] * m00 + offset[3] * m01 + x,
            offset[4] * m00 + offset[5] * m01 + x,
            offset[6] * m00 + offset[7] * m01 + x
        ]
        v[1::4] = [
            offset[0] * m10 + offset[1] * m11 + y,
            offset[2] * m10 + offset[3] * m11 + y,
            offset[4] * m10 + offset[5] * m11 + y,
            offset[6] * m10 + offset[7] * m11 + y]
class AtlasAttachmentLoader(spine.AttachmentLoader.AttachmentLoader):
    def __init__(self, atlas):
        super(AtlasAttachmentLoader, self).__init__()
        if atlas is None:
            raise Exception("Atlas cannot be None")
        self.atlas = atlas

    def newAttachment(self, tp, name):
        if tp == spine.AttachmentLoader.AttachmentType.region:
            region = self.atlas.findRegion(name)
            if not region:
                raise Exception("Atlas region not found: ", name)
            return RegionAttachment(region)

        elif tp == spine.AttachmentLoader.AttachmentType.mesh:
            mesh = self.atlas.findRegion(name)
            if not mesh:
                raise Exception("Atlas region not found: ", name)
            return MeshAttachment(name)
        elif tp == spine.AttachmentLoader.AttachmentType.skinnedMesh:
            skinnedMesh = self.atlas.findRegion(name)
            if not skinnedMesh:
                raise Exception("Atlas region not found: ", name)
            return SkinnedMeshAttachment(name)
        elif tp == spine.AttachmentLoader.AttachmentType.boundingBox:
            boundingBox = self.atlas.findRegion(name)
            if not boundingBox:
                raise Exception("Atlas region not found: ", name)
            return BoundingBoxAttachment(name)
        else:
            raise Exception('Unknown attachment type: ', type)
class AtlasPage(spine.AtlasPage):
    def __init__(self):
        super(AtlasPage, self).__init__()
        self.texture = None
class AtlasRegion(spine.AtlasRegion):
    def __init__(self):
        super(AtlasRegion, self).__init__()
        self.page = None
class Atlas(spine.Atlas):
    def __init__(self, filename):
        self.atlas_dir = dirname(filename)
        super(Atlas, self).__init__()
        super(Atlas, self).loadWithFile(filename)

    def newAtlasPage(self, name):
        page = AtlasPage()
        filename = realpath(join(self.atlas_dir, name))
        if filename:
            page.texture = Image(filename).texture
            page.texture.flip_vertical()
        return page

    def newAtlasRegion(self, page):
        region = AtlasRegion()
        region.page = page
        return region

    def findRegion(self, name):
        return super(Atlas, self).findRegion(name)
class SkeletonViewer(Widget):
    animations = ListProperty([])
    skins = ListProperty([])
    skinCurrent = StringProperty("")
    animationCurrent = StringProperty("")
    pause = BooleanProperty(False)
    alphaP = BooleanProperty(False)
    loop = BooleanProperty(False)
    speed = NumericProperty(1.0)
    scale = NumericProperty(0.0)
    mix = NumericProperty(0.0)
    flipX = BooleanProperty(False)
    flipY = BooleanProperty(False)
    debugBones = BooleanProperty(False)
    debugRegions = BooleanProperty(False)
    debugBounds = BooleanProperty(False)
    debugMeshHull = BooleanProperty(False)
    debugMeshTriangles = BooleanProperty(False)
    skeletonX = NumericProperty(50)
    skeletonY = NumericProperty(50)
    percent = NumericProperty(0)
    def __init__(self):
        super(SkeletonViewer, self).__init__()
        self.drawing = CanvasDrawing()
        self.drawing.viewer = self
        self.drawing.filename = 'data/dragon'
        self.add_widget(self.drawing)
        print("Making viewer")
        print(str(self.children))


    def on_skinCurrent(self, instance, value):
        if self.skinCurrent != "Skin:":
            print(self.skinCurrent)

    def on_animationCurrent(self, instance, value):
        if self.animationCurrent != "Animation:":
            # print(self.animationCurrent)
            self.drawing.animate(self.animationCurrent)

    def on_flipX(self, *args):
        print("FlipX: " + str(self.flipX))
        self.drawing.skeleton.flipX = self.flipX
        self.drawing.skeleton.updateWorldTransform()

    def on_flipY(self, *args):
        print("FlipY: " + str(self.flipY))
        self.drawing.skeleton.flipY = self.flipY
        self.drawing.skeleton.updateWorldTransform()

    def on_debugBones(self, *args):
        print("DBones: " + str(self.debugBones))

    def on_debugRegions(self, *args):
        print("DRegions: " + str(self.debugRegions))
        self.drawing.skeleton.debugRegions = self.debugRegions

    def on_debugBounds(self, *args):
        print("DBounds: " + str(self.debugBounds))

    def on_debugMeshHull(self, *args):
        print("DMeshHull: " + str(self.debugMeshHull))

    def on_debugMeshTriangles(self, *args):
        print("DMeshTriangles: " + str(self.debugMeshTriangles))

    def on_alphaP(self, *args):
        print("PAlpha: " + str(self.alphaP))

    def on_loop(self, *args):
        if not self.drawing.animated:
            Clock.schedule_interval(self.drawing.update, 1 / 60)

    def on_scale(self, *args):
        print("Scale: " + str(self.scale))
        self.drawing.skeleton.setScale(self.scale, self.scale)
        self.drawing.skeleton.updateWorldTransform()

    def on_pause(self, *args):
        print("Pause: " + str(self.pause))
        self.drawing.animated = False

    def on_mix(self, *args):
        print("Mix: " + str(self.mix))

    def on_skeletonX(self, *args):
        print("SkeletonX:  " + str(self.skeletonX))
        self.drawing.skeleton.setPosition(self.skeletonX, self.skeletonY)
        self.drawing.skeleton.updateWorldTransform()
        # self.drawing.skeleton.draw(self.canvas)

    def on_skeletonY(self, *args):
        print("SkeletonX:  " + str(self.skeletonY))
        self.drawing.skeleton.setPosition(self.skeletonX, self.skeletonY)
        self.drawing.skeleton.updateWorldTransform()
        # self.skeleton.draw(self.canvas)

    def openSkeleton(self, *args):
        print("open new skeleton")
        if self.drawing.animated:
            self.drawing.animated = False
            Clock.unschedule(self.drawing.update)
        self.chooser = FileChooserListView(path = "C:/Users/Zoe Wolfe/.kivy/garden/garden.spine/examples/data", filters=['*.json'])

        self.popup = Popup(title='Test popup', content=self.chooser, auto_dismiss=False)
        self.chooser.add_widget(Button(text="Cancel", on_release=self.cancelSkeleton, size_hint=(None, None)))
        self.chooser.add_widget(Button(text="Select", pos=(self.chooser.width, 0), size_hint=(None, None), on_release=self.openSkeletonChosen))
        self.popup.open()

    def cancelSkeleton(self, *args):
        self.popup.dismiss()

    def openSkeletonChosen(self, *args):
        print("option chosen")
        self.popup.dismiss()
        print(str(self.chooser.selection[0].rsplit("\\", 1)[1][:-5]))
        self.drawing = CanvasDrawing()
        self.drawing.filename = "data\\"+str(self.chooser.selection[0].rsplit("\\", 1)[1][:-5])
        # self.animation.apply(skeleton=self.skeleton, time=self.frameNumber, loop=self.loop)
        # self.skeleton.setPosition(self.skeletonX, self.skeletonY)
        # self.skeleton.updateWorldTransform()
        # self.skeleton.draw(self.canvas)
class SpineDrawing(Widget):
    def __init__(self, **kwargs):
        super(SpineDrawing, self).__init__(**kwargs)

class CanvasDrawing(Widget):
    filename = StringProperty()
    animated = BooleanProperty(False)
    frameNumber = NumericProperty(0)
    frameCount = NumericProperty(0)

    def __init__(self, **kwargs):
        self.char = SpineDrawing()
        self.canvas = self.char.canvas
        self.canvas = Canvas()
        self.frameNumber = 0
        super(CanvasDrawing, self).__init__(**kwargs)
        # Clock.schedule_interval(self.update, 0)

    def on_animated(self, *args):
        if not self.animated:
            Clock.unschedule(self.update)

    def on_filename(self, *args):
        print(self.filename)
        self.load_spine_asset(self.filename)
        self.canvas.clear()
        self.viewer.animations = [animation.name for animation in self.skeletonData.animations]
        self.viewer.skins = [skin.name for skin in self.skeletonData.skins]
        self.frameNumber = 0
        self.animate(self.viewer.animations[0])
        # Clock.unschedule(self.update)
        self.skeleton.setPosition(self.viewer.skeletonX, self.viewer.skeletonY)



    def load_spine_asset(self, basefn):
        atlas = Atlas(filename="{}.atlas".format(basefn))
        loader = AtlasAttachmentLoader(atlas)
        skeletonJson = SkeletonJson(loader)
        self.skeletonData = skeletonJson.readSkeletonDataFile("{}.json".format(basefn))
        self.skeleton = Skeleton(skeletonData=self.skeletonData)
        self.skeleton.debugRegions = False
        self.animation = None


    def animate(self, name):
        self.animated = True
        self.animation = self.skeletonData.findAnimation(name)
        self.frameCount = self.animation.duration
        print("Duration: " + str(self.frameCount))
        skeleton = self.skeleton
        skeleton.setToBindPose()
        skeleton.flipX = self.viewer.flipX
        skeleton.flipY = self.viewer.flipY
        skeleton.updateWorldTransform()

    def on_percent(self, *args):
        print("Animation Percent: " + str(self.viewer.percent))
        if self.animation:
            self.animation.apply(skeleton=self.skeleton, time = self.viewer.percent / 100 / (1 / self.viewer.speed), loop=False)
            self.skeleton.updateWorldTransform()
            self.skeleton.draw(self.canvas)

    def update(self, dt):
        if not self.viewer.pause:
            if self.animation:
                if not self.viewer.loop:
                    if self.frameCount-self.frameNumber <= 0.01:
                        self.animated = False
                        # Clock.unschedule(self.update)
                else:
                    if self.frameCount-self.frameNumber <= 0.01:
                        self.frameNumber = 0
                self.frameNumber=((Clock.get_time() / 1/self.viewer.speed) % self.frameCount)
                print(str("Frame: " + str(self.frameNumber)))
                # self.percentSlider = self.frameNumber * 100

                #     self.frameNumber += 1
                #     self.animation.apply(skeleton=self.skeleton, time=self.frameNumber / (1 / self.speed), loop=self.loop)
                #Animation does time = time % duration, so time % 1
                self.animation.apply(skeleton=self.skeleton, time=self.frameNumber, loop=self.viewer.loop)
                self.skeleton.setPosition(self.viewer.skeletonX, self.viewer.skeletonY)
                self.skeleton.updateWorldTransform()
                self.skeleton.draw(self.canvas)





    # def on_speed(self, *args):
    #     print("Speed: " + str(self.speed))
    #     Clock.unschedule(self.update)
    #     if self.speed > 0:
    #         if self.loop:
    #             if self.speed < 5:
    #                 Clock.schedule_interval(self.update, 0)
    #             else:
    #                 Clock.schedule_interval(self.update, .5 / self.speed)
    #         else:
    #             Clock.schedule_once(self.update)




    # def on_loop(self, *args):
    #     print("Loop: " + str(self.loop))
        # self.animated = True
        # Clock.unschedule(self.update)
        # # if self.loop:
        # if self.speed < 5:
        #     Clock.schedule_interval(self.update, 0)
        # else:
        #     Clock.schedule_interval(self.update, .5 / self.speed)
        # else:
        #     Clock.schedule_once(self.update)


class SpineApp(App):
    title = "Skeleton Viewer"

    def build(self):
        Window.size = (1250, 800)
        from kivy.lang import Builder
        return Builder.load_string(kv)


if __name__ == "__main__":
    SpineApp().run()


import os

os.environ['KIVY_HOME'] = '../config'

from src.spine.skeleton.skeletonrendererdebug import SkeletonRendererDebug

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Canvas
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.properties import NumericProperty

from src.modules.KivyBase.Hoverable import FileChooserListViewBase
from src.spine.animation.animationstate import AnimationState
from src.spine.animation.animationstatedata import AnimationStateData
from src.spine.skeleton.skeletonloader import SkeletonLoader
from src.spine.skeleton.skeletonrenderer import SkeletonRenderer
from tools.movegenerator import PopupBase

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
    RelativeLayout:
        size: self.parent.width * 0.3, self.parent.height
        id: layout
        canvas.before:
            Color:
                rgba: .1, .1, .1, 1
            Rectangle:
                size: self.width, self.height
                pos: 0,0
        GridLayout:
            cols: 1
            rows: 15
            orientation: "vertical"
            size_hint: 1, 1
            pos: 0,0
            RelativeLayout:
                Label:
                    size_hint: 0.5, 1
                    font_size: 16
                    text: "Skeleton:"
                Button:
                    id: browse
                    size_hint: 0.5, 1
                    pos_hint: {'x': 0.5}
                    text: "Browse"
                    on_release: root.open_skeleton()
            RelativeLayout:
                Label:
                    size_hint: 0.2, 1
                    font_size: 16
                    text: "Scale: "
                Label:
                    size_hint: 0.2, 1
                    pos_hint: {'x': 0.2}
                    font_size: 16
                    text: "" + str(round(scale.value, 2))
                Slider:
                    id: scale
                    value: 0.25
                    min: 0.01
                    max: 20
                    size_hint: 0.6, 1
                    pos_hint: {'x': 0.4}
            RelativeLayout:
                Label:
                    size_hint: 0.2, 1
                    font_size: 16
                    text: "Flip:"
                RelativeLayout:
                    size_hint: 0.4, 1
                    pos_hint: {'x': 0.2}
                    CheckBox:
                        size_hint: 0.5, 1
                        id: x
                    Label:
                        size_hint: 0.5, 1
                        pos_hint: {'x': 0.5}
                        font_size: 16
                        text: "X"
                RelativeLayout:
                    size_hint: 0.4, 1
                    pos_hint: {'x': 0.6}
                    CheckBox:
                        size_hint: 0.5, 1
                        id: y
                    Label:
                        size_hint: 0.5, 1
                        pos_hint: {'x': 0.5}
                        font_size: 16
                        text: "Y"
                
            RelativeLayout:
                Label:
                    size_hint: 0.2, 1
                    font_size: 16
                    text: "Debug:"
                RelativeLayout:
                    size_hint: 0.8, 1
                    pos_hint: {'x': 0.2}
                    RelativeLayout:
                        size_hint: 1, 0.5
                        pos_hint: {'y': 0.5}
                        CheckBox:
                            size_hint: 0.1, 1
                            id: bones
                        Label:
                            size_hint: 0.2, 1
                            pos_hint: {'x': 0.1}
                            font_size: 16
                            text: "Bones"
                        CheckBox:
                            size_hint: 0.1, 1
                            pos_hint: {'x': 0.3}
                            id: regions
                        Label:
                            size_hint: 0.2, 1
                            pos_hint: {'x': 0.4}
                            font_size: 16
                            text: "Regions"
                        CheckBox:
                            size_hint: 0.1, 1
                            pos_hint: {'x': 0.6}
                            id: bounds
                        Label:
                            size_hint: 0.2, 1
                            pos_hint: {'x': 0.7}
                            font_size: 16
                            text: "Bounds"
                    RelativeLayout:
                        size_hint: 1, 0.5
                        CheckBox:
                            size_hint: 0.1, 1
                            id: meshhull
                        Label:
                            size_hint: 0.3, 1
                            pos_hint: {'x': 0.1}
                            font_size: 16
                            text: "Mesh Hull" 
                        CheckBox:
                            size_hint: 0.1, 1
                            pos_hint: {'x': 0.4}
                            id: meshtriangles
                        Label:
                            size_hint: 0.4, 1
                            pos_hint: {'x': 0.5}
                            font_size: 16
                            text: "Mesh Triangles"
            RelativeLayout:
                Label:
                    size_hint: 0.2, 1
                    font_size: 16
                    text: "Alpha:"
                CheckBox:
                    size_hint: 0.1, 1
                    pos_hint: {'x': 0.2}
                    id: premultiplied
                Label:
                    size_hint: 0.7, 1
                    pos_hint: {'x': 0.3}
                    font_size: 16
                    text: "Premultiplied"
            Spinner:
                text: "Skins:"
                id: skins
                values: root.skins
                on_text: root.skinCurrent = self.text
            RelativeLayout:
                Label:
                    size_hint: 0.25, 1
                    font_size: 16
                    text: "Setup Pose:"
                Button:
                    size_hint: 0.25, 1
                    pos_hint: {'x': 0.25}
                    text: 'Bones'
                Button:
                    size_hint: 0.25, 1
                    pos_hint: {'x': 0.5}
                    text: 'Sltos'
                Button:
                    size_hint: 0.25, 1
                    pos_hint: {'x': 0.75}
                    text: 'Both'
            Spinner:
                text: "Animations:"
                id: animations
                values: root.animations
                on_text: root.animationCurrent = self.text
            RelativeLayout:        
                Label:
                    size_hint: 0.2, 1
                    font_size: 16
                    text: "Mix: "
                Label:
                    size_hint: 0.2, 1
                    pos_hint: {'x': 0.2}
                    font_size: 16
                    text: "" + str(round(mix.value, 2))
                Slider:
                    id: mix
                    min: 0
                    max: 1
                    size_hint: 0.6, 1
                    pos_hint: {'x': 0.4}
            RelativeLayout:     
                Label:
                    size_hint: 0.2, 1
                    font_size: 16
                    text: "Speed: "
                Label:
                    size_hint: 0.2, 1
                    pos_hint: {'x': 0.2}
                    font_size: 16
                    text: "" + str(round(speed.value, 2))
                Slider:
                    id: speed
                    min: 0.1
                    max: 10
                    value: 1
                    size_hint: 0.6, 1
                    pos_hint: {'x': 0.4}
            RelativeLayout:
                RelativeLayout:   
                    size_hint: 0.5, 1
                    Label:
                        size_hint: 0.5, 1
                        font_size: 16
                        text: "Playback:"
                    ToggleButton:
                        size_hint: 0.5, 1
                        pos_hint: {'x': 0.5}
                        id: pause
                        text: "Pause"
                RelativeLayout:
                    size_hint: 0.5, 1
                    pos_hint: {'x': 0.5}
                    CheckBox:
                        size_hint: 0.5, 1
                        id: loop
                        active: True
                    Label:
                        size_hint: 0.5, 1
                        pos_hint: {'x': 0.5}
                        font_size: 16
                        text: "Loop"
            RelativeLayout:
                Label:
                    size_hint: 0.2, 1
                    font_size: 16
                    text: "Percent: "
                Label:
                    size_hint: 0.2, 1
                    pos_hint: {'x': 0.2}
                    font_size: 16
                    text: "" + str(round(percentSlider.value, 2))
                Slider:
                    id: percentSlider
                    min: 0
                    max: 1
                    value: 0.0
                    size_hint: 0.6, 1
                    pos_hint: {'x': 0.4}
            RelativeLayout:
                Label:
                    size_hint: 0.2, 1
                    font_size: 16
                    text: "X Position"
                Label:
                    size_hint: 0.2, 1
                    pos_hint: {'x': 0.2}
                    font_size: 16
                    text: "" + str(round(xPos.value, 2))
                Slider:
                    id: xPos
                    value: 75.42
                    size_hint: 0.6, 1
                    pos_hint: {'x': 0.4}
            RelativeLayout:
                Label:
                    size_hint: 0.2, 1
                    font_size: 16
                    text: "Y Position"    
                Label:
                    size_hint: 0.2, 1
                    pos_hint: {'x': 0.2}
                    font_size: 16
                    text: "" + str(round(yPos.value, 2))
                Slider:
                    id: yPos
                    value: 39.83
                    size_hint: 0.6, 1
                    pos_hint: {'x': 0.4}    
"""

#         SpineDrawing:
#             pos: 1000, 500
#             size: 1000, 1000
# <CanvasDrawing>:
#     width: 950
#     pos: 300, 0
#     id: drawing

# class Skeleton(spine.Skeleton):
#     def __init__(self, skeletonData):
#         super(Skeleton, self).__init__(skeletonData=skeletonData)
#         self.x = 0
#         self.y = 0
#         self.texture = None
#         self.debug = False
#         self.pause = False
#         self.images = []
#         self.clock = None
#
#     def draw(self, canvas):
#         canvas.clear()
#         for slot in self.drawOrder:
#             if not slot.attachment:
#                 continue
#             slot.attachment.debugRegions = self.debugRegions
#             slot.attachment.skeletonX = self.x
#             slot.attachment.skeletonY = self.y
#             slot.attachment.draw(slot, canvas)
#
# class MeshAttachment(spine.MeshAttachment):
#     def __init__(self, mesh):
#         super(MeshAttachment, self).__init__()
# class SkinnedMeshAttachment(spine.SkinnedMeshAttachment):
#     def __init__(self, skinnedMesh):
#         super(SkinnedMeshAttachment, self).__init__()
# class BoundingBoxAttachment(spine.BoundingBoxAttachment):
#     def __init__(self, boundingBox):
#         super(BoundingBoxAttachment, self).__init__()
# class RegionAttachment(spine.RegionAttachment):
#     def __init__(self, region):
#         super(RegionAttachment, self).__init__()
#         self.texture = region.page.texture.get_region(region.x, region.y, region.width, region.height)
#         u, v = self.texture.uvpos
#         uw, vh = self.texture.uvsize
#         self.u = u
#         self.v = v
#         self.u2 = u + uw
#         self.v2 = v + vh
#         self.first_time = True
#         if region.rotate:
#             self._tex_coords = (
#                 self.u2,  # self.vertices[0].texCoords.x
#                 self.v2,  # self.vertices[0].texCoords.y
#                 self.u,  # self.vertices[1].texCoords.x
#                 self.v2,  # self.vertices[1].texCoords.y
#                 self.u,  # self.vertices[2].texCoords.x
#                 self.v,  # self.vertices[2].texCoords.y
#                 self.u2,  # self.vertices[3].texCoords.x
#                 self.v,  # self.vertices[3].texCoords.y
#             )
#         else:
#             self._tex_coords = (
#                 self.u,  # self.vertices[0].texCoords.x
#                 self.v2,  # self.vertices[0].texCoords.y
#                 self.u,  # self.vertices[1].texCoords.x
#                 self.v,  # self.vertices[1].texCoords.y
#                 self.u2,  # self.vertices[2].texCoords.x
#                 self.v,  # self.vertices[2].texCoords.y
#                 self.u2,  # self.vertices[3].texCoords.x
#                 self.v2  # self.vertices[3].texCoords.y
#             )
#
#     def prepare_graphics(self, canvas):
#         self._mesh_vertices = vertices = [0] * 16
#         vertices[2::4] = self._tex_coords[::2]
#         vertices[3::4] = self._tex_coords[1::2]
#         self.canvas = Canvas()
#         with self.canvas:
#             Color(1, 1, 1, 1)
#             # PushMatrix()
#             self.g_mesh = Mesh(vertices=vertices,
#                                indices=range(4),
#                                mode="triangle_fan",
#                                texture=self.texture)
#             self.g_debug_color = Color(1, 0, 0, 1)
#             self.g_debug_mesh = Mesh(vertices=vertices,
#                                      indices=range(4),
#                                      mode="line_loop", )
#             # Translate(x=200, y=200)
#             # PopMatrix()
#
#     def draw(self, slot, canvas):
#         if self.first_time:
#             self.first_time = False
#             self.prepare_graphics(canvas)
#
#         skeleton = slot.skeleton
#         canvas.add(self.canvas)
#
#         self.updateOffset()
#         self.updateWorldVertices(slot.bone)
#
#         # update graphics
#         self.g_mesh.vertices = self._mesh_vertices
#         # print(self.g_mesh.vertices)
#         if self.debugRegions:
#             self.g_debug_mesh.vertices = self._mesh_vertices
#             self.g_debug_color.a = 1
#         else:
#             self.g_debug_color.a = 0
#
#     def updateWorldVertices(self, bone):
#         x = bone.worldX + self.skeletonX
#         y = bone.worldY + self.skeletonY
#         m00 = bone.m00
#         m01 = bone.m01
#         m10 = bone.m10
#         m11 = bone.m11
#         offset = self.offset
#         v = self._mesh_vertices
#         v[0::4] = [
#             offset[0] * m00 + offset[1] * m01 + x,
#             offset[2] * m00 + offset[3] * m01 + x,
#             offset[4] * m00 + offset[5] * m01 + x,
#             offset[6] * m00 + offset[7] * m01 + x
#         ]
#         v[1::4] = [
#             offset[0] * m10 + offset[1] * m11 + y,
#             offset[2] * m10 + offset[3] * m11 + y,
#             offset[4] * m10 + offset[5] * m11 + y,
#             offset[6] * m10 + offset[7] * m11 + y]
# class AtlasAttachmentLoader(spine.AttachmentLoader.AttachmentLoader):
#     def __init__(self, atlas):
#         super(AtlasAttachmentLoader, self).__init__()
#         if atlas is None:
#             raise Exception("atlas cannot be None")
#         self.atlas = atlas
#
#     def newAttachment(self, tp, name):
#         if tp == spine.AttachmentLoader.AttachmentType.region:
#             region = self.atlas.findRegion(name)
#             if not region:
#                 raise Exception("atlas region not found: ", name)
#             return RegionAttachment(region)
#
#         elif tp == spine.AttachmentLoader.AttachmentType.mesh:
#             mesh = self.atlas.findRegion(name)
#             if not mesh:
#                 raise Exception("atlas region not found: ", name)
#             return MeshAttachment(name)
#         elif tp == spine.AttachmentLoader.AttachmentType.skinnedMesh:
#             skinnedMesh = self.atlas.findRegion(name)
#             if not skinnedMesh:
#                 raise Exception("atlas region not found: ", name)
#             return SkinnedMeshAttachment(name)
#         elif tp == spine.AttachmentLoader.AttachmentType.boundingBox:
#             boundingBox = self.atlas.findRegion(name)
#             if not boundingBox:
#                 raise Exception("atlas region not found: ", name)
#             return BoundingBoxAttachment(name)
#         else:
#             raise Exception('Unknown attachment type: ', type)
# class AtlasPage(spine.AtlasPage):
#     def __init__(self):
#         super(AtlasPage, self).__init__()
#         self.texture = None
# class AtlasRegion(spine.AtlasRegion):
#     def __init__(self):
#         super(AtlasRegion, self).__init__()
#         self.page = None
# class Atlas(spine.Atlas):
#     def __init__(self, filename):
#         self.atlas_dir = dirname(filename)
#         super(Atlas, self).__init__()
#         super(Atlas, self).loadWithFile(filename)
#
#     def newAtlasPage(self, name):
#         page = AtlasPage()
#         filename = realpath(join(self.atlas_dir, name))
#         if filename:
#             page.texture = Image(filename).texture
#             page.texture.flip_vertical()
#         return page
#
#     def newAtlasRegion(self, page):
#         region = AtlasRegion()
#         region.page = page
#         return region
#
#     def findRegion(self, name):
#         return super(Atlas, self).findRegion(name)


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

    def __init__(self, **kwargs):
        self.register_event_type('on_touch_hover')
        self.chooser = None
        self.popup = None

        self.skeletons = []
        self.states = []

        # self.batch = PolygonSpriteBatch()

        self.renderer = SkeletonRenderer()
        self.debugRenderer = SkeletonRendererDebug()

        self.draw_canvas = Canvas()

        super().__init__(**kwargs)
        self.canvas.add(self.draw_canvas)

    def on_touch_hover(self, touch):
        return False

    def on_skinCurrent(self, instance, value):
        if self.skinCurrent != "Skin:":
            for skeleton in self.skeletons:
                skeleton.setSkin(self.skinCurrent)
                skeleton.setSlotsToSetupPose()

    def on_animationCurrent(self, instance, value):
        if self.animationCurrent != "animation:":
            for state in self.states:
                state.setAnimation(0, self.animationCurrent, self.loop)

    def on_setup_pose_both(self, *args):
        if self.skeleton is not None:
            self.skeleton.setToSetupPose()

    def on_setup_pose_bones(self, *args):
        if self.skeleton is not None:
            self.skeleton.setBonesToSetupPose()

    def on_setup_pose_slots(self, *args):
        if self.skeleton is not None:
            self.skeleton.setSlotsToSetupPose()

    def on_scale(self, *args):
        Clock.unschedule(self.set_scale)
        Clock.schedule_once(self.set_scale)

    def set_scale(self, *args):
        if len(self.skeletons) > 0:
            self.load_skeleton()

    def on_mix(self, *args):
        for state in self.states:
            state.getData().setDefaultMix(self.mix)

    def open_skeleton(self, *args):
        print("open new skeleton")
        self.chooser = FileChooserListViewBase(path="C:/Users/ethan/OneDrive/Desktop/danmachi assets/danmachi chars/gac_1011002023", filters=['*.skel'])
        #
        self.popup = PopupBase(title='Test popup', content=self.chooser, auto_dismiss=False)
        self.chooser.add_widget(Button(text="Cancel", on_release=self.cancel_skeleton, size_hint=(None, None)))
        self.chooser.add_widget(Button(text="Select", pos=(self.chooser.width, 0), size_hint=(None, None), on_release=self.load_skeleton))
        self.popup.open()

    def cancel_skeleton(self, *args):
        self.popup.dismiss()

    def load_skeleton(self, *args):
        if self.popup is not None:
            self.popup.dismiss()
        if self.chooser is None:
            return
        if len(self.chooser.selection) != 1:
            return
        name = str(self.chooser.selection[0].rsplit("\\", 1)[1][:-5])
        print(name)

        filepath = self.chooser.selection[0].replace('\\', '/')
        skele_loader = SkeletonLoader()
        self.skeletons = []
        self.skeletons.append(skele_loader.load_skeleton(filepath, False, self.scale))
        self.skeletons.append(skele_loader.load_skeleton("C:/Users/ethan/OneDrive/Desktop/danmachi assets/danmachi chars/gac_1011004010/1041004010.skel", False, self.scale))
        self.skeletons.append(skele_loader.load_skeleton("C:/Users/ethan/OneDrive/Desktop/danmachi assets/danmachi chars/gac_1011006009/1041006009.skel", False, self.scale))
        self.skeletons.append(skele_loader.load_skeleton("C:/Users/ethan/OneDrive/Desktop/danmachi assets/danmachi chars/gac_1011018009/1041018009.skel", False, self.scale))
        self.skeletons.append(skele_loader.load_skeleton("C:/Users/ethan/OneDrive/Desktop/danmachi assets/danmachi chars/gac_1011041004/1041041004.skel", False, self.scale))
        self.skeletons.append(skele_loader.load_skeleton("C:/Users/ethan/OneDrive/Desktop/danmachi assets/danmachi chars/gac_1011043003/1041043003.skel", False, self.scale))
        self.skeletons.append(skele_loader.load_skeleton("C:/Users/ethan/OneDrive/Desktop/danmachi assets/danmachi chars/gac_1011091003/1041091003.skel", False, self.scale))
        self.skeletons.append(skele_loader.load_skeleton("C:/Users/ethan/OneDrive/Desktop/danmachi assets/danmachi chars/gac_1011092003/1041092003.skel", False, self.scale))
        self.states = []
        self.states.append(AnimationState(AnimationStateData(self.skeletons[0].getData())))
        self.states.append(AnimationState(AnimationStateData(self.skeletons[1].getData())))
        self.states.append(AnimationState(AnimationStateData(self.skeletons[2].getData())))
        self.states.append(AnimationState(AnimationStateData(self.skeletons[3].getData())))
        self.states.append(AnimationState(AnimationStateData(self.skeletons[4].getData())))
        self.states.append(AnimationState(AnimationStateData(self.skeletons[5].getData())))
        self.states.append(AnimationState(AnimationStateData(self.skeletons[6].getData())))
        self.states.append(AnimationState(AnimationStateData(self.skeletons[7].getData())))
        items = []
        for skin in self.skeletons[0].getData().getSkins():
            items.append(skin.getName())
        self.ids.skins.values = items
        self.ids.skins.text = items[0]

        items = []
        for animation in self.skeletons[0].getData().getAnimations():
            items.append(animation.getName())
        self.ids.animations.values = items
        self.ids.animations.text = items[0]

        self.skeletons[0].setSkin(self.ids.skins.text)
        for skeleton in self.skeletons[1:]:
            skeleton.setSkin(skeleton.getData().getSkins()[0].getName())
        self.states[0].setAnimation(0, self.ids.animations.text, True)
        for state, skeleton in zip(self.states[1:], self.skeletons[1:]):
            state.setAnimation(0, skeleton.getData().getAnimations()[0].getName(), True)
        print("Finished loading skeleton!")
        Clock.schedule_interval(self.render, 1 / 144)

    def render(self, delta):
        if len(self.skeletons) > 0:
            self.draw_canvas.clear()
            for state in self.states:
                state.getData().setDefaultMix(self.mix)
            self.renderer.setPremultipliedAlpha(self.alphaP)

            delta = min(delta, 0.032) * self.speed
            for skeleton in self.skeletons:
                skeleton.update(delta)
                skeleton.setFlip(self.flipX, self.flipY)
            if not self.pause:
                for state, skeleton in zip(self.states, self.skeletons):
                    state.update(delta)
                    state.apply(skeleton)
            self.skeletons[0].setPosition(self.skeletonX, self.skeletonY)
            self.skeletons[1].setPosition(self.skeletonX + 300, self.skeletonY)
            self.skeletons[2].setPosition(self.skeletonX + 600, self.skeletonY)
            self.skeletons[3].setPosition(self.skeletonX + 150, self.skeletonY - 75)
            self.skeletons[4].setPosition(self.skeletonX + 450, self.skeletonY - 75)
            self.skeletons[5].setPosition(self.skeletonX + 75, self.skeletonY - 150)
            self.skeletons[6].setPosition(self.skeletonX + 375, self.skeletonY - 150)
            self.skeletons[7].setPosition(self.skeletonX + 675, self.skeletonY - 150)

            for skeleton in self.skeletons:
                skeleton.updateWorldTransform()
                self.renderer.draw(self.draw_canvas, skeleton)

            entry = self.states[0].getCurrent(0)
            if entry is not None:
                self.percent = entry.getTime() / entry.getEndTime()
                if entry.getLoop():
                    self.percent %= 1


class SpineApp(App):
    title = "Skeleton Viewer"

    def build(self):
        Window.size = (1250, 800)
        self.width, self.height = 1250, 800
        from kivy.lang import Builder
        return Builder.load_string(kv)

    def on_touch_hover(self, touch):
        return False


if __name__ == "__main__":
    SpineApp().run()


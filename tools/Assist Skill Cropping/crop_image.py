from PIL import Image
import os
from os import listdir, remove
from comtypes.client import CreateObject
from time import sleep
from sys import argv
import win32com.client

if len(argv) == 1:
    print('No label text passed!')
    quit(1)

label_text = argv[1]


class PhotoshopHandler:
    def __init__(self, ps_app):
        self._horizontal = ps_app.CharIDToTypeID("Hrzn") # Horizontal
        self._vertical = ps_app.CharIDToTypeID("Vrtc") # Vertical
        self._fromPoint = ps_app.CharIDToTypeID('From') # From
        self._toPoint = ps_app.CharIDToTypeID("T   ")    # To
        self._pixel = ps_app.CharIDToTypeID("#Pxl")  # Pixel Coordinates
        self._point = ps_app.CharIDToTypeID("Pnt ")  # Point
        self._gradientTemplate = ps_app.CharIDToTypeID("Grad") # Gradient
        self._type = ps_app.CharIDToTypeID("Type") # Type
        self._gradientType = ps_app.CharIDToTypeID("GrdT") # Gradient Type
        self._linear = ps_app.CharIDToTypeID("Lnr ")  # Linear
        self._dither = ps_app.CharIDToTypeID("Dthr") # Dithering
        self._useMultisampling = ps_app.CharIDToTypeID("UsMs") # Transparency
        self._name = ps_app.CharIDToTypeID("Nm  ")   # Name
        self._gradient_filter = ps_app.CharIDToTypeID("GrdF")
        self._cstS = ps_app.CharIDToTypeID("CstS")
        self._intersect = ps_app.CharIDToTypeID("Intr") # Intersect
        self._colorList = ps_app.CharIDToTypeID("Clrs") # Color list
        self._color = ps_app.CharIDToTypeID("Clr ") # Color
        self._red = ps_app.CharIDToTypeID("Rd  ")  # Red
        self._green = ps_app.CharIDToTypeID("Grn ") # Green
        self._blue = ps_app.CharIDToTypeID("Bl  ")  # Blue
        self._RGBC = ps_app.CharIDToTypeID("RGBC") # RGB Color
        self._color_y = ps_app.CharIDToTypeID("Clry")
        self._userSet = ps_app.CharIDToTypeID("UsrS")
        self._location = ps_app.CharIDToTypeID("Lctn") # Location
        self._midpoint = ps_app.CharIDToTypeID("Mdpn") # Midpoint
        self._color_transform = ps_app.CharIDToTypeID("Clrt")
        self._transparency = ps_app.CharIDToTypeID("Trns")  # Transparency
        self._opacity = ps_app.CharIDToTypeID("Opct")  # Opacity
        self._protected = ps_app.CharIDToTypeID("#Prc")
        self._opacity_transform = ps_app.CharIDToTypeID("TrnS")  #
        self._gradient = ps_app.CharIDToTypeID("Grdn")  # Gradient Color

        # For use in Hue Color
        self._angle = ps_app.CharIDToTypeID("#Ang")
        self._hue = ps_app.CharIDToTypeID("H   ")
        self._strength = ps_app.CharIDToTypeID("Strt")
        self._brightness = ps_app.CharIDToTypeID("Brgh")
        self._HSBC = ps_app.CharIDToTypeID("HSBC")

        self._magicWandTool = ps_app.StringIDToTypeID("magicWandTool")
        self._gradientTool = ps_app.CharIDToTypeID("GrTl") # Gradient Tool

        self._dontRecord = ps_app.StringIDToTypeID("dontRecord")
        self._forceNotify = ps_app.StringIDToTypeID("forceNotify")

        self._selectTool = ps_app.CharIDToTypeID("slct") # Select
        self._null = ps_app.CharIDToTypeID("null") # Null
        self._selection = ps_app.CharIDToTypeID("setd") # Set
        self._channel = ps_app.CharIDToTypeID("Chnl") # Channel
        self._focus_selection = ps_app.CharIDToTypeID("fsel") # Force Selection
        self._tolerance = ps_app.CharIDToTypeID("Tlrn") # Tolerance
        self._antiAliasing = ps_app.CharIDToTypeID("AntA") # Anti-Aliasing
        self._contiguous = ps_app.CharIDToTypeID("Cntg")

        self.magic_wand = CreateObject("Photoshop.ActionReference", dynamic=True)
        self.magic_wand.PutClass(self._magicWandTool)

        self.gradient_tool = CreateObject("Photoshop.ActionReference", dynamic=True)
        self.gradient_tool.PutClass(self._gradientTool)

    def select_tool(self, tool_reference):
        select_tool = CreateObject("Photoshop.ActionDescriptor", dynamic=True)
        select_tool.PutReference(self._null, tool_reference)
        select_tool.PutBoolean(self._dontRecord, True)
        select_tool.PutBoolean(self._forceNotify, True)
        ps_app.ExecuteAction(self._selectTool, select_tool, 3)

    def wand_select_point(self, x, y):
        self.select_tool(self.magic_wand)
        set_selection = CreateObject("Photoshop.ActionDescriptor", dynamic=True)
        channel = CreateObject("Photoshop.ActionReference", dynamic=True)
        channel.PutProperty(self._channel, self._focus_selection)
        set_selection.PutReference(self._null, channel)
        set_selection.PutObject(self._toPoint, self._point, self.create_point(x, y))
        set_selection.PutInteger(self._tolerance, 0)
        set_selection.PutBoolean(self._antiAliasing, True)
        set_selection.PutBoolean(self._contiguous, False)
        ps_app.ExecuteAction(self._selection, set_selection, 3)

    def create_point(self, x, y):
        point = CreateObject("Photoshop.ActionDescriptor", dynamic=True)
        point.PutUnitDouble(self._horizontal, self._pixel, x)
        point.PutUnitDouble(self._vertical, self._pixel, y)
        return point

    def create_color(self, r, g, b):
        color = CreateObject("Photoshop.ActionDescriptor", dynamic=True)
        color.PutDouble(self._red, r)
        color.PutDouble(self._green, g)
        color.PutDouble(self._blue, b)
        return color

    def create_color_list(self, colors):
        color_list = CreateObject("Photoshop.ActionList", dynamic=True)

        for index, (r, g, b) in enumerate(colors):
            gradient_color = CreateObject("Photoshop.ActionDescriptor", dynamic=True)
            gradient_color.PutObject(self._color, self._RGBC, self.create_color(r, g, b))
            gradient_color.PutEnumerated(self._type, self._color_y, self._userSet)
            gradient_color.PutInteger(self._location, int(index / len(colors) * 4096))
            gradient_color.PutInteger(self._midpoint, 50)
            color_list.PutObject(self._color_transform, gradient_color)
        return color_list

    def create_opacity_list(self, opacities):
        opacity_list = CreateObject("Photoshop.ActionList", dynamic=True)

        for index, opacity in enumerate(opacities):
            transform_location = CreateObject("Photoshop.ActionDescriptor", dynamic=True)
            transform_location.PutUnitDouble(self._opacity, self._protected, opacity)
            transform_location.PutInteger(self._location, int(index / len(opacities) * 4096))
            transform_location.PutInteger(self._midpoint, 50)
            opacity_list.PutObject(self._opacity_transform, transform_location)
        return opacity_list

    def create_gradient_template(self, name, colors, opacities):
        gradient_template = CreateObject("Photoshop.ActionDescriptor", dynamic=True)
        gradient_template.PutString(self._name, name)
        gradient_template.PutEnumerated(self._gradient_filter, self._gradient_filter, self._cstS)
        gradient_template.PutDouble(self._intersect, 4096.0)

        gradient_template.PutList(self._colorList, self.create_color_list(colors))
        gradient_template.PutList(self._transparency, self.create_opacity_list(opacities))
        return gradient_template

    def create_gradient(self, gradient_template, start_point, end_point, dither=True):
        gradient = CreateObject("Photoshop.ActionDescriptor", dynamic=True)

        gradient.PutObject(self._fromPoint, self._point, self.create_point(*start_point))
        gradient.PutObject(self._toPoint, self._point, self.create_point(*end_point))

        gradient.PutEnumerated(self._type, self._gradientType, self._linear)
        gradient.PutBoolean(self._dither, dither)
        gradient.PutBoolean(self._useMultisampling, False)

        gradient.PutObject(self._gradientTemplate, self._gradient, gradient_template)
        ps_app.ExecuteAction(self._gradient, gradient, 3)


bronze_colors  = [(255, 255, 199), (194, 126,  60)]
silver_colors  = [(238, 255, 255), (115, 120, 167)]
golden_colors  = [(255, 254, 155), (179, 122,  30)]
rainbow_colors = [(255, 174, 255), (153, 251, 255), (161, 240, 157), (255, 255, 161), (227, 166, 175)]
opacities = [100, 100]
letter_widths = {'D': 35, 'C': 35, 'B': 35, 'A': 35, 'S': 35, 'SS': 55, 'SSS': 80}

# Create all the images
ps_app = CreateObject('Photoshop.Application', dynamic=True)
ps_app.visible = True
ps_app.Open(f'{os.getcwd()}/assist_label.psd')
ps_app.displayDialogs = 3
photoshop_handler = PhotoshopHandler(ps_app)

text_layer = None
gradient_layer = None
for layer in ps_app.ActiveDocument.ArtLayers:
    if layer.Name == "Gradient Layer":
        gradient_layer = layer
    else:
        text_layer = layer
text_object = text_layer.TextItem
for level in ['D', 'C', 'B', 'A', 'S', 'SS', 'SSS']:
    width = letter_widths[level]
    text_object.contents = f'{label_text} {level}'
    gradient_layer.Clear()

    if level != 'D':
        # Select the end layer
        ps_app.ActiveDocument.activeLayer = text_layer
        photoshop_handler.select_tool(photoshop_handler.magic_wand)
        photoshop_handler.wand_select_point(0, 0)
        ps_app.ActiveDocument.Selection.Invert()
        left, bottom, right, top = ps_app.ActiveDocument.Selection.Bounds
        ps_app.ActiveDocument.Selection.Select([[right - width, bottom], [right - width, top], [right, top], [right, bottom]], 4)

        # Create the gradient
        ps_app.ActiveDocument.activeLayer = gradient_layer

        center = left + int((right - left) / 2)
        if level == 'C':
            bronze = photoshop_handler.create_gradient_template("Bronze", bronze_colors, opacities)
            photoshop_handler.create_gradient(bronze, (center, top), (center, bottom))
        elif level == 'B':
            silver = photoshop_handler.create_gradient_template("Silver", silver_colors, opacities)
            photoshop_handler.create_gradient(silver, (center, top), (center, bottom))
        elif level == 'A':
            golden = photoshop_handler.create_gradient_template("Golden", golden_colors, opacities)
            photoshop_handler.create_gradient(golden, (center, top), (center, bottom))
        else:
            rainbow = photoshop_handler.create_gradient_template("Rainbow", rainbow_colors, opacities)
            photoshop_handler.create_gradient(rainbow, (center, top), (center, bottom))

    # Save a copy
    ps_app.ActiveDocument.SaveAs(f'{os.getcwd()}/Labels/{label_text} {level}')
ps_app.ActiveDocument.Save()
ps_app.ActiveDocument.Close()

# Open the images and export them
ps_app = win32com.client.Dispatch("Photoshop.Application")
options = win32com.client.Dispatch('Photoshop.ExportOptionsSaveForWeb')
options.Format = 13
options.PNG8 = False
options.Quality = 100
for level in ['D', 'C', 'B', 'A', 'S', 'SS', 'SSS']:
    # Open in win32 and save
    ps_app.Open(f'{os.getcwd()}/Labels/{label_text} {level}.psd')
    export = f'{os.getcwd()}/Labels/{label_text} {level}.png'
    ps_app.Application.ActiveDocument.Export(ExportIn=export, ExportAs=2, Options=options)
    ps_app.Application.ActiveDocument.Save()
    ps_app.Application.ActiveDocument.Close()
    remove(f'{os.getcwd()}/Labels/{label_text} {level}.psd')

# Crop all the images
for level in ['D', 'C', 'B', 'A', 'S', 'SS', 'SSS']:
    def get_image_bounds(image):
        pixels = image.load()
        width, height = image.size
        left, bottom, right, top = width, height, 0, 0
        for x in range(width):
            for y in range(height):
                (r, g, b, a) = pixels[x, y]
                if a != 0:
                    top = max(y + 1, top)
                    bottom = min(y, bottom)
                    left = min(x, left)
                    right = max(x + 1, right)
        return left, bottom, right, top


    # Load image into PIL
    image = Image.open(f'Labels/{label_text} {level}.png'.replace(' ', '-'))
    left, bottom, right, top = get_image_bounds(image)

    cropped_image = image.crop((left, bottom, right, top))
    width = int((right - left) * (42 / (top - bottom)))
    small_image = cropped_image.resize((width, 42), Image.LANCZOS)
    result = Image.new(small_image.mode, (512, 42), (0, 0, 0, 0))
    result.paste(small_image, (int((512 - width) / 2), 0))
    background = Image.open(f'Background.png')
    background.paste(result, (0, 22))
    background.save(f'Output/{label_text} {level}.png')

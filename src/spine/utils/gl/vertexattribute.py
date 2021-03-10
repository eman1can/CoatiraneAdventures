import struct

from kivy.app import App
from kivy.graphics.opengl import GL_UNSIGNED_BYTE, GL_FLOAT, GL_UNSIGNED_SHORT, GL_SHORT, GL_BYTE, glCreateShader, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glShaderSource, glGetShaderiv, glCompileShader, GL_COMPILE_STATUS, glGetShaderInfoLog, glCreateProgram, glAttachShader, glLinkProgram, glGetProgramiv, GL_LINK_STATUS, glGetProgramInfoLog, \
    glGetAttribLocation, glGetUniformLocation, glUseProgram, glDeleteShader, glDeleteProgram, GL_ACTIVE_UNIFORMS, glGetActiveUniform, GL_ACTIVE_ATTRIBUTES, glGetActiveAttrib, glUniformMatrix4fv, glUniform1i


class Usage:
    Position = 1
    ColorUnpacked = 2
    ColorPacked = 4
    Normal = 8
    TextureCoordinates = 16
    Generic = 32
    BoneWeight = 64
    Tangent = 128
    BiNormal = 256


class ShaderProgram:
    POSITION_ATTRIBUTE = "a_position"
    NORMAL_ATTRIBUTE = "a_normal"
    COLOR_ATTRIBUTE = "a_color"
    TEXCOORD_ATTRIBUTE = "a_texCoord"
    TANGENT_ATTRIBUTE = "a_tangent"
    BINORMAL_ATTRIBUTE = "a_binormal"
    BONEWEIGHT_ATTRIBUTE = "a_boneWeight"

    pedantic = True
    prependVertexCode = ""
    prependFragmentCode = ""
    shaders = {}

    def __init__(self, vertexShader, fragmentShader):
        self.log = ""
        self.compiled = False
        self.uniforms = {}
        self.uniformTypes = {}
        self.uniformSizes = {}
        self.uniformNames = []
        self.attributes = {}
        self.attributeTypes = {}
        self.attributesSizes = {}
        self.attributeNames = []
        self.program = 0
        self.vertexShaderHandle = 0
        self.fragmentShaderHandle = 0
        self.matrix = None
        self.vertexShaderSource = None
        self.fragmentShaderSource = None
        self.invalidated = False
        self.refCount = 0

        if vertexShader is None:
            raise Exception("vertexShader must not be None")
        if fragmentShader is None:
            raise Exception("vertexShader must not be None")

        if self.prependVertexCode is not None and len(self.prependVertexCode) > 0:
            vertexShader = self.prependVertexCode + vertexShader
        if self.prependFragmentCode is not None and len(self.prependFragmentCode) > 0:
            fragmentShader = self.prependFragmentCode + fragmentShader

        self.vertexShaderSource = vertexShader
        self.fragmentShaderSource = fragmentShader
        self.matrix = [0.0 for x in range(16)]

        self.compileShaders(vertexShader, fragmentShader)
        if self.isCompiled():
            self.fetchAttributes()
            self.fetchUniforms()
            self.addManagedShader(App.get_running_app(), self)

    def compileShaders(self, vertexShader, fragmentShader):
        self.vertexShaderHandle = self.loadShader(GL_VERTEX_SHADER, vertexShader)
        self.fragmentShaderHandle = self.loadShader(GL_FRAGMENT_SHADER, fragmentShader)

        if self.vertexShaderHandle == -1 or self.fragmentShaderHandle == -1:
            self.compiled = False
            return

        self.program = self.linkProgram(self.createProgram())
        if self.program == -1:
            self.compiled = False
            return

        self.compiled = True

    def loadShader(self, type, source):
        shader = glCreateShader(type)
        if shader == 0:
            return -1

        glShaderSource(shader, bytes(source, 'utf-8'))
        glCompileShader(shader)
        compiled = glGetShaderiv(shader, GL_COMPILE_STATUS)

        if compiled == 0:
            infoLog = glGetShaderInfoLog(shader, 64)
            self.log += "Vertex Shader:\n" if type == GL_VERTEX_SHADER else "Fragment shader:\n"
            self.log += str(infoLog)
            return -1
        return shader

    def createProgram(self):
        program = glCreateProgram()
        return program if program != 0 else -1

    def linkProgram(self, program):
        if program == -1:
            return -1

        glAttachShader(program, self.vertexShaderHandle)
        glAttachShader(program, self.fragmentShaderHandle)
        glLinkProgram(program)

        linked = glGetProgramiv(program, GL_LINK_STATUS)
        if linked == 0:
            self.log = glGetProgramInfoLog(program, 64)
            return -1
        return program

    def getLog(self):
        if self.isCompiled:
            self.log = glGetProgramInfoLog(self.program, 64)
        return self.log

    def isCompiled(self):
        return self.isCompiled

    def fetchAttributeLocation(self, name):
        location = self.attributes[name]
        if location is None:
            location = glGetAttribLocation(self.program, name)
            self.attributes[name] = location
        return location

    def fetchUniformLocation(self, *args):
        if len(args) == 1:
            return self.fetchUniformLocation(args[0], self.pedantic)
        else:
            if args[0] not in self.uniforms:
                location = glGetUniformLocation(self.program, bytes(args[0], 'utf-8'))
                if location == -1 and args[1]:
                    raise Exception(f"no uniform with name {args[0]} in shader")
                self.uniforms[args[0]] = location
            else:
                location = self.uniforms[args[0]]
            return location

    def begin(self):
        self.checkManaged()
        glUseProgram(self.program)

    def end(self):
        glUseProgram(0)

    def dispose(self):
        glUseProgram(0)
        glDeleteShader(self.vertexShaderHandle)
        glDeleteShader(self.fragmentShaderHandle)
        glDeleteProgram(self.program)
        if self.shaders[App.get_running_app()] is not None:
            self.shaders[App.get_running_app()] = None

    def checkManaged(self):
        if self.invalidated:
            self.compileShaders(self.vertexShaderSource, self.fragmentShaderSource)
            self.invalidated = False

    def addManagedShader(self, app, shaderProgram):
        if app not in self.shaders:
            managedResources = []
        else:
            managedResources = self.shaders[app]
        managedResources.append(shaderProgram)
        self.shaders[app] = managedResources

    def fetchUniforms(self):
        numUniforms = glGetProgramiv(self.program, GL_ACTIVE_UNIFORMS)

        self.uniformNames = []

        for i in range(numUniforms):
            name, params, type = glGetActiveUniform(self.program, i)
            location = glGetUniformLocation(self.program, name)
            self.uniforms[name] = location
            self.uniformTypes[name] = type
            self.uniformSizes[name] = params
            self.uniformNames.append(name)

    def fetchAttributes(self):
        numAttributes = glGetProgramiv(self.program, GL_ACTIVE_ATTRIBUTES)

        self.attributeNames = []

        for i in range(numAttributes):
            name, type, params = glGetActiveAttrib(self.program, i)
            location = glGetAttribLocation(self.program, name)
            self.attributes[name] = location
            self.attributeTypes[name] = type
            self.attributesSizes[name] = params
            self.attributeNames.append(name)

    def setUniformMatrix(self, name, matrix, transpose=False):
        location = self.fetchUniformLocation(name)
        self.checkManaged()
        b = b''
        for val in matrix.val:
            b += bytes(struct.unpack('<I', struct.pack('<f', val))[0])
        glUniformMatrix4fv(location, 1, transpose, b)

    def setUniform(self, name, value):
        self.checkManaged()
        location = self.fetchUniformLocation(name)
        glUniform1i(location, value)

class VertexAttribute:
    def __init__(self, *args):
        self.usage = 0
        self.numComponents = 0
        self.normalized = False
        self.type = 0
        self.offset = 0
        self.alias = None
        self.unit = 0
        self.usageIndex = 0

        if len(args) == 3:
            usage, numComponents, type, normalized, alias, unit = args[0], args[1], GL_UNSIGNED_BYTE if args[0] == Usage.ColorPacked else GL_FLOAT, args[0] == Usage.ColorPacked, args[2], 0
        elif len(args) == 4:
            usage, numComponents, type, normalized, alias, unit = args[0], args[1], GL_UNSIGNED_BYTE if args[0] == Usage.ColorPacked else GL_FLOAT, args[0] == Usage.ColorPacked, args[2], args[3]
        elif len(args) == 5:
            usage, numComponents, type, normalized, alias, unit = args[0], args[1], args[2], args[3], args[4], 0
        else:
            usage, numComponents, type, normalized, alias, unit = args[0], args[1], args[2], args[3], args[4], args[5]
        self.usage = usage
        self.numComponents = numComponents
        self.type = type
        self.normalized = normalized
        self.alias = alias
        self.unit = unit
        self.usageIndex = len(str(usage)) - len(str(usage).rstrip('0'))

    def __eq__(self, other):
        if not isinstance(other, VertexAttribute) or other is None:
            return False
        if not self.usage == other.usage:
            return False
        if not self.numComponents == other.numComponents:
            return False
        if not self.type == other.type:
            return False
        if not self.normalized == other.normalized:
            return False
        if not self.alias == other.alias:
            return False
        if not self.unit == other.unit:
            return False

    def getKey(self):
        return (self.usageIndex << 8) + (self.unit & 0xFF)

    def getSizeInBytes(self):
        if self.type == GL_FLOAT:
            return 4 * self.numComponents
        if self.type == GL_UNSIGNED_BYTE or self.type == GL_BYTE:
            return self.numComponents
        if self.type == GL_UNSIGNED_SHORT or self.type == GL_SHORT:
            return 2 * self.numComponents
        return 0

    def __hash__(self):
        result = self.getKey()
        result = 541 * result + self.numComponents
        result = 541 * result + hash(self.alias)
        return result


class VertexAttributes:
    def __init__(self, *attributes):
        self.attributes = None
        self.vertexSize = 0
        self.mask = -1

        if len(attributes) == 0:
            raise Exception("attributes must be >= 1")

        self.attributes = [attribute for attribute in attributes]
        self.vertexSize = self.calculateOffsets()

    def calculateOffsets(self):
        count = 0
        for attribute in self.attributes:
            attribute.offset = count
            count += attribute.getSizeInBytes()
        return count

    def __len__(self):
        return len(self.attributes)


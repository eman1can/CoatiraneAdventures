from enum import Enum

from kivy.app import App
from kivy.graphics.opengl import glDrawArrays, glDrawElements, GL_UNSIGNED_SHORT

from src.spine.utils.gl.disposable import Disposable
from src.spine.utils.gl.indexarray import IndexArray
from src.spine.utils.gl.vertexarray import VertexArray


class Mesh(Disposable):
    class VertexDataType(Enum):
        VertexArray = 0
        VertexBufferObject = 1
        VertexBufferObjectSubData = 2
        VertexBufferObjectWithVAO = 3

    def __init__(self, type, isStatic, maxVertices, maxIndices, *attributes):
        self.meshes = {}

        self.vertices = None
        self.indices = None
        self.autoBind = True
        self.isVertexArray = False

        self.instances = None
        self.isInstanced = False

        if type == self.VertexDataType.VertexBufferObject:
            self.vertices = VertexBufferObject(isStatic, maxVertices, *attributes)
            self.indices = IndexBufferObject(isStatic, maxIndices)
            self.isVertexArray = False
        elif type == self.VertexDataType.VertexBufferObjectSubData:
            self.vertices = VertexBufferObjectSubData(isStatic, maxVertices, *attributes)
            self.indices = IndexBufferObjectSubData(isStatic, maxIndices)
            self.isVertexArray = False
        elif type == self.VertexDataType.VertexBufferObjectWithVAO:
            self.vertices = VertexBufferObjectWithVAO(isStatic, maxVertices, *attributes)
            self.indices = IndexBufferObjectWithVAO(isStatic, maxIndices)
            self.isVertexArray = False
        else:
            self.vertices = VertexArray(maxVertices, *attributes)
            self.indices = IndexArray(maxIndices)
            self.isVertexArray = True

        self.addManagedMesh(App.get_running_app(), self)

    def addManagedMesh(self, app, mesh):
        managedResources = self.meshes.get(app)
        if managedResources is None:
            managedResources = []
        managedResources.append(mesh)
        self.meshes[app] = managedResources

    def setVertices(self, vertices, offset, count):
        self.vertices.setVertices(vertices, offset, count)
        return self

    def setIndices(self, indices, offset, count):
        self.indices.setIndices(indices, offset, count)
        return self

    def bind(self, shader, locations=None):
        self.vertices.bind(shader, locations)
        if self.instances is not None and self.instances.getNumUnstances() > 0:
            self.instances.bind(shader, locations)
        if self.indices.getNumIndicies() > 0:
            self.indices.bind()

    def unbind(self, shader, locations=None):
        self.vertices.unbind(shader, locations)
        self.vertices.unbind(shader, locations)
        if self.instances is not None and self.instances.getNumUnstances() > 0:
            self.instances.unbind(shader, locations)
        if self.indices.getNumIndicies() > 0:
            self.indices.unbind()

    def render(self, shader, primitiveType, offset, count, *args):
        if len(args) == 0:
            autoBind = self.autoBind
        else:
            autoBind = args[0]

        if count == 0:
            return

        if autoBind:
            self.bind(shader)

        if self.isVertexArray:
            if self.indices.getNumIndicies() > 0:
                buffer = self.indices.getBuffer()
                oldPosition = buffer.position()
                oldLimit = buffer.limit()
                buffer.position(offset)
                buffer.limit(offset + count)
                glDrawElements(primitiveType, count, GL_UNSIGNED_SHORT, buffer)
                buffer.position(oldPosition)
                buffer.limit(oldLimit)
            else:
                glDrawArrays(primitiveType, offset, count)
        else:
            raise Exception("Not Implemented!")

        if autoBind:
            self.unbind(shader)

    def dispose(self):
        if self.meshes.get(App.get_running_app()) is not None:
            self.meshes.get(App.get_running_app()).removeValue(self, True)
            self.vertices.dispose()
            if self.instances is not None:
                self.instances.dispose()
            self.indices.dispose()

class BitmapClip(Bitmap):
    depth = 0
    visible = False
    name = None
    width = 0.0
    height = 0.0
    regX = 0.0
    regY = 0.0
    x = 0.0
    y = 0.0
    scaleX = 0.0
    scaleY = 0.0
    rotation = 0.0
    alpha = 0.0
    offsetX = 0.0
    offsetY = 0.0
    originalWidth = 0.0
    originalHeight = 0.0

    _scaleX = 0.0
    _scaleY = 0.0
    _rotation = 0.0
    _cos = 0.0
    _sin = 0.0
    _matrix = 0.0

    def __init__(self, lwf, parent, objId):
        super().__init__(lwf, parent, objId)
        data = lwf.data.bitmaps[objId]
        fragment = lwf.data.textureFragments[data.textureFragmentId]
        texdata = lwf.data.textures[fragment.textureId]

        self.width = fragment.w / texdata.scale
        self.height = fragment.h / texdata.scale
        self.offsetX = fragment.x
        self.offsetY = fragment.y
        self.originalWidth = fragment.ow
        self.originalHeight = fragment.oh

        self.depth = -1
        self.visible = True

        self.regX = 0
        self.regY = 0
        self.x = 0
        self.y = 0
        self.scaleX = 0
        self.scaleY = 0
        self.rotation = 0
        self.alpha = 1

        self._scaleX = self.scaleX
        self._scaleY = self.scaleY
        self._rotation = self.rotation
        self._cos = 1
        self._sin = 0

        self._matrix = Matrix()

    def Exec(self, matrixId=0, colorTransformId=0):
        pass

    def Update(self, m, c):
        dirty = False
        if self.rotation is not self._rotation:
            self._rotation = self.rotation
            radian = self._rotation * math.pi / 180.0
            self._cos = math.cos(radian)
            self._sin = math.sin(radian)
            dirty = True
        if dirty or self._scaleX is not self.scaleX or self._scaleY is not self.scaleY:
            self._scaleX = self.scaleX
            self._scaleY = self.scaleY
            self._matrix.scaleX = self._scaleX * self._cos
            self._matrix.skew1 = self.scaleX * self._sin
            self._matrix.skew0 = self.scaleY * -self._sin
            self._matrix.scaleY = self.scaleY * self._cos
        self._matrix.translateX = self.x - self.regX
        self._matrix.translateY = self.y - self.regY

        self.m_matrix.scaleX = m.scaleX * self._matrix.scaleX + m.skew0 * self._matrix.skew1
        self.m_matrix.skew0 = m.scaleX * self._matrix.skew0 + m.skew0 * self._matrix.scaleY
        self.m_matrix.translateX = m.scaleX * self.x + m.skew0 * self.y + m.translateX + \
           m.scaleX * self.regX + m.skew0 * self.regY + \
           self.m_matrix.scaleX * -self.regX + self.m_matrix.skew0 * -self.regY

        self.m_matrix.skew1 = m.skew1 * self._matrix.scaleX + m.scaleY * self._matrix.skew1
        self.m_matrix.scaleY = m.skew1 * self._matrix.skew0 + m.scaleY * self._matrix.scaleY
        self.m_matrix.translateY = m.skew1 * self.x + m.scaleY * self.y + m.translateY + m.skew1 \
            * self.regX + m.scaleY * self.regY + self.m_matrix.skew1 * -self.regX + self.m_matrix.scaleY * -self.regY

        self.m_colorTransform.Set(c)
        self.m_colorTransform.multi.alpha *= self.alpha

        self.m_lwf.RenderObject()

    def DetachFromParent(self):
        if self.m_parent is not None:
            self.m_parent.DetachBitmap(self.depth)
            self.m_parent = None

    def IsBitmapClip(self):
        return True

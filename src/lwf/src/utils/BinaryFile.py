class BinaryReader:
    def __init__(self, bytesArray):
        self.byteArray = bytesArray
        self.pos = 0

    def ReadByte(self):
        byte = self.byteArray[self.pos]
        self.pos += 1
        return byte

    def ReadBytes(self, length):
        startPos = self.pos
        endPos = self.pos + length
        self.pos += length
        return self.byteArray[startPos:endPos]


    def ReadChar(self):
        return self.unpack('b')

    def ReadUChar(self):
        return self.unpack('B')

    def ReadBool(self):
        return self.unpack('?')

    def ReadInt16(self):
        return self.unpack('h', 2)

    def ReadUInt16(self):
        return self.unpack('H', 2)

    def ReadInt32(self):
        return self.unpack('i', 4)

    def ReadUInt32(self):
        return self.unpack('I', 4)

    def ReadInt64(self):
        return self.unpack('q', 8)

    def ReadUInt64(self):
        return self.unpack('Q', 8)

    def ReadSingle(self):
        return self.unpack('f', 4)

    def ReadDouble(self):
        return self.unpack('d', 8)

    def unpack(self, fmt, length=1):
        return unpack(fmt, self.ReadBytes(length))[0]

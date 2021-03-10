import struct


def clamp(value, min, max):
    if value < min:
        return min
    if value > max:
        return max
    return value


class DataInputStream:

    def __init__(self, fileObject):

        self.istream = None

        self.istream = fileObject

    def read(self):
        return int.from_bytes(self.istream.read(1), byteorder='little', signed=False)

    def readBoolean(self):
        return self.readByte() != 0

    def readByte(self):
        i = self.read()
        if i == -1:
            raise EOFError
        return int.from_bytes((i).to_bytes(1, 'little', signed=False), byteorder='little', signed=True)

    def readChar(self):
        a = self.read()
        b = self.readUnsignedByte()
        return chr((a << 8) | b)

    def readDouble(self):
        return self.readLong()

    def readFloat(self):
        num = self.readInt()
        float_num = struct.unpack('>f', struct.pack('>i', num))[0]
        return float(float_num)

    def readInt(self):
        a = self.read()
        b = self.read()
        c = self.read()
        d = self.readUnsignedByte()
        return int.from_bytes(((a << 24) + (b << 16) + (c << 8) + d).to_bytes(4, 'little'), byteorder='little', signed=True)

    def readLong(self):
        a = self.readInt()
        b = self.readInt() & 0x0ffffffff
        return (a << 32) | b

    def readShort(self):
        a = self.read()
        b = self.readUnsignedByte()
        return int.from_bytes(((a << 8) | b).to_bytes(2, 'little'), byteorder='little', signed=True)

    def readUTF(self):
        bytes = self.readUnsignedShort()
        sb = ""
        while bytes > 0:
            bytes -= self.readUtfChar(sb)
        return sb

    def readUtfChar(self, output):
        a = self.readUnsignedByte()
        if (a & 0x80) == 0:
            output += chr(a)
            return 1
        if (a & 0xe0) == 0xc0:
            b = self.readUnsignedByte()
            output += chr(((a & 0x1F) << 6) | (b & 0x3F))
            return 2
        if (a & 0xf0) == 0xe0:
            b = self.readUnsignedByte()
            c = self.readUnsignedByte()
            output += chr(((a & 0x0F) << 12) | ((b & 0x3F) << 6) | (c & 0x3F))
            return 3
        raise ValueError

    def readUnsignedByte(self):
        i = self.read()
        if i == -1:
            raise EOFError
        return int.from_bytes((i).to_bytes(1, 'little'), byteorder='little', signed=False)

    def readUnsignedShort(self):
        a = self.read()
        b = self.readUnsignedByte()
        return int.from_bytes(((a << 8) | b).to_bytes(2, 'little'), byteorder='little', signed=False)

    def close(self):
        self.istream.close()


class DataInput(DataInputStream):

    def __init__(self, input):
        super().__init__(input)

    def readVarInt(self, optimizePositive=False):
        b = self.read()
        result = b & 0x7F
        if (b & 0x80) != 0:
            b = self.read()
            result |= (b & 0x7F) << 7
            if (b & 0x80) != 0:
                b = self.read()
                result |= (b & 0x7F) << 14
                if (b & 0x80) != 0:
                    b = self.read()
                    result |= (b & 0x7F) << 21
                    if (b & 0x80) != 0:
                        b = self.read()
                        result |= (b & 0x7F) << 28
        result = int.from_bytes(result.to_bytes(4, byteorder='little', signed=False), byteorder='little', signed=True)
        return result if optimizePositive else ((result >> 1) ^ -(result & 1))

    def readString(self):
        charCount = self.readVarInt(True)
        # print("The string is length ", charCount)
        if charCount == 0:
            return None
        elif charCount == 1:
            return ""
        charCount -= 1

        self.chars = []
        charIndex = 0
        b = 0
        while charIndex < charCount:
            b = self.read()
            if b > 127:
                break
            self.chars.append(chr(b))
            # print("read byte ", self.chars[len(self.chars) - 1])
            charIndex += 1
        if charIndex < charCount:
            # print("SLOW")
            self.readUtf8_slow(charCount, charIndex, b)
        s = ""
        for char in self.chars:
            if char == '\x00':
                break
            s += char
        return s

    def readUtf8_slow(self, charCount, charIndex, b):
        while True:
            o = b >> 4
            if 0 <= o <= 7:
                self.chars.append(chr(b))
            elif 12 <= o <= 13:
                self.chars.append(chr((b & 0x1F) << 6 | self.read() & 0x3F))
            elif o == 14:
                self.chars.append(chr((b & 0x0F) << 12 | (self.read() & 0x3F) << 6 | self.read() & 0x3F))
            charIndex += 1
            if charIndex >= charCount:
                break
            b = self.read() & 0xFF
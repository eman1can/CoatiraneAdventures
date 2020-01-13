# Internal Imports
from ..Format import Format
from ..objects.Data import Data

# External Imports
from lzma import LZMADecompressor


class Loader:
    @staticmethod
    def load(d):
        if not d or not isinstance(d, bytes):
            return
        print("Loading Data!")
        print(d)
        return Data(d)

    @staticmethod
    def loadArray(d):
        Loader.load(d)


class CanvasLoader:
    @staticmethod
    def load(d):
        if not d or not isinstance(d, str):
            return None
        option = d[Format.Constant.OPTION_OFFSET] & 0xff
        if option & Format.Constant.OPTION_COMPRESSED == 0:
            return Loader.load(d)
        #if compressed
        a = [0 for _ in range(len(d))]
        for i in range(0, len(d)):
            a[i] = d[i] & 0xff
        return Loader.loadArray(a)

    def loadArray(self, d):
        if not d:
            return None
        option = d[Format.Constant.OPTION_OFFSET]
        if (option & Format.Constant.OPTION_COMPRESSED) == 0:
            return Loader.loadArray(d)

        header = d[0:Format.Constant.HEADER_SIZE]
        compressed = d[Format.Constant.HEADER_SIZE:]
        #if compressed
        try:#implement
            decompressed = LZMADecompressor.decompress(compressed)
        except Exception:
            return None
        d.header.append(decompressed)
        return Loader.loadArray(d)

__all__ = ('read_byte', 'read_int32', 'read_single')

from struct import pack, unpack


def read_byte(data_bytes, index):
    byte = data_bytes[index]
    index += 1
    return byte, index


def read_uInt32(data_bytes, index):
    a, index = read_byte(data_bytes, index)
    b, index = read_byte(data_bytes, index)
    c, index = read_byte(data_bytes, index)
    d, index = read_byte(data_bytes, index)
    return a + (b << 8) + (c << 16) + (d << 24), index


def read_int32(data_bytes, index):
    num, index = read_uInt32(data_bytes, index)
    return unpack('<i', pack('<I', num))[0], index


def read_single(data_bytes, index):
    num, index = read_uInt32(data_bytes, index)
    float_num = unpack('<f', pack('<I', num))[0]
    return float(float_num), index

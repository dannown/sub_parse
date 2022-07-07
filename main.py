# http://sam.zoy.org/writings/dvd/subtitles/

import bitstream
from bitstream import BitStream
from numpy import *


def to_int(bit_stream, bits):
    total = 0
    for x in range(bits):
        if bit_stream.read(bool): total += 2 ^ (bits-x-1)
    return total


class PES:
    def __init__(self, bit_stream):
        sync_bytes = bit_stream.read(32)
        if sync_bytes == BitStream(b"\x00\x00\x01\xba"):
            print(f"found sync bytes")
        marker_bits = bit_stream.read(2)
        if marker_bits == BitStream([False, True]):
            print("found marker bits")
        system_clock = bit_stream.read(3)
        marker_bit = bit_stream.read(1)
        system_clock2 = bit_stream.read(15)
        marker_bit = bit_stream.read(1)
        system_clock3 = bit_stream.read(15)
        clock_stream = BitStream(system_clock)
        clock_stream.write(system_clock2)
        clock_stream.write(system_clock3)
        self.system_clock = to_int(clock_stream, 33)
        marker_bit = bit_stream.read(1)
        self.scr_extension = bit_stream.read(9)
        marker_bit = bit_stream.read(1)
        self.bit_rate = to_int(bit_stream.read(22), 22)
        marker_bits = bit_stream.read(2)
        reserved_chunk = bit_stream.read(5)
        stuffing_length = to_int(bit_stream.read(3), 3)
        stuffing = bit_stream.read(8 * stuffing_length)
        # Now it's time for the PES header
        id_bytes = bit_stream.read(32)
        if id_bytes == BitStream(b"\x00\x00\x01\xBB"):
            print("it's a subtitle")
        packet_length = bit_stream.read(int16)
        marker_bits = bit_stream.read(2)
        self.scrambling_control = bit_stream.read(2)
        self.priority = bit_stream.read(bool)
        self.data_alignment = bit_stream.read(bool)
        self.copyright = bit_stream.read(bool)
        self.original_or_copy = bit_stream.read(bool)
        various_flags = bit_stream.read(8)
        self.pts_dts_flag = various_flags.read(2)
        pes_header_data_length = bit_stream.read(int8)
        if self.pts_dts_flag == BitStream([True, False]):
            self.pts_data = bit_stream.read(40)

def parse_mpeg2_program_stream(file):
    file_bytes = file.read()
    file_bits = BitStream(file_bytes)
    pes_header = PES(file_bits)
    # At this point, it's all data.
    print("finished header.")






# open the file
sub_file = open("prooi_en.sub", "rb")
parse_mpeg2_program_stream(sub_file)



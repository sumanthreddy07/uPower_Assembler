import sys

from pass_1 import get_symbol_table_instructions
from pass_22 import convert_lines
from instruc import int_string

def int_string(val,bits=32):
    #assume val is negative
    val=(1<<(bits-1))+val
    ans="1"+"{0:031b}".format(val)
    return ans

class Assembler:
    def __init__(self):
        pass

    def assemble(self, input_filename, obj_filename="test.o"):
        with open(input_filename, encoding="utf-8", mode="r") as f:
            lines = f.read().splitlines()
            (instructions, label, data, initialized) = get_symbol_table_instructions(lines)
            object_lines = convert_lines(instructions, label, data)

            obj_file_str = ""

        initialized = {int(k, 0): initialized[k] for k in initialized.keys()}

        #data size
        if len(initialized.keys()) == 0:
            len_data = 0
        else:
            #-8 for headers
            last_key = sorted(initialized.keys())[-1]
            if initialized[last_key][-1] == '\0':
                len_data = int(last_key) + len(initialized[last_key]) - 8
            else:
                len_data = last_key - 4


        headers = "{:032b}".format(len_data)
        #text size

        headers += "{:032b}".format(len(instructions) * 4)

        print(f"\nheaders: {headers}")


        data_segment = ""
        for d in sorted(initialized.keys()):
            if initialized[d][-1]=="\0":
                for v in initialized[d]:
                    data_segment += "{:08b}".format(ord(v))

            else:
                val = int(initialized[d])
                if val < 0:
                    val = int_string(val)
                    data_segment +=val
                else:
                    data_segment += "{:032b}".format(val)

        print(f"data_segment: {data_segment}")


        #converting from hex to int
        object_lines = {int(k, 0):object_lines[k] for k in object_lines.keys()}

        text_segment= ""

        for i in sorted(object_lines.keys()):
            # print(f"object_lines key: {i} value: {object_lines[i]}")
            text_segment += object_lines[i]

        print(f"text_segment: {text_segment}")

        obj_file_str = headers + data_segment + text_segment

        # print(f"object file with text segment: {obj_file_str}")

        with open(obj_filename, encoding="utf-8", mode="w+") as o:
            o.write(obj_file_str)

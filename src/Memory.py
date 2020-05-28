import sys

class Memory:
    def __init__(self):
        self.memory = {}

    #single byte
    def get_address(self, address_str):
        if address_str in self.memory:
            return self.memory[addresss_str]
        else:
            print("memory not assigned, returning zero")
            return '0'*8

    #single byte
    def set_address(self, address_str, value):
        # print(f"setting memory address {address_str} to value {value}")
        self.memory[address_str] = value

    def get_byte(self, address_str):
        return self.memory[address_str]

    def get_halfword(self, address_str):
        return "".join([self.memory[str(int(address_str)+i)] for i in range(2)])

    def get_word(self, address_str):
        # print(f"address to access: {address_str}")
        return "".join([self.memory[str(int(address_str)+i)] for i in range(4)])

    def get_doubleword(self, address_str):
        # print(f"get double_word address_str: {address_str}")
        return "".join([self.memory[str(int(address_str)+i)] for i in range(8)])

    def store_byte(self, address_str, value):
        if len(value) == 8:
            self.memory[address_str]= value
        else:
            print(f"store_byte takes only 8 bit values, but got {len(value)}")
            sys.exit(0)

    def store_halfword(self, address_str, value):
        if len(value) == 16:
            for i in range(2):
                self.memory[str(int(address_str) + i)] = value[i*8: 8 + i*8]
        else:
            print(f"store_halfword takes only 16 bit values, but got {len(value)}")
            sys.exit(0)

    def store_word(self, address_str, value):
        if len(value) == 32:
            for i in range(4):
                self.memory[str(int(address_str) + i)] = value[i*8:8 + i*8]
        else:
            print(f"store_word takes only 32 bit values, but got {len(value)}")
            sys.exit(0)

    def store_doubleword(self, address_str, value):
        if len(value) == 64:
            for i in range(8):
                self.memory[str(int(address_str) + i)] = value[i*8:8 + i*8]
        else:
            print(f"store_halfword takes only 64 bit values, but got {len(value)}")
            sys.exit(0)

    def set_n_bytes(self, address_str, value, n):
        if len(value) // 8 == n:
            for i in range(n):
                self.store_byte(
                        str(int(address_str) + i*8),
                        value[i*8:8 + i*8]
                )
        else:
            raise ValueError("length {len(value)} not a multiple of 8")

    def get_string(self, address):
        address = str(int(address, 2))

        if address in self.memory:
            string=""

            while self.memory[address]!='0'*8:
                char = chr(int(self.memory[address], 2))
                string = string + char
                address = str(int(address) + 1)

            return string
        else:
            raise RuntimeError("get_string: address not in memory")

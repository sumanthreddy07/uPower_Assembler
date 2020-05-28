import sys
from Memory import Memory
from Registers import Registers
#from Executioner import Executioner
from Assemble import Assembler

#word in bytes
WORD = 4

class Simulator:
    def __init__(self, asm_filename, obj_filename="../test.o"):
        self.memory = Memory()
        self.registers = Registers()
#        self.executer = Executioner()
        self.assembler = Assembler()

        self.asm_filename = asm_filename
        self.obj_filename = obj_filename

    def run(self):
        self.assembler.assemble(self.asm_filename, self.obj_filename)

        self.registers.cia = -1
        #TODO: NEED START OF TEXT SEGMENT HERE
        self.registers.nia = 0

        try:
            self.obj_file = open(self.obj_filename, mode='r+', encoding='utf-8')
        except:
            print("error while reading file...")
            sys.exit(0)

        obj_data = self.obj_file.read()

        print(f"\n\nObject file inside Simulator.py: {obj_data}")

        # print(f"length of object file in bits: {len(obj_data)} | words: {len(obj_data) / 32}")

        len_data = int(obj_data[:32], 2)
        len_text = int(obj_data[32:64], 2)
        # print(f"len of data: {len_data} | len of text: {len_text}")

        # print(f"{obj_data[:32]} | {obj_data[32:64]}")

        #for now
        data_start = 8
        text_start = data_start + len_data

        #load text and data into memory
        data = obj_data[64:len_data*8+64]
        text = obj_data[64+len_data*8:]

        # print("data: {data}\n\ntext: {text}")

        # print("starting writing data to memory")
        for i in range(len_data):
            self.memory.set_address(str(data_start + i), data[i*8:8+(i*8)])

        # print("\n\nstarting writing text to memory")
        for i in range(len_text):
            self.memory.set_address(str(text_start + i), text[i*8:8+(i*8)])

        # print(f"\n\ndata:{data} {len(data)}\n\ntext: {text} {len(text)}")

        #################################################################
        #now the big bois
        #initialize PCs
        self.registers.cia = text_start
        self.registers.nia = text_start + WORD

        # print(f"\n\nmemory:{self.memory.memory}\n\n")
        # print("before loop")
        # print(f"cia: {self.registers.cia} | cia in memory? {self.registers.cia in self.memory.memory.keys()}")

        while str(self.registers.cia) in self.memory.memory.keys():
            input("\n\npress [enter] to execute next instruction")
            print("\n\n\n")
            instruction = self.memory.get_word(str(self.registers.cia))
            print(f"instruction: {instruction}")

            self.convert_and_execute(instruction)

            self.registers.cia += 4
            print(self.registers)

    def twos_comp(self, val, bits=64):
        '''
            val is a string in signed 2's comp. gets the value as int
        '''
        if val[0] == '1':
            return - 2**(bits - 1) + int(val[1:], 2)
        return int(val, 2)

    def int_string(self, val, bits=64):
        if val >= 0:
            return "{:064b}".format(val)

        val=(1<<(bits-1))+val
        ans="1"+"{0:063b}".format(val)
        return ans


    def convert_and_execute(self, lin):
        '''
            syscall
            R30: syscall type
            R31: syscall address
        '''
        if lin == "0"*32:
            call_type = int(self.registers.R[30], 2)
            address = self.registers.R[31]

            if call_type == 1:
                #word input
                inp = self.int_string(int(input(">>>")))
                self.memory.store_doubleword(address, inp)
            if call_type == 2:
                #word output
                value = self.memory.get_doubleword(str(self.registers.R[31]))
                print(f"\n[OUTPUT BINARY]: {value}\n[OUTPUT DECIMAL]: {self.twos_comp(value)}")
            if call_type == 3:
                #string input
                pass
            if call_type == 4:
                #string output
                value=self.memory.get_string(str(self.registers.R[31]))
                print(f"\n[OUTPUT]\n{value}\n")

        op=int(lin[:6],2)

        if op==31:

            #X-Type instructions
            ex_op=int(lin[22:31],2)

            #cmp
            if ex_op == 0:
                ranum=int(lin[6:11],2)
                bf=int(lin[11:16],2)
                rbnum=int(lin[16:21],2)

                ra = self.registers.R[ranum]
                rb = self.registers.R[rbnum]
                bfval = self.twos_comp(self.registers.R[bf])


                if bfval != 7:
                    raise ValueError("BF is supposed to be 7")

                print("cmp: ra")
                if ra < rb:
                    self.registers.cr = self.registers.cr[:-4] + "1001"
                elif ra == rb:
                    self.registers.cr = self.registers.cr[:-4] + "0010"
                else:
                    self.registers.cr = self.registers.cr[:-4] + "0101"


            if ex_op==27:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2)

                shift_amount=self.twos_comp(self.registers.R[rb][57:])
                self.registers.R[ra]=self.registers.R[rs][shift_amount:]+"0"*shift_amount
                print(f"ra {ra} rb {rb} rs {rs} shift_amount {shift_amount}")
                return

            if ex_op==539:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2)

                shift_amount=self.twos_comp(self.registers.R[rb][57:])
                self.registers.R[ra]="0"*shitf_amount + self.registers.R[rs][:64-shift_amount]
                return

            if ex_op==266:
                #add
                rt=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2)


                self.registers.R[rt]=self.int_string((self.twos_comp(self.registers.R[ra],64)+self.twos_comp(self.registers.R[rb],64)),64)

                return

            if ex_op==40:
                rt=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2)

                self.registers.R[rt]=self.int_string(-(self.twos_comp(self.registers.R[ra],64)+self.twos_comp(self.registers.R[rb],64)),64)

                return

            ex_op=int(lin[21:31],2)

            if ex_op==28:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2)

                self.registers.R[ra]=self.int_string((self.twos_comp(self.registers.R[rs]))&(self.twos_comp(self.registers.R[rb])))
                return

            if ex_op==444:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2)

                self.registers.R[ra]=self.int_string((self.twos_comp(self.registers.R[rs]))|(self.twos_comp(self.registers.R[rb])))
                return

            if ex_op==316:
                rs=int(lin[6:11],2)
                ra=int(lin[11:16],2)
                rb=int(lin[16:21],2)

                self.registers.R[ra]=self.int_string((self.twos_comp(self.registers.R[rs]))^(self.twos_comp(self.registers.R[rb])))
                return

        if op==14:
            #addi
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            si=self.twos_comp(lin[16:],32)

            res = self.twos_comp(self.registers.R[ra]) + si
            # print(f"addi result: {res}")

            self.registers.R[rt]=self.int_string(res)

            return

        if op==15:
            # addi
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            si=self.twos_comp(lin[16:]+"0"*16,32)

            self.registers.R[rt]=self.int_string(self.twos_comp(self.registers.R[ra])+si)
            return

        if op==58:
            # get double word
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            ds=self.twos_comp(lin[16:30]+"00",32)

            add=str(self.twos_comp(self.registers.R[ra])+ds);

            # this function returns doubleword in signed bit format
            self.registers.R[rt]=self.memory.get_doublewordi(add)

            return

        if op==32:
            #lwz
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            ds=self.twos_comp(lin[16:],32)

            add=str(self.twos_comp(self.registers.R[ra], 64)+ds)

            # print(f"address in lwz :{add}")

            self.registers.R[rt]="0"*32+self.memory.get_word(add)

            return

        if op==62:
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            ds=self.twos_comp(lin[16:30]+"00",32)

            add=str(self.twos_comp(self.registers.R[ra])+ds)

            self.memory.store_doubleword(add,self.registers.R[rt])

        if op==36:

            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            d=int(lin[16:],2)

            add=str(int(self.registers.R[ra], 2)+d)

            self.memory.store_word(add,self.registers.R[rt][32:])

            return

        if op==18:
            AA=int(lin[30],2)
            li=int(lin[6:30],2)

            if AA==1:

                registers.cia=li+"0"*40

                return

            if AA=="0":

                self.registers.cia=self.int_string(int(li+"0"*40,2)+int(self.registers.cia,2))

                return

        if op==19:
            # bc instruction
            bo=int(lin[6:11],2)
            bi=int(lin[11:16],2)
            add=self.twos_comp(lin[16:30],14)

            # print(f"bo: {bo} | bi: {bi} | address: {add}")

            if bi==28 and self.registers.cr[28]=='1':
                self.registers.cia+=add;
                return

            elif bi==29 and self.registers.cr[29]=='1':
                self.registers.cia+=add
                return

            elif bi==30 and self.registers.cr[30]=='1':
                self.registers.cia+=add
                return

            elif bi==31 and self.registers.cr[31]=='1':
                self.registers.cia+=add
                return

if __name__ == "__main__":
    obj_filename = "test.o"
    if len(sys.argv[1:]) == 1:
        simulator = Simulator(asm_filename=sys.argv[1], obj_filename=obj_filename)
        simulator.run()
    else:
        print(f"Usage: python3 Simulator.py <assembly file name>")

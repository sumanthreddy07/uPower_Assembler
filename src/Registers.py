class Registers:
    def __init__(self):
        self.R = ['0'*64] * 32
        self.cia = '0' * 64
        self.nia = '0' * 64
        self.lr = '0' * 64
        self.srr0 = '0' * 64
        self.cr = '0' * 32


    def __str__(self):
        res = "Register Status:\n"

        for i in range(32):
            res = res + f"R{i}: {self.R[i]}\n"

        res = res + f"CIA: {self.cia}\n"
        # res = res + f"NIA: {self.nia}\n"
        res = res + f"LR: {self.lr}\n"
        res = res + f"SRR0: {self.srr0}\n"
        res = res + f"CR: {self.cr}\n"

        return res + "\n"

    def __repr__(self):
        return self.__str__()

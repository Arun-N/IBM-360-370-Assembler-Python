
class Compiler:

    def __init__(self):
        self.base_index = ""
        self.base_reg = ""
        self.prog_name = ""
        self.count = 6
        self.current_index = 0
        self.opcode = {}
        self.symbol_table = {}  # {"symbol" : "index value size"}
        self.pass_two_req = False

    def get_sizes(self, filename):
        ptr = 0
        fp = open(filename, 'r')
        codes = fp.read().split()
        while ptr < len(codes):
            self.opcode[codes[ptr]] = codes[ptr+1]
            ptr += 2

        print(self.opcode)

    def tokenize(self, filename):
        fp = open(filename, 'r')
        tokens = fp.read().split()
        return tokens

    def pass1(self, filename):
        self.get_sizes('size.txt')
        tokens = self.tokenize(filename)
        self.prog_name = tokens[0]
        self.base_index = tokens[2]
        self.base_reg = tokens[5]
        print("LC\tOPCODE\tREG\tOFFSET\tINDEX\tBASE REG")
        LC = op_size = reg = offset = b_index = b_reg = 0
        op = None
        while True:
            if tokens[self.count] in self.opcode:   # token is an opcode
                op = tokens[self.count]
                op_size = self.opcode[op]
                self.count += 1
                if tokens[self.count].isnumeric():  # if opcode is followed by register (ex: L 1 FIVE)
                    reg = int(tokens[self.count])
                    self.count += 1
                    if tokens[self.count] in self.symbol_table:  # if there is entry, get offset
                        offset = str(self.symbol_table[tokens[self.count]]).split()[0]
                        print("{lc}\t{opcode}\t{reg}\t{offset}\t{index}\t{basereg}".format(lc=LC,
                                                                                           opcode=op,
                                                                                           reg=reg,
                                                                                           offset=offset,
                                                                                           index=self.base_index,
                                                                                           basereg=self.base_reg))
                        LC += op_size
                        self.count += 1
                    else:
                        self.symbol_table[tokens[self.count]] = ""  # if there is no entry, make a new one
                        offset = "__"   # 2nd pass required
                        self.pass_two_req = True
                        print("{lc}\t{opcode}\t{reg}\t{offset}\t{index}\t{basereg}".format(lc=LC, opcode=op,
                                                                                           reg=reg,
                                                                                           offset=offset,
                                                                                           index=self.base_index,
                                                                                           basereg=self.base_reg))
                        LC += op_size
                        self.count += 1
            elif tokens[self.count] in self.symbol_table:
                op = tokens[self.count]
                if self.symbol_table[op] == "":  # symbol was already encountered
                    self.count += 2
                    if tokens[self.count] in self.symbol_table: # if 'f'
                        op_size = self.opcode[tokens[self.count]]
                        # set symbol_table dict value

compiler = Compiler()
compiler.pass1('xyz.txt')

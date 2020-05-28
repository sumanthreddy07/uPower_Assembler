from instruc import int_string

def twos_comp(val, bits=32):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

def int_string(val,bits=24):
    if val > 0:
        return "{:024b}".format(val)

    val=(1<<(bits-1))+val
    ans="1"+"{0:023b}".format(val)
    return ans

def convert_lines(lines, label, data):
    instruct_x={"and":[31,None,0,28,None,None],"exstw":[31,None,0,986,None,None],"nand":[31,None,0,476,None,None],"or":[31,None,0,444,None,None],"xor":[31,None,0,316,None,None],"sld":[31,None,0,27,None,None],"srd":[31,None,0,539,None,None],"srad":[31,None,0,794,None,None],"cmp":[31,None,0,0,None,None]}

    instruct_xo={"add":[31,0,0,266,None,None],"subf":[31,0,0,40,None,None]}

    instruct_d={"addi":[14,None,None,None,None,0],"addis":[15,None,None,None,None,0],"andi":[28,None,None,None,None,0],"ori":[24,None,None,None,None,0],"xori":[26,None,None,None,None,0],"lwz":[32,None,None,None,None,1],"stw":[36,None,None,None,None,1],"stwu":[37,None,None,None,None,1],"lhz":[40,None,None,None,None,1],"lha":[42,None,None,None,None,1],"sth":[44,None,None,None,None,1],"lbz":[34,None,None,None,None,1],"stb":[38,None,None,None,None,1]}

    instruct_m={"rlwinm":[21,None,0,None,None,None]}

    # sradi

    instruct_xs={"sradi":[31,None,0,413,None,None]}


    instruct_i={"b":[18,None,None,None,0,0],"ba":[18,None,None,None,1,0],"bl":[18,None,None,None,0,1]}

    # take care
    instruct_b={"bc":[19,None,None,None,0,0],"bca":[19,None,None,None,1,0]}

    instruct_ds={"ld":[58,None,None,0,None,None],"std":[62,None,None,0,None,None]}


    reg_to_num={"R"+str(i):i for i in range(32)}
    reg_to_num["LR"]=32
    reg_to_num["CR"]=33
    reg_to_num["SRR0"]=34


    fin_ans={}


    for z in lines:
        #unpack key, value
        u=hex(z)
        v=lines[z]
       # print(f"u: {u}, v: {v}")
        #function name (add, sub, etc.)
        #system call
        if v.strip() == "syscall":
            tmp = "0" * 32
            fin_ans[u] = tmp
            continue

        func=v[:v.index(' ')]
        args=v[v.index(' '):]

        tmp=""
        req=args.split(",")
        req=[i.replace(" ","") for i in req]


        if func in instruct_x.keys():
            tmp=tmp+"{:06b}".format(instruct_x[func][0])
            tmp=tmp+"{:05b}".format(reg_to_num[req[1]])
            tmp=tmp+"{:05b}".format(reg_to_num[req[0]])
            tmp=tmp+"{:05b}".format(reg_to_num[req[2]])
            tmp=tmp+"{:010b}".format(instruct_x[func][3])+"0"
            tmp=tmp.replace("0b","")
            fin_ans[u]=tmp

        elif func in instruct_xo.keys():
            tmp += "{:06b}".format(instruct_xo[func][0])
            tmp += "{:05b}".format(reg_to_num[req[0]])
            tmp += "{:05b}".format(reg_to_num[req[1]])
            tmp += "{:05b}".format(reg_to_num[req[2]])
            tmp += "{:01b}".format(instruct_xo[func][1])
            tmp += "{:09b}".format(instruct_xo[func][3]) + "0"
            tmp = tmp.replace("0b","")
            fin_ans[u]=tmp

        elif func in instruct_d.keys():
            if instruct_d[func][-1] == 1 and '(' in req[1]:
                #func RT, D(RA)
                RT = req[0].strip()

                i1 = req[1].index('(')
                i2 = req[1].index(')')

                SI = int(req[1][:i1].strip())
                RA = req[1][i1+1:i2].strip()

                tmp += "{:06b}".format(instruct_d[func][0])
                tmp += "{:05b}".format(reg_to_num[RT])
                tmp += "{:05b}".format(reg_to_num[RA])
                tmp += "{:016b}".format(SI)
                tmp = tmp.replace("0b","")
                fin_ans[u]=tmp

            elif instruct_d[func][-1] == 0:
                tmp += "{:06b}".format(instruct_d[func][0])
                tmp += "{:05b}".format(reg_to_num[req[0]])
                tmp += "{:05b}".format(reg_to_num[req[1]])
                tmp += "{:016b}".format(int(req[2], 0))
                tmp = tmp.replace("0b","")
                fin_ans[u]=tmp

            else:
                print("\n\nsomething isn't right. D type assembly\n\n")

        elif func in instruct_i.keys():
            tmp += "{:06b}".format(instruct_i[func][0])

            AA = instruct_i[func][-2]
            LI = req[0]

            if AA == 0:
                LI_address = int(label[LI])
                #-4 because CIA gets +4 every time
                offset = int_string(LI_address - z - 4, 24)
                # print(f"LI: {LI} LI_address: {LI_address} | offset: {offset}")

                tmp += offset
            else:
                print("Not Implemented AA=1, ignoring...")
                continue


            #tmp += "{:024b}".format(reg_to_num[req[0]])
            #tmp += "{:01b}".format(instruct_i[func][-2])
            #tmp += "{:01b}".format(instruct_i[func][-1])
            #tmp = tmp.replace("0b","")
            fin_ans[u]=tmp

        elif func in instruct_ds.keys():
            RT = req[0].strip()

            i1 = req[1].index('(')
            i2 = req[1].index(')')

            DS = int(req[1][:i1].strip())
            RA = req[1][i1+1:i2].strip()

            tmp += "{:06b}".format(instruct_d[func][0])
            tmp += "{:05b}".format(reg_to_num[RT])
            tmp += "{:05b}".format(reg_to_num[RA])
            tmp += "{:014b}".format(DS)
            tmp += "{:02b}".format(instruct_d[func][3])
            tmp = tmp.replace("0b","")
            fin_ans[u]=tmp

        elif func in instruct_b.keys():
            # print("B start!! tmp : {}".format(tmp))
            tmp += "{:06b}".format(instruct_b[func][0])
            print(tmp)
            tmp += "{:05b}".format(reg_to_num[req[0]])
            print(tmp)
            tmp += "{:05b}".format(reg_to_num[req[1]])

            if req[2] not in label:
                raise RuntimeError(f"Label: {req[2]} not found in symbol table!!")
                return

            label_address = int(label[req[2]], 0)

            if instruct_b[func][-2] == 0:
                label_address -= int(u, 0) + 4

            def int_to_string14(val):
                if val > 0:
                    return "{:014b}".format(val)

                val=(1<<(13))+val
                ans="1"+"{0:013b}".format(val)
                return ans


            tmp += int_to_string14(label_address)
            print(len(tmp))
            tmp += "{:01b}".format(instruct_b[func][-2])
            print(tmp)
            tmp += "{:01b}".format(instruct_b[func][-1])
            print(tmp)
            # print("B TYPE!!!")

            fin_ans[u] = tmp

        else:
            print(f"command '{func}' not recognized...exiting")
            return

    # print(f"final ans: {fin_ans}")

    return fin_ans

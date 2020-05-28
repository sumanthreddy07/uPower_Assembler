def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)        
    return val            

def int_string(val,bits):
    if val > 0:
        return "{:064b}".format(val)

    val=(1<<(bits-1))+val
    ans="1"+"{0:063b}".format(val)
    return ans


def convert_and_execute(lin):
    op=int(lin[:6],2)

    if op==31:
        ex_op=int(lin[22:31],2)
        
        if ex_op==27:
            rs=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            rb=int(lin[16:21],2)
            
            shift_amount=int(reg[rb][57:],2)
            reg[ra]=reg[rs][:64-shift_amount]+"0"*shift_amount
            return

        if ex_op==539:
            rs=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            rb=int(lin[16:21],2)
            
            shift_amount=int(reg[rb][57:],2)
            reg[ra]="0"*shitf_amount + reg[rs][:64-shift_amount]
            return

        if ex_op==266:
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            rb=int(lin[16:21],2)
             
            
            reg[rt]=int_string((twos_comp(int(reg[ra],2),64)+twos_comp(int(reg[rb],2),32)),64)
            
            return
        
        if ex_op==40:
            rt=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            rb=int(lin[16:21],2) 
            
            reg[rt]=int_string(-(twos_comp(int(reg[ra],2),64)+twos_comp(int(reg[rb],2),64)),64)
            
            return

        ex_op=int(lin[21:31],2)

        if ex_op==28:
            rs=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            rb=int(lin[16:21],2) 

            reg[ra]=int_string((int(reg[rs],2))&(int(reg[rb],2)))
            return 

        if ex_op==444:
            rs=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            rb=int(lin[16:21],2) 

            reg[ra]=int_string((int(reg[rs],2))|(int(reg[rb],2)))
            return 

        if ex_op==316:
            rs=int(lin[6:11],2)
            ra=int(lin[11:16],2)
            rb=int(lin[16:21],2) 

            reg[ra]=int_string((int(reg[rs],2))^(int(reg[rb],2)))
            return 

    if op==14:
        rt=int(lin[6:11],2)
        ra=int(lin[11:16],2)
        si=int(lin[16:],2) 

        reg[rt]=int_string(int(reg[ra],2) + si)

        return

    if op==15:
        rt=int(lin[6:11],2)
        ra=int(lin[11:16],2)
        si=int(lin[16:]+"0"*16,0)

        rt=int_string(int(reg[ra],2)+si)
        return

    if op==58:
        rt=int(lin[6:11],2)
        ra=int(lin[11:16],2)
        ds=int(lin[16:30]+"00",2)
        
        add=reg[ra]+ds;
        
        # this function returns doubleword in signed bit format
        rt=get_doubleword(int_string(add))

        return

    if op==32:
       
        rt=int(lin[6:11],2)
        ra=int(lin[11:16],2)
        ds=int(lin[16:],2)
        
        add=reg[ra]+ds;

        reg[rt]="0"*32+get_word(int_string(add))

        return

    if op==62:
        rt=int(lin[6:11],2)
        ra=int(lin[11:16],2)
        ds=int(lin[16:30]+"00",2)
        
        add=reg[ra]+ds;
        
        store_doubleword(add,reg[rt])

    if op==36:

        rt=int(lin[6:11],2)
        ra=int(lin[11:16],2)
        d=int(lin[16:],2)
        
        add=reg[ra]+ds;
        
        store_word(add,reg[rt][32:])

        return

    if op==18:

        AA=int(lin[30],2)
        li=lin[6:30],2

        if AA=="1":

            registers.NIA=li+"0"*40
            
            return
        
        if AA=="0":

            registers.NIA=int_string(int(li+"0"*40,2)+int(CIA))

            return

import re

def startswith(line, starting, withspace=True):
    if withspace:
        starting = starting + ' '

    l = len(starting)

    if len(line) >= len(starting):
        return line[:l] == starting
    else:
        return False

def preprocess(lines, data, label):
    res = []

    for i in lines:
        lines[i] = lines[i].strip()

        if len(lines[i].strip()) == 0:
            continue
        if " " not in lines[i].strip():
            res.append(lines[i])
            continue

        #print("lines[i]: {}".format(lines[i]))
        tokens_str = lines[i][lines[i].index(' '):].strip()
        tokens = tokens_str.split(',')

        #print(tokens)

        if len(tokens) >= 2 and startswith(lines[i], 'la'):
            Rx, dry = tokens[0].strip(), tokens[1].strip()

            # print("its la!")
            if '(' in dry:
                # print("found (")
                i1 = dry.index('(')
                i2 = dry.index(')')
                D = dry[:i1]
                Ry = dry[i1+1:i2]
                lines[i] = f"addi {Rx}, {Ry}, {D}"
            else:
                # print("no (")

                if dry in data:
                    lines[i] = f"addi {Rx}, R0, {data[dry]}"
                    # print(f"la with address: {lines[i]}")
                else:
                    print(f"{dry} not found in data...")

        elif len(tokens) == 1:
            if startswith(lines[i], 'beq'):
                lines[i] = f"bc R0, R30, {tokens[0]}"
            if startswith(lines[i], 'bne'):
                lines[i] = f"bc R0, R31, {tokens[0]}"

        else:
            lines[i] = lines[i].strip()

    return lines

def get_symbol_table_instructions(lines):
    f = lines

    start_data=0
    start_labels=0
    for i in range(len(f)):
        if f[i]==".text":
            start_labels=i
        if f[i]==".data":
            start_data=i


    cur_location=0x000000
    labels={}
    instruction={}
    var=re.compile(r'.+:')
    for i in range(start_labels+1,len(f)):
        if bool(var.match(f[i])):
            x=re.split(":",f[i])
            labels[x[0].strip()] = hex(cur_location)
            cur_location=cur_location-4
        else:
            tmp=f[i].split('#')[0]
            tmp=" ".join(tmp.split())
            if tmp.strip():
                instruction[cur_location]=tmp
            else:
                cur_location=cur_location-4
        cur_location=cur_location+4


    #32+32 bits text and data segment size in header
    cur_location=0x8
    data={}
    initilized={}
    for i in range(start_data+1,start_labels):
        if bool(var.match(f[i])):
            arr=f[i].split()
            lable=re.split(":",arr[0])[0]
            data[lable]=hex(cur_location)
            datatype=arr[1][1:]
            flag=0
            string=""
            # print(f[i])
            if datatype=="ascii":
                for x in f[i]:
                    #print(i)
                    if x=="\"" and flag==0:
                        flag=1
                        continue
                    if flag==1 and x!="\"":
                        string=string+x
                    if flag==1 and x=="\"":
                        flag=0
                initilized[str(cur_location)]=string+'\0'
            elif datatype=="word":
                x=f[i].split(',')
                for i in range(len(x)):
                    if i==0:
                        initilized[str(cur_location+i*4)]=x[i].split()[-1]
                    else:
                        initilized[str(cur_location+i*4)]=x[i]
            else:
                y=f[i].split("#")
                y=y[0].split()
                if len(y)>=2:
                    initilized[str(cur_location)]=y[2]
            if datatype=="byte":
                cur_location=cur_location+1
            elif datatype=="word":
                x=len(f[i].split(','))
                cur_location=cur_location+4*x
            elif datatype=="halfword":
                cur_location=cur_location+2
            elif datatype=="space":
                cur_location=cur_location+int(arr[2])
            elif datatype=="ascii":
                flag=0
                count=0
                for x in f[i]:
                    if x=="\"" and flag==0:
                        flag=1
                        continue
                    if flag==1 and x!="\"":
                        count=count+1
                    if flag==1 and x=="\"":
                        flag=0

                cur_location=cur_location+count+1

    print(f"\n\nlabels: {labels}\n\n")
    instruction = preprocess(instruction, data, labels)

    return (instruction, labels, data,initilized)


instruct_x={"and":[31,None,0,28,None,None],"exstw":[31,None,0,986,None,None],"nand":[31,None,0,476,None,None],"or":[31,None,0,444,None,None],"xor":[31,None,0,316,None,None],"sld":[31,None,0,794,None,None],"srd":[31,None,0,539,None,None],"srad":[31,None,0,794,None,None],"cmp":[31,None,0,0,None,None]}

instruct_xo={"add":[31,0,0,266,None,None],"subf":[31,0,0,40,None,None]}

instruct_d={"addi":[14,None,None,None,None,0],"addis":[15,None,None,None,None,0],"andi":[28,None,None,None,None,0],"ori":[24,None,None,None,None,0],"xori":[26,None,None,None,None,0],"lwz":[32,None,None,None,None,1],"stw":[36,None,None,None,None,1],"stwu":[37,None,None,None,None,1],"lhz":[40,None,None,None,None,1],"lha":[42,None,None,None,None,1],"sth":[44,None,None,None,None,1],"lbz":[34,None,None,None,None,1],"stb":[38,None,None,None,None,1]}

instruct_m={"rlwinm":[21,None,0,None,None,None]}

# sradi

instruct_xs={"sradi":[31,None,0,413,None,None]}


isntruct_i={"b":[18,None,None,None,0,0],"ba":[18,None,None,None,1,0],"bl":[18,None,None,None,0,1]}

# take care
instruct_b={"bc":[19,None,None,None,0,0],"bca":[19,None,None,None,1,0]}

instruct_ds={"ld":[58,None,None,0,None,None],"std":[62,None,None,0,None,None]}

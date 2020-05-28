.text
    addi R1, R0, 5
    addi R3, R0, 7 #BF 7
    addi R2, R0, 0

    loop:
        addi R2, R2, 1
        cmp R3, R2, R1
        bne loop


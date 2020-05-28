.data
    X: .word 1, 3, 5, 7, 9
.text
    addi R1, R0, 5
    addi R3, R0, 7 #BF 7
    addi R2, R0, 0

    addi R4, R0, 0
    la R5, X

    loop:
        addi R2, R2, 1

        lwz R6, 0(R5)

        add R4, R4, R6

        addi R5, R5, 4

        cmp R3, R2, R1
        bne loop

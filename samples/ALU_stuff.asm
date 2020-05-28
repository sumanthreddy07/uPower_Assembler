.data #global data
X: .word 5
Y: .word 9
SUM: .word 0

.text
#.globl main
main:
    la R1, X
    la R2, Y
    lwz R3, 0(R1)
    lwz R4, 0(R2)

    and R5, R3, R4
    or R6, R3, R4
    xor R7, R3, R4

    sld R8, R3, R4

    addi R10, R0, 2

    srd R9, R4, R10

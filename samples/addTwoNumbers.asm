.data #global data
X: .word 5
Y: .word 10
SUM: .word 0

.text
#.globl main
main:
    la R1, X
    la R2, Y
    lwz R3, 0(R1)
    lwz R4, 0(R2)

    add R5, R3, R4

    la R6, SUM
    stw R5, 0(R6)

    lwz R8, 0(R6)
#    .end

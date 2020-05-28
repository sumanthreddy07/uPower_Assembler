.data #global data
X: .word 5
.text
#.globl main
main:
    addi R30, R0, 1
    la R31, X
    syscall

    addi R30, R0, 2
    la R31, X
    syscall

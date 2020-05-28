.data
x: .ascii "Hellow World"
.text
la R31,x
addi R30,R0,4
syscall

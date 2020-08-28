.data
	arr1: .byte 2 4 -9 6 3 5
    arr2: .byte 1 0 -3 5 3 4

.text
addi x10 x0 5
addi x18 x0 18
addi x19 x0 19
addi x20 x0 20
jal x1 MEMCMP
jal x0 EXIT

MEMCMP:
addi x2 x2 -20
sw x18 0(x2)
sw x19 4(x2)
sw x20 8(x2)
sw x21 12(x2)
sw x22 16(x2)

auipc x6 65536
addi x6 x6 -48
auipc x6 65536
addi x5 x5 -50
addi x18 x0 0
addi x11 x0 0
loop:
add x19 x18 x5
add x20 x18 x6
lb x21 0(x19) 
lb x22 0(x20) 
addi x18 x18 1
addi x10 x10 -1
bne x21 x22 count
bge x10 x0 loop
jalr x0 0(x1)
count: addi x11 x11 1
bge x10 x0 loop
lw x18 0(x2)
lw x19 4(x2)
lw x20 8(x2)
lw x21 12(x2)
lw x22 16(x2)
addi x2 x2 20
jalr x0 0(x1)

EXIT:
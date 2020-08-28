addi x3 x0 7
addi x1 x0 0
addi x2 x0 1
addi x5 x0 1
addi x6 x0 2

loop:
	sub x3 x3 x5
  	add x4 x1 x2
  	add x1 x2 x0
  	add x2 x4 x0
  	bne x3 x6 loop
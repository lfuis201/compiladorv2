.data
	var_x: .word 270
	var_y: .word 1
	var_z: .word 270
	var_bol1: .word 270
.text
main:
    lw $t0, var_x

    lw $t1, var_y


    add $t3, $t1, $t0


    # imprimimos el promedio
    li $v0,1
    move $a0, $t3
    syscall

 	li $v0,10 
 	syscall 
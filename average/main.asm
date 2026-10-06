section .data
        err_msg db "Error: file is corrupted or not found", 0x0A
        err_len equ $ - err_msg
        res_msg db "Result: "
        res_len equ $ - res_msg

section .bss
        buffer resb 4096
        bytes_read resq 1
        first_line resq 100
        second_line resq 100
        count_first resq 1

section .text
global _start
_start:
        mov rdi, [rsp + 16]
        test rdi, rdi
        jz file_error

        mov rsi, 0
        mov rdx, 0
        mov rax, 2                      ; sys_open
        syscall

        cmp rax, 0
        jl file_error

        mov rdi, rax
        mov rax, 0                      ; sys_read
        mov rsi, buffer
        mov rdx, 4096
        syscall

        cmp rax, 0
        jle file_error

        mov [bytes_read], rax

        xor rsi, rsi
        xor rcx, rcx

parse_first_line:
        cmp rsi, [bytes_read]
        jge reset_rcx

        mov bl, [buffer + rsi]

        cmp bl, 0x0A
        je reset_rcx

        cmp bl, '0'
        jl not_num_first_line
        cmp bl, '9'
        jg not_num_first_line

        xor rax, rax

calculate_number_first:
        sub bl, '0'
        imul rax, rax, 10
        xor rdx, rdx
        mov dl, bl
        add rax, rdx

        inc rsi

        cmp rsi, [bytes_read]
        jge save_and_reset_rcx

        mov bl, [buffer + rsi]

        cmp bl, '0'
        jl finish_num_first
        cmp bl, '9'
        jle calculate_number_first

finish_num_first:
        mov [first_line + rcx*8], rax
        inc rcx
        jmp parse_first_line

not_num_first_line:
        cmp bl, ' '
        je skip_delim_first
        cmp bl, ','
        je skip_delim_first
        jmp file_error

skip_delim_first:
        inc rsi
        jmp parse_first_line

save_and_reset_rcx:
        mov [first_line + rcx*8], rax
        inc rcx

reset_rcx:
        mov [count_first], rcx
        inc rsi
        xor rcx, rcx
        xor rax, rax

parse_second_line:
        cmp rsi, [bytes_read]
        jge check_counts

        mov bl, [buffer + rsi]

        cmp bl, 0x0A
        je check_counts

        cmp bl, '0'
        jl not_num_second_line
        cmp bl, '9'
        jg not_num_second_line

        xor rax, rax

calculate_number_second:
        sub bl, '0'
        imul rax, rax, 10
        xor rdx, rdx
        mov dl, bl
        add rax, rdx

        inc rsi

        cmp rsi, [bytes_read]
        jge save_and_finish_second

        mov bl, [buffer + rsi]

        cmp bl, '0'
        jl finish_num_second
        cmp bl, '9'
        jle calculate_number_second

finish_num_second:
        mov [second_line + rcx*8], rax
        inc rcx
        jmp parse_second_line

not_num_second_line:
        cmp bl, ' '
        je skip_delim_second
        cmp bl, ','
        je skip_delim_second
        jmp file_error

skip_delim_second:
        inc rsi
        jmp parse_second_line

save_and_finish_second:
        mov [second_line + rcx*8], rax
        inc rcx

check_counts:
        cmp rcx, [count_first]
        jne file_error

update:
        xor rcx, rcx
        xor rdx, rdx
        xor rax, rax

calculate_value:
        cmp rcx, [count_first]
        je result

        mov rax, [first_line + rcx*8]
        add rdx, rax
        mov rax, [second_line + rcx*8]
        sub rdx, rax
        inc rcx

        jmp calculate_value

file_error:
        mov rax, 1                      ; sys_write
        mov rdi, 1
        mov rsi, err_msg
        mov rdx, err_len
        syscall

        mov rax, 60                     ; sys_exit
        mov rdi, 1
        syscall

result:
        mov rax, rdx
        cqo
        idiv qword [count_first]
        jmp exit_program

exit_program:
        mov rbx, rax
        mov rax, 1                      ; sys_write
        mov rdi, 1
        mov rsi, res_msg
        mov rdx, res_len
        syscall

        mov rax, 60                     ; sys_exit
        mov rdi, rbx
        syscall

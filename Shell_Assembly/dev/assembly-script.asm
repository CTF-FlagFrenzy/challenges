section .data
    env_var db 'HOME', 0  ; Environment variable name
    newline db 0xA

section .text

    extern getenv
    extern puts
    extern exit
    global _start

_start:
    ; Save the current base pointer
    push rbp

    ; Set the new base pointer
    mov rbp, rsp

    ; Allocate space for the environment variable name
    sub rsp, 8

    ; Copy the environment variable name to the stack
    lea rdi, [env_var]
    call getenv

    ; Restore the stack
    add rsp, 8

    ; Save the result in a register
    mov rbx, rax

    ; Check if the environment variable was found
    test rax, rax
    jz env_var_not_found

    ; Print the environment variable value
    mov rdi, rax
    call puts

    ; Exit the program
    mov edi, 0
    call exit

env_var_not_found:
    ; Print an error message
    lea rdi, [error_msg]
    call puts

    ; Exit the program with an error code
    mov edi, 1
    call exit

section .data
    error_msg db 'Environment variable not found', 0

section .bss
    resb 8
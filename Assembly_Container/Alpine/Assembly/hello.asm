;---------------------
;  Flat Assembler file
;  Syscall Hello World
;---------------------
section .data
msg db 'Hello 64-bit world!', 0xA
msg_size equ $ - msg

section .text
global _start

_start:
  ; sys_write
  mov edx, msg_size
  lea rsi, [msg]
  mov edi, 1
  mov eax, 1
  syscall

  ; sys_exit
  mov eax, 60
  xor edi, edi
  syscall
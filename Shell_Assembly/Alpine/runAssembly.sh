#!/bin/sh
cd /uploads
# compile
nasm -f elf64 assembly-script.asm -o script.o
# link
ld script.o -o script -dynamic-linker /lib/ld-musl-x86_64.so.1 -lc
# run
./script
# compile
nasm -f elf64 hello.asm -o hello.o
# link
ld hello.o -o hello
# run
./hello
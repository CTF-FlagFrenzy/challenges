# Use the official Alpine image as the base image
FROM alpine:latest

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary packages and dependencies
RUN sh installation.sh

#DEBUG DO NOT LEAVE IN FINAL VERSION
#DEBUG DO NOT LEAVE IN FINAL VERSION
#DEBUG DO NOT LEAVE IN FINAL VERSION
#DEBUG DO NOT LEAVE IN FINAL VERSION
#DEBUG DO NOT LEAVE IN FINAL VERSION
#DEBUG DO NOT LEAVE IN FINAL VERSION
# Assemble the hello.asm file
RUN nasm -f elf64 ./Assembly/hello.asm -o ./Assembly/hello.o

# Link the object file to create an executable
RUN ld ./Assembly/hello.o -o ./Assembly/hello -lc --dynamic-linker /lib/ld-musl-x86_64.so.1
#DEBUG DO NOT LEAVE IN FINAL VERSION
#DEBUG DO NOT LEAVE IN FINAL VERSION
#DEBUG DO NOT LEAVE IN FINAL VERSION
#DEBUG DO NOT LEAVE IN FINAL VERSION
#DEBUG DO NOT LEAVE IN FINAL VERSION
#DEBUG DO NOT LEAVE IN FINAL VERSION



# Run a simple command to keep the container running
CMD ["sh", "-c", "while true; do sleep 3600; done"]
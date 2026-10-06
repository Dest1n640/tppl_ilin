ASM = nasm
ASMFLAGS = -felf64
LD = ld
TARGET = average
SRC = main.asm
OBJ = main.o

.PHONY: all run clean

all: $(TARGET)

$(TARGET): $(OBJ)
	$(LD) $(OBJ) -o $(TARGET)

$(OBJ): $(SRC)
	$(ASM) $(ASMFLAGS) $(SRC) -o $(OBJ)

run: $(TARGET)
	./$(TARGET) data.txt

clean:
	rm -f $(OBJ) $(TARGET)

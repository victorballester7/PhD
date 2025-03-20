# Compiler and flags
CC := gcc
CFLAGS := -Wall -Wextra -pedantic -std=c17 -fPIC

# Libraries
LIBS := -lopenblas -lm

# Folders
SRC := src_c
INCLUDE := include
BIN := bin

# Executable name
TARGET := main

# We create a list of all the sources by looking for all the .c files
SOURCES := $(wildcard $(SRC)/*.c)

# We create a list of object files by replacing the .c extension with .o in the list of sources
OBJECTS := $(patsubst $(SRC)/%.c,$(BIN)/%.o,$(SOURCES))

# We need to tell the compiler where to find the headers
HEADERS := $(wildcard $(INCLUDE)/*.h)

# .PHONY target specifies that all and clean are not real files, but are just targets that don't produce output files.
.PHONY: all clean

# Default target
all: $(BIN)/$(TARGET)

# We compile the .c files into object files
$(BIN)/%.o: $(SRC)/%.c | $(BIN)
	@$(CC) $(CFLAGS) -I$(INCLUDE) -c $< -o $@

# We link the object files to create the executable
$(BIN)/$(TARGET): $(OBJECTS)
	@$(CC) $(CFLAGS) $^ -o $@ $(LIBS)

# Ensure the bin directory exists
$(BIN):
	@mkdir -p $(BIN)

# Clean target
clean:
	@rm -rf $(BIN)/*.o $(BIN)/$(TARGET)


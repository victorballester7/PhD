# Compiler and flags
CC := gcc
CXX := g++
CXXFLAGS := -Wall -Wextra -Wpedantic -Wshadow -Wformat=2 -Wcast-align -Wconversion -Wsign-conversion -Wnull-dereference -g3 -Ofast -std=c++11
CFLAGS := -Wall -Wextra -pedantic -Ofast -std=c11

# Libraries
LIBS := -lopenblas -lm

# Folders
SRC := src
INCLUDE := include
BIN := bin

# Executable name
TARGET := main

# Sources and objects
SOURCES := $(wildcard $(SRC)/*.c) $(wildcard $(SRC)/*.cpp)
OBJECTS := $(patsubst $(SRC)/%.cpp, $(BIN)/%.o, $(filter %.cpp, $(SOURCES))) $(patsubst $(SRC)/%.c, $(BIN)/%.o, $(filter %.c, $(SOURCES))) 

# Headers
HEADERS := $(wildcard $(INCLUDE)/*.h) $(wildcard $(INCLUDE)/*.hpp)

# .PHONY target specifies that all and clean are not real files, but are just targets that don't produce output files.
.PHONY: all clean

# Default target
all: $(BIN)/$(TARGET)

$(BIN)/$(TARGET): $(OBJECTS)
	@$(CXX) $(CXXFLAGS) -o $@ $^ $(LIBS)

$(BIN)/%.o: $(SRC)/%.cpp $(HEADERS)
	@$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

$(BIN)/%.o: $(SRC)/%.c $(HEADERS)
	@$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# Ensure the bin directory exists
$(BIN):
	@mkdir -p $(BIN)

# Clean target
clean:
	@rm -rf $(BIN)/*.o $(BIN)/$(TARGET)


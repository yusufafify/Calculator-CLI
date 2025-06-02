# Makefile for calculator_cli

# Compiler and flags
CC = gcc
CFLAGS = -I c_src -Wall -Werror -O2

# Source and output
SRC = c_src/calculate.c

ifeq ($(OS),Windows_NT)
    DLL = c_src/calculate.dll
    DLL_CMD = $(CC) -shared -o $(DLL) $(SRC) $(CFLAGS)
    CLEAN_CMD = del /Q c_src\*.dll 2>nul || true & del /Q c_src\*.exe 2>nul || true
else
    DLL = c_src/libcalculate.so
    DLL_CMD = $(CC) -shared -fPIC -o $(DLL) $(SRC) $(CFLAGS)
    CLEAN_CMD = rm -f c_src/*.so c_src/*.out
endif

# Default target
all: $(DLL)

# Build DLL/shared object for Python usage
$(DLL): $(SRC)
	$(DLL_CMD)

# Clean build artifacts
clean:
	$(CLEAN_CMD)

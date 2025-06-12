# Makefile for calculator_cli
# ---------------------------

# ── Compiler ────────────────────────────────────────────────────────────────────
CC      ?= gcc
CFLAGS_BASE := -I c_src -Wall -Werror -O2 -lm
CFLAGS_STANDALONE := $(CFLAGS_BASE) -DEXCLUDE_PYTHON_CODE
CFLAGS_PYTHON := $(CFLAGS_BASE)
SRC     := c_src/calculate.c

# ── Python / venv ───────────────────────────────────────────────────────────────
PYTHON   ?= python
VENV_DIR ?= .venv

# ── Python Development Libraries ───────────────────────────────────────────────
# Find Python include directories and libraries for linking
PYTHON_INCLUDE := $(shell $(PYTHON) -c "import sysconfig; print(sysconfig.get_path('include'))")
PYTHON_LIBS := $(shell $(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('LIBS'))")
PYTHON_LDFLAGS := $(shell $(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('LDFLAGS'))")

ifeq ($(OS),Windows_NT)
# On Windows, we need to link against python3X.lib
PYTHON_VERSION := $(shell $(PYTHON) -c "import sys; print(f'{sys.version_info.major}{sys.version_info.minor}')")
PYTHON_LIB_PATH := $(shell $(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('prefix'))")
PYTHON_LINK_FLAGS := -I"$(PYTHON_INCLUDE)" -L"$(PYTHON_LIB_PATH)/libs" -lpython$(PYTHON_VERSION)
else
PYTHON_LINK_FLAGS := -I"$(PYTHON_INCLUDE)" $(PYTHON_LDFLAGS) $(PYTHON_LIBS)
endif

# ── Platform-specific paths & commands ─────────────────────────────────────────
ifeq ($(OS),Windows_NT)                      # ── WINDOWS ───────────────────────
VENV_SITE_PACKAGES := $(VENV_DIR)/Lib/site-packages
DEST_DIR           := $(VENV_SITE_PACKAGES)/calculator_c
DLL_STANDALONE     := c_src/calculate.dll
DLL_PYTHON         := c_src/calculator_c.dll
DLL                := $(DLL_PYTHON)  # Default to Python extension DLL

# Standalone DLL (no Python dependencies) 
DLL_STANDALONE_CMD = $(CC) -shared -o $(DLL_STANDALONE) $(SRC) $(CFLAGS_STANDALONE)
# Python extension DLL (with Python wrapper functions)
DLL_PYTHON_CMD = $(CC) -shared -o $(DLL_PYTHON) $(SRC) $(CFLAGS_PYTHON) $(PYTHON_LINK_FLAGS)
DLL_CMD = $(DLL_PYTHON_CMD)  # Default to building Python extension

MKDIR_CMD = if not exist "$(subst /,\,$(DEST_DIR))" mkdir "$(subst /,\,$(DEST_DIR))"
COPY_STANDALONE_CMD = copy /Y "$(subst /,\,$(DLL_STANDALONE))" "$(subst /,\,$(DEST_DIR))"
COPY_PYTHON_CMD = copy /Y "$(subst /,\,$(DLL_PYTHON))" "$(subst /,\,$(DEST_DIR))"
COPY_CMD = $(COPY_PYTHON_CMD)  # Default to copying Python extension
CLEAN_CMD = del /Q c_src\*.dll 2>nul || true & del /Q c_src\*.exe 2>nul || true

else                                         # ── LINUX / macOS ─────────────────
# Ask the venv’s Python for its pure-lib directory → version-agnostic
VENV_SITE_PACKAGES := $(shell $(PYTHON) - <<PY \
import sysconfig, pathlib, sys; \
print(pathlib.Path('$(VENV_DIR)').joinpath( \
      'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', \
      'site-packages')); \
PY)

DEST_DIR := $(VENV_SITE_PACKAGES)/calculator_c
DLL      := c_src/libcalculate.so

DLL_CMD   = $(CC) -shared -fPIC -o $(DLL) $(SRC) $(CFLAGS)
MKDIR_CMD = mkdir -p $(DEST_DIR)
COPY_CMD  = cp $(DLL) $(DEST_DIR)
CLEAN_CMD = rm -f c_src/*.so c_src/*.out
endif

# ── Build targets ──────────────────────────────────────────────────────────────
.PHONY: all python-install clean standalone python-dll

all: $(DLL)

$(DLL): $(SRC)
	$(DLL_CMD)

# Build standalone DLL (no Python dependencies)
standalone: $(DLL_STANDALONE)

$(DLL_STANDALONE): $(SRC)
	$(DLL_STANDALONE_CMD)

# Build Python extension DLL (with Python wrapper functions)
python-dll: $(DLL_PYTHON)

$(DLL_PYTHON): $(SRC)
	$(DLL_PYTHON_CMD)

# ── Install library + Python shim into venv ────────────────────────────────────
python-install: $(DLL)
	$(MKDIR_CMD)
	$(COPY_CMD)
ifeq ($(OS),Windows_NT)
	@echo from ctypes import CDLL, c_float > "$(subst /,\,$(DEST_DIR))\\__init__.py" 
	@echo import os, sys >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
	@echo _dll = CDLL(os.path.join(os.path.dirname(__file__), 'calculator_c.dll')) >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
	@echo _dll.add.argtypes = [c_float, c_float] >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
	@echo _dll.add.restype = c_float >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
	@echo _dll.subtract.argtypes = [c_float, c_float] >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
	@echo _dll.subtract.restype = c_float >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
	@echo _dll.multiply.argtypes = [c_float, c_float] >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
	@echo _dll.multiply.restype = c_float >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
	@echo _dll.divide.argtypes = [c_float, c_float] >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
	@echo _dll.divide.restype = c_float >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
	@echo def add(a, b): return _dll.add(float(a), float(b)) >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
	@echo def subtract(a, b): return _dll.subtract(float(a), float(b)) >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
	@echo def multiply(a, b): return _dll.multiply(float(a), float(b)) >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
	@echo def divide(a, b): return _dll.divide(float(a), float(b)) >> "$(subst /,\,$(DEST_DIR))\\__init__.py"
else
	@echo from ctypes import CDLL, c_float > "$(DEST_DIR)/__init__.py"
	@echo import os, sys >> "$(DEST_DIR)/__init__.py"
	@echo _dll = CDLL(os.path.join(os.path.dirname(__file__), 'libcalculate.so')) >> "$(DEST_DIR)/__init__.py"
	@echo _dll.add.argtypes = [c_float, c_float] >> "$(DEST_DIR)/__init__.py"
	@echo _dll.add.restype = c_float >> "$(DEST_DIR)/__init__.py"
	@echo _dll.subtract.argtypes = [c_float, c_float] >> "$(DEST_DIR)/__init__.py"
	@echo _dll.subtract.restype = c_float >> "$(DEST_DIR)/__init__.py"
	@echo _dll.multiply.argtypes = [c_float, c_float] >> "$(DEST_DIR)/__init__.py"
	@echo _dll.multiply.restype = c_float >> "$(DEST_DIR)/__init__.py"
	@echo _dll.divide.argtypes = [c_float, c_float] >> "$(DEST_DIR)/__init__.py"
	@echo _dll.divide.restype = c_float >> "$(DEST_DIR)/__init__.py"
	@echo def add(a, b): return _dll.add(float(a), float(b)) >> "$(DEST_DIR)/__init__.py"
	@echo def subtract(a, b): return _dll.subtract(float(a), float(b)) >> "$(DEST_DIR)/__init__.py"
	@echo def multiply(a, b): return _dll.multiply(float(a), float(b)) >> "$(DEST_DIR)/__init__.py"
	@echo def divide(a, b): return _dll.divide(float(a), float(b)) >> "$(DEST_DIR)/__init__.py"
endif
	@echo DLL installed to Python environment as 'calculator_c'
	@echo You can now use: import calculator_c



# ── Test targets ───────────────────────────────────────────────────────────────
test: test-c test-python
	@echo ======================================
	@echo All tests completed successfully!
	@echo ======================================

test-c:
	@echo ======================================
	@echo Running C unit tests...
	@echo ======================================
ifeq ($(OS),Windows_NT)
	@cd tests_c && $(CC) -o test_runner.exe calculateTest.c Unity/unity.c ../c_src/calculate.c -I../c_src -IUnity -lm -DEXCLUDE_PYTHON_CODE
	@cd tests_c && test_runner.exe
	@cd tests_c && del /Q test_runner.exe 2>nul || true
else
	@cd tests_c && $(CC) -o test_runner calculateTest.c Unity/unity.c ../c_src/calculate.c -I../c_src -IUnity -lm -DEXCLUDE_PYTHON_CODE
	@cd tests_c && ./test_runner
	@cd tests_c && rm -f test_runner
endif

test-python: $(DLL) python-install
	@echo ======================================
	@echo Running Python unit tests...
	@echo ======================================
ifeq ($(OS),Windows_NT)
	@if exist "$(VENV_DIR)\Scripts\python.exe" ( \
		"$(VENV_DIR)\Scripts\python.exe" -m pytest tests_py/ -v \
	) else ( \
		$(PYTHON) -m pytest tests_py/ -v \
	)
else
	@if [ -f "$(VENV_DIR)/bin/python" ]; then \
		$(VENV_DIR)/bin/python -m pytest tests_py/ -v; \
	else \
		$(PYTHON) -m pytest tests_py/ -v; \
	fi
endif


# ── Clean ──────────────────────────────────────────────────────────────────────
clean:
	$(CLEAN_CMD)

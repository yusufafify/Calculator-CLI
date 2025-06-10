# Choose DLL name for python __init__.py
if(WIN32)
  set(DLL_NAME "libcalculate.dll")
else()
  set(DLL_NAME "libcalculate.so")
endif()

# Find site-packages inside the current venv (assumes Python executable is in env)
execute_process(
  COMMAND python -c
  "import sysconfig, pathlib; print(sysconfig.get_path('purelib'))"
  OUTPUT_VARIABLE SITE_PACKAGES
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

set(DEST_DIR "${SITE_PACKAGES}/calculator_c")
file(MAKE_DIRECTORY "${DEST_DIR}")

# Copy from build output directory (assumes OUTPUT_BIN passed or use env var)
if(WIN32)
  file(COPY "${CMAKE_CURRENT_BINARY_DIR}/c_src/libcalculate.dll" DESTINATION "${DEST_DIR}")
else()
  file(COPY "${CMAKE_CURRENT_BINARY_DIR}/c_src/libcalculate.so" DESTINATION "${DEST_DIR}")
endif()  #refractor, use variable  , update name in python wrapper

# Write __init__.py with injected DLL name
file(WRITE "${DEST_DIR}/__init__.py" "
from ctypes import CDLL, c_float
import os

_dll_path = os.path.join(os.path.dirname(__file__), '${DLL_NAME}')
_dll = CDLL(_dll_path)

_dll.add.argtypes = [c_float, c_float]
_dll.add.restype = c_float
_dll.subtract.argtypes = [c_float, c_float]
_dll.subtract.restype = c_float
_dll.multiply.argtypes = [c_float, c_float]
_dll.multiply.restype = c_float
_dll.divide.argtypes = [c_float, c_float]
_dll.divide.restype = c_float

def add(a, b): return _dll.add(float(a), float(b))
def subtract(a, b): return _dll.subtract(float(a), float(b))
def multiply(a, b): return _dll.multiply(float(a), float(b))
def divide(a, b): return _dll.divide(float(a), float(b))
")

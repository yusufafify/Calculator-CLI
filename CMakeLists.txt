cmake_minimum_required(VERSION 3.10)
project(calculator_c C)

# Source file
set(SRC c_src/calculate.c)

# Find Python development environment (needed for Python.h)
find_package(Python REQUIRED COMPONENTS Development)
include_directories(${Python_INCLUDE_DIRS})

# Output directory for compiled libraries
set(OUTPUT_DIR "${CMAKE_CURRENT_BINARY_DIR}/c_src")  
file(MAKE_DIRECTORY "${OUTPUT_DIR}")               

# Determine output name and platform specifics
set(LIB_NAME calculate)

if(WIN32)
    add_library(${LIB_NAME} SHARED ${SRC})
    set_target_properties(${LIB_NAME} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY "${OUTPUT_DIR}"     
        OUTPUT_NAME "calculate"
    )
else()
    add_library(${LIB_NAME} SHARED ${SRC})
    set_target_properties(${LIB_NAME} PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${OUTPUT_DIR}"   
        OUTPUT_NAME "libcalculate"
    )
endif()

target_link_libraries(${LIB_NAME} PRIVATE ${Python_LIBRARIES})

# Path to final shared lib file (used in install and clean)
if(WIN32)
    set(OUTPUT_BIN "${OUTPUT_DIR}/libcalculate.dll")
else()
    set(OUTPUT_BIN "${OUTPUT_DIR}/libcalculate.so")
endif()

# Install target to copy the shared library into the Python venv
add_custom_target(python-install ALL
    COMMAND ${CMAKE_COMMAND} -E echo "Installing to Python virtual environment..."
    COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_SOURCE_DIR}/cmake/python_install.cmake
    DEPENDS ${LIB_NAME}
)

# Clean target to remove only the generated .dll or .so file
add_custom_target(clean-lib
    COMMAND ${CMAKE_COMMAND} -E echo "Removing generated library..."
    COMMAND ${CMAKE_COMMAND} -E rm -f "${OUTPUT_BIN}"
    COMMENT "Cleaning shared library files"
)


#where to install cmake and ninja
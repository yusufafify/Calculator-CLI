cmake_minimum_required(VERSION 3.10)
project(calculator_c C)

# Source file
set(SRC c_src/calculate.c)

# Find Python development environment (needed for pip install, optional for deployment)
find_package(Python REQUIRED COMPONENTS Development)
include_directories(${Python_INCLUDE_DIRS})

# Handle Python library linking carefully on Windows
if(WIN32)
    # Try to find the release version of Python library to avoid debug issues
    if(Python_LIBRARIES)
        # Check if we're trying to link against debug libraries
        string(FIND "${Python_LIBRARIES}" "python3" HAS_PYTHON3)
        string(FIND "${Python_LIBRARIES}" "_d.lib" HAS_DEBUG_LIB)
        
        if(HAS_DEBUG_LIB GREATER -1)
            # Replace debug library with release library
            string(REPLACE "_d.lib" ".lib" Python_LIBRARIES_RELEASE "${Python_LIBRARIES}")
            if(EXISTS "${Python_LIBRARIES_RELEASE}")
                set(Python_LIBRARIES "${Python_LIBRARIES_RELEASE}")
                message(STATUS "Using release Python library: ${Python_LIBRARIES}")
            endif()
        endif()
    endif()
    set(PYTHON_AVAILABLE TRUE)
else()
    set(PYTHON_AVAILABLE TRUE)
endif()

# Output directory for compiled libraries
set(OUTPUT_DIR "${CMAKE_CURRENT_BINARY_DIR}/c_src")  
file(MAKE_DIRECTORY "${OUTPUT_DIR}")               

# Determine output name and platform specifics
set(LIB_NAME calculate)

if(WIN32)
    add_library(${LIB_NAME} SHARED ${SRC})
    set_target_properties(${LIB_NAME} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY "${OUTPUT_DIR}"     
        OUTPUT_NAME "libcalculate"
        PREFIX ""
    )
    # Exclude Python code for standalone builds on Windows
    if(SKIP_PYTHON_INSTALL)
        target_compile_definitions(${LIB_NAME} PRIVATE EXCLUDE_PYTHON_CODE)
    endif()
else()
    add_library(${LIB_NAME} SHARED ${SRC})
    set_target_properties(${LIB_NAME} PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${OUTPUT_DIR}"   
        OUTPUT_NAME "libcalculate"
    )
endif()

# Handle Python library linking based on build type
if(SKIP_PYTHON_INSTALL)
    # For deployment builds, don't link Python libraries on Windows to avoid debug issues
    if(NOT WIN32 AND PYTHON_AVAILABLE)
        target_link_libraries(${LIB_NAME} PRIVATE ${Python_LIBRARIES})
    endif()
else()
    # For pip install, try to link Python libraries but handle debug library issues
    if(PYTHON_AVAILABLE)
        target_link_libraries(${LIB_NAME} PRIVATE ${Python_LIBRARIES})
    endif()
endif()

# Path to final shared lib file (used in install and clean)
if(WIN32)
    set(OUTPUT_BIN "${OUTPUT_DIR}/libcalculate.dll")
    set(SOURCE_DIR_BIN "${CMAKE_CURRENT_SOURCE_DIR}/c_src/libcalculate.dll")
else()
    set(OUTPUT_BIN "${OUTPUT_DIR}/libcalculate.so")
    set(SOURCE_DIR_BIN "${CMAKE_CURRENT_SOURCE_DIR}/c_src/libcalculate.so")
endif()

# Copy built library to source directory for deployment compatibility
add_custom_command(TARGET ${LIB_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy "$<TARGET_FILE:${LIB_NAME}>" "${CMAKE_CURRENT_SOURCE_DIR}/c_src/"
    COMMENT "Copying library to source directory for deployment"
)

# Install target to copy the shared library into the Python venv (optional)
# This can be disabled by setting -DSKIP_PYTHON_INSTALL=ON
option(SKIP_PYTHON_INSTALL "Skip Python virtual environment installation" OFF)
if(NOT SKIP_PYTHON_INSTALL)
    add_custom_target(python-install ALL
        COMMAND ${CMAKE_COMMAND} -E echo "Installing to Python virtual environment..."
        COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_SOURCE_DIR}/cmake/python_install.cmake
        DEPENDS ${LIB_NAME}
    )
endif()

# Clean target to remove only the generated .dll or .so file
add_custom_target(clean-lib
    COMMAND ${CMAKE_COMMAND} -E echo "Removing generated library..."
    COMMAND ${CMAKE_COMMAND} -E rm -f "${OUTPUT_BIN}"
    COMMAND ${CMAKE_COMMAND} -E rm -f "${CMAKE_CURRENT_SOURCE_DIR}/c_src/libcalculate.dll"
    COMMAND ${CMAKE_COMMAND} -E rm -f "${CMAKE_CURRENT_SOURCE_DIR}/c_src/libcalculate.so"
    COMMENT "Cleaning shared library files"
)

# Testing
enable_testing()

file(GLOB TEST_SOURCES CONFIGURE_DEPENDS "tests_c/*.c")
set(UNITY_SOURCES tests_c/unity/unity.c)

add_executable(test_calculator ${TEST_SOURCES} ${UNITY_SOURCES})
target_include_directories(test_calculator PRIVATE tests_c c_src)
target_link_libraries(test_calculator PRIVATE calculate)

# custom target to run C tests manually like a regular command
add_custom_target(
  run_c_tests
  COMMAND ${CMAKE_COMMAND} -E env
          "PATH=$<TARGET_FILE_DIR:calculate>;$ENV{PATH}"
          $<TARGET_FILE:test_calculator>
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  COMMENT "Running C unit tests"
  DEPENDS test_calculator
)

# Python tests target
find_package(Python REQUIRED COMPONENTS Interpreter)

# Add target to run Python tests
add_custom_target(
  run_python_tests
  COMMAND ${Python_EXECUTABLE} -m pytest ${CMAKE_SOURCE_DIR}/tests_py -v
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  COMMENT "Running Python unit tests with pytest"
)

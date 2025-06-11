#!/usr/bin/env python3
"""
Calculator CLI Deployment Script
Creates a standalone executable for distribution with build system choice
"""

import os
import sys
import subprocess
import shutil
import platform
import argparse

def run_command(command, check=True):
    """Run a command and handle errors."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if check:
            sys.exit(1)
        return e

def check_build_tools():
    """Check which build tools are available."""
    has_make = shutil.which("make") is not None
    has_cmake = shutil.which("cmake") is not None
    has_gcc = shutil.which("gcc") or shutil.which("cc") is not None
    
    return {
        "make": has_make,
        "cmake": has_cmake,
        "gcc": has_gcc
    }

def choose_build_system(build_tools):
    """Let user choose between available build systems."""
    available_systems = []
    
    if build_tools["make"] and build_tools["gcc"]:
        available_systems.append(("make", "Make (traditional build system)"))
    
    if build_tools["cmake"] and build_tools["gcc"]:
        available_systems.append(("cmake", "CMake (modern build system)"))
    
    if not available_systems:
        print("ERROR: No suitable build system found!")
        print("Please install one of the following:")
        print("  - Make + GCC")
        print("  - CMake + GCC")
        sys.exit(1)
    
    if len(available_systems) == 1:
        system, description = available_systems[0]
        print(f"Using {description} (only available option)")
        return system
    
    print("\nAvailable build systems:")
    for i, (system, description) in enumerate(available_systems, 1):
        print(f"  {i}. {description}")
    
    while True:
        try:
            choice = input(f"\nChoose build system (1-{len(available_systems)}): ").strip()
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(available_systems):
                system, description = available_systems[choice_idx]
                print(f"Selected: {description}")
                return system
            else:
                print(f"Please enter a number between 1 and {len(available_systems)}")
        except (ValueError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            sys.exit(1)

def build_with_make():
    """Build C library using Make."""
    print("Building C library with Make...")
    run_command("make clean", check=False)
    run_command("make")
    
    # Check if library was created
    lib_extensions = ["dll", "so", "dylib"]
    for ext in lib_extensions:
        lib_path = f"c_src/calculate.{ext}"
        if os.path.exists(lib_path):
            print(f"✅ C library built: {lib_path}")
            return lib_path
    
    raise FileNotFoundError("C library not found after Make build")

def build_with_cmake():
    """Build C library using CMake."""
    print("Building C library with CMake...")
    
    # Create build directory
    build_dir = "build"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)
      # Configure with CMake
    run_command(f"cmake -B {build_dir} -S . -DSKIP_PYTHON_INSTALL=ON")
    
    # Build with CMake
    run_command(f"cmake --build {build_dir}")
    
    # CMake puts the library in build/c_src/ directory
    # Look for the DLL in the CMake output directory structure
    lib_extensions = ["dll", "so", "dylib"]
    
    # CMake build output locations
    search_paths = [
        f"{build_dir}/c_src",           # Primary CMake output location
        f"{build_dir}/c_src/Debug",     # Debug build
        f"{build_dir}/c_src/Release",   # Release build
        f"{build_dir}/Debug",           # Alternative Debug location
        f"{build_dir}/Release"          # Alternative Release location
    ]
    
    for search_path in search_paths:
        for ext in lib_extensions:
            # Look for libcalculate.dll (the name CMake creates)
            lib_path = f"{search_path}/libcalculate.{ext}"
            if os.path.exists(lib_path):
                print(f"✅ C library built: {lib_path}")
                return lib_path
    
    raise FileNotFoundError("C library not found after CMake build")

def get_library_binary_for_pyinstaller():
    """Get the appropriate library file for PyInstaller --add-binary."""
    if platform.system() == "Windows":
        lib_file = "libcalculate.dll"  # Changed to match what Python code expects
    elif platform.system() == "Darwin":
        lib_file = "libcalculate.dylib"
    else:  # Linux and others
        lib_file = "libcalculate.so"
    
    lib_path = f"c_src/{lib_file}"
    if not os.path.exists(lib_path):
        # Try alternative naming
        alt_files = ["libcalculate.dll", "calculate.dll", "libcalculate.so", "libcalculate.dylib"]
        for alt_file in alt_files:
            alt_path = f"c_src/{alt_file}"
            if os.path.exists(alt_path):
                lib_path = alt_path
                lib_file = alt_file
                break
    
    if not os.path.exists(lib_path):
        raise FileNotFoundError(f"No suitable library file found in c_src/")
    
    return lib_path, lib_file

def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(
        description="Calculator CLI Deployment Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deploy.py                    # Interactive mode (choose build system)
  python deploy.py --build-system make    # Use Make
  python deploy.py --build-system cmake   # Use CMake
  python deploy.py --no-interactive       # Auto-select build system
        """
    )
    
    parser.add_argument(
        "--build-system", "-b",
        choices=["make", "cmake"],
        help="Force use of specific build system"
    )
    
    parser.add_argument(
        "--no-interactive", "-n",
        action="store_true",
        help="Auto-select build system without prompting"
    )
    
    parser.add_argument(
        "--clean-only", "-c",
        action="store_true",
        help="Only clean build artifacts and exit"
    )
    
    args = parser.parse_args()
    
    print("=== Calculator CLI Deployment ===")
    print(f"Platform: {platform.system()}")
    
    # Ensure we're in the right directory
    if not os.path.exists("setup.py"):
        print("ERROR: Run this script from the project root directory")
        sys.exit(1)
    
    # Clean previous builds
    print("Cleaning previous builds...")
    for item in ["build", "dist", "__pycache__"]:
        if os.path.exists(item):
            shutil.rmtree(item, ignore_errors=True)
    
    # Clean compiled Python files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".pyc", ".pyo")):
                os.remove(os.path.join(root, file))
    
    if args.clean_only:
        print("✅ Build artifacts cleaned!")
        return 0
    
    # Check available build tools
    print("Checking available build tools...")
    build_tools = check_build_tools()
    
    print(f"Make available: {'✅' if build_tools['make'] else '❌'}")
    print(f"CMake available: {'✅' if build_tools['cmake'] else '❌'}")
    print(f"GCC available: {'✅' if build_tools['gcc'] else '❌'}")
    
    if not build_tools["gcc"]:
        print("ERROR: GCC not found. Please install a C compiler.")
        sys.exit(1)
    
    # Choose build system
    if args.build_system:
        build_system = args.build_system
        if build_system == "make" and not build_tools["make"]:
            print("ERROR: Make not available but requested")
            sys.exit(1)
        elif build_system == "cmake" and not build_tools["cmake"]:
            print("ERROR: CMake not available but requested")
            sys.exit(1)
        print(f"Using specified build system: {build_system}")
    elif args.no_interactive:
        # Auto-select: prefer CMake if available, fallback to Make
        if build_tools["cmake"]:
            build_system = "cmake"
            print("Auto-selected: CMake")
        elif build_tools["make"]:
            build_system = "make"
            print("Auto-selected: Make")
        else:
            print("ERROR: No suitable build system found")
            sys.exit(1)
    else:
        # Interactive mode
        build_system = choose_build_system(build_tools)
    
    # Build C library
    try:
        if build_system == "make":
            lib_path = build_with_make()
        else:  # cmake
            lib_path = build_with_cmake()
    except Exception as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)
    
    # Install PyInstaller if not available
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        run_command("pip install pyinstaller")
    
    # Get library file for PyInstaller
    try:
        lib_path, lib_file = get_library_binary_for_pyinstaller()
        print(f"Using library for packaging: {lib_path}")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    # Create standalone executable
    print("Creating standalone executable...")
    exe_name = "calculator-cli"
    if platform.system() == "Windows":
        exe_name += ".exe"
      # Build PyInstaller command
    separator = ";" if platform.system() == "Windows" else ":"
    
    # Find calculator_c module path
    calculator_c_path = None
    venv_path = os.environ.get("VIRTUAL_ENV")
    if venv_path:
        calculator_c_path = os.path.join(venv_path, "Lib", "site-packages", "calculator_c")
    
    cmd = f'pyinstaller --onefile --console --name {exe_name} python/cli.py --add-binary "{lib_path}{separator}." --clean'
    
    # Add calculator_c module if found
    if calculator_c_path and os.path.exists(calculator_c_path):
        cmd += f' --add-data "{calculator_c_path}{separator}calculator_c"'
        print(f"Including calculator_c module from: {calculator_c_path}")
    else:
        print("WARNING: calculator_c module not found - executable may not work properly")
    
    run_command(cmd)
    
    # Verify executable was created
    exe_path = f"dist/{exe_name}"
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path)
        print(f"✅ Standalone executable created: {exe_path} ({size:,} bytes)")
        print("\n=== Deployment Complete ===")
        print(f"Your executable is ready at: {exe_path}")
        print("You can distribute this file to run on any compatible system.")
        
        # Test the executable
        print("\nTesting executable...")
        test_result = run_command(f'"{exe_path}" "2+2"', check=False)
        if test_result.returncode == 0:
            print("✅ Executable test passed!")
        else:
            print("⚠️  Executable test failed, but binary was created")
    else:
        print("❌ Failed to create executable")
        sys.exit(1)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

# This script formats all C source and header files in the project using clang-format.
# It is intended to be used as a pre-commit hook or manually before pushing code.

# Usage (from project root):
#   bash scripts/format_c_code.sh

find ./c_src ./tests_c -type f \( -name '*.c' -o -name '*.h' \) -exec clang-format -i --style=file {} +

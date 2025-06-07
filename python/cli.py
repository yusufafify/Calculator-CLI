import argparse
import sys
from . import Calculator


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="CLI Calculator")
    parser.add_argument(
        "expression", nargs="?", help="Mathematical expression to evaluate"
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive mode"
    )

    args = parser.parse_args()
    calc = Calculator()

    if args.interactive or not args.expression:
        interactive_mode(calc)
    else:
        try:
            result = calc.calculate(args.expression)
            print(f"{args.expression} = {result}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


def interactive_mode(calc: Calculator):
    """Run calculator in interactive mode."""
    print("Calculator - Interactive Mode")
    print("Enter expressions like '2 + 3' or 'quit' to exit")

    while True:
        try:
            expression = input("> ").strip()
            if expression.lower() in ["quit", "exit", "q"]:
                break
            if not expression:
                continue

            result = calc.calculate(expression)
            print(f"= {result}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

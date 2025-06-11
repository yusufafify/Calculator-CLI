import argparse
import sys
import os

# Handle both package import and standalone execution
try:
    from . import Calculator
except ImportError:
    # Add parent directory to path for standalone execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from python import Calculator


def main():
    """Main CLI function."""
    try:
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
                sys.stdout.flush()
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.stderr.flush()
                sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


def interactive_mode(calc):
    """Run calculator in interactive mode."""
    print("Calculator CLI - Interactive Mode")
    print("Enter mathematical expressions or 'quit' to exit")
    print("Examples: 2 + 3, 10 * 5, 20 / 4")
    print("-" * 40)

    while True:
        try:
            expr = input("calc> ").strip()

            if expr.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            if not expr:
                continue

            result = calc.calculate(expr)
            print(f"= {result}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

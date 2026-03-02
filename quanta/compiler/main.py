import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Quanta Compiler")
    parser.add_argument("file", help="Quanta source file to compile")
    args = parser.parse_args()

    print(f"Compiling {args.file}...")
    # TODO: Implement compiler pipeline

if __name__ == "__main__":
    main()

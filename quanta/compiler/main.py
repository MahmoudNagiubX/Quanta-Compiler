from __future__ import annotations
import argparse
from pathlib import Path
import sys
from .lexer.lexer import Lexer
from .parser.parser import Parser
from .semantic_analysis.analyser import SemanticAnalyzer

def compile_source(source: str):
    """
    Run the current front-end pipeline.

    Stages:
    1. Lexer  -> convert source text into tokens
    2. Parser -> convert tokens into AST
    3. Semantic analyzer -> check meaning, scopes, and types
    """
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    semantic_result = SemanticAnalyzer().analyze(ast)
    return tokens, ast, semantic_result


def build_cli() -> argparse.ArgumentParser:
    """
    Build command-line interface for the compiler driver.
    """
    parser = argparse.ArgumentParser(description="Quanta compiler front-end driver")
    parser.add_argument("file", help="Path to Quanta source file")
    parser.add_argument("--show-tokens", action="store_true", help="Print lexer tokens")
    parser.add_argument("--show-ast", action="store_true", help="Print parsed AST")
    return parser


def main(argv: list[str] | None = None) -> int:
    """
    CLI entry point.

    Returns:
    - 0 if compilation front-end succeeds
    - 1 if there is an error
    """
    parser = build_cli()
    args = parser.parse_args(argv)

    source_path = Path(args.file)
    if not source_path.exists():
        print(f"Error: file not found: {source_path}", file=sys.stderr)
        return 1

    source = source_path.read_text(encoding="utf-8")

    try:
        tokens, ast, semantic_result = compile_source(source)
    except Exception as exc:
        # Lexer and parser errors will end up here.
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Compiling {source_path}...")

    if args.show_tokens:
        print("\nTOKENS:")
        for token in tokens:
            print(token)

    if args.show_ast:
        print("\nAST:")
        for node in ast:
            print(node)

    if semantic_result.ok:
        print("\nSemantic analysis: OK")
        return 0

    print("\nSemantic analysis: FAILED")
    for error in semantic_result.errors:
        print(error)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
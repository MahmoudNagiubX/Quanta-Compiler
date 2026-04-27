from __future__ import annotations
import argparse
from pathlib import Path
import sys
from .lexer.lexer import Lexer
from .lexer.token import LexerError
from .parser.errors import ParseError
from .parser.parser import Parser
from .semantic_analysis.analyser import SemanticAnalyzer
from .semantic_analysis.errors import SemanticError
from .errors.error_reporter import format_error
from .interpreter.interpreter import Interpreter
from .ir.ir_generator import IRGenerator
from .ir.optimizer import IROptimizer

COMMANDS = ("tokens", "ast", "ir", "run")


def build_command_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Quanta compiler front-end driver")
    subparsers = parser.add_subparsers(dest="command", metavar="command")

    tokens_parser = subparsers.add_parser("tokens", help="Run lexer and print tokens")
    tokens_parser.add_argument("file", help="Path to Quanta source file")

    ast_parser = subparsers.add_parser("ast", help="Run lexer and parser and print AST")
    ast_parser.add_argument("file", help="Path to Quanta source file")

    ir_parser = subparsers.add_parser("ir", help="Run full pipeline and print IR")
    ir_parser.add_argument("file", help="Path to Quanta source file")
    ir_parser.add_argument("--optimize", action="store_true", help="Optimize IR output")

    run_parser = subparsers.add_parser("run", help="Run semantic analysis")
    run_parser.add_argument("file", help="Path to Quanta source file")

    return parser


def build_legacy_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("file", nargs="?", help="Path to Quanta source file")
    parser.add_argument("--show-tokens", action="store_true", help="Print lexer tokens")
    parser.add_argument("--show-ast", action="store_true", help="Print parsed AST")
    parser.add_argument("--show-ir", action="store_true", help="Print generated IR")
    parser.add_argument("--optimize", action="store_true", help="Optimize IR output")
    return parser


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


def main(argv: list[str] | None = None) -> int:
    """
    CLI entry point.

    Returns:
    - 0 if compilation front-end succeeds
    - 1 if there is an error
    """
    args_list = argv if argv is not None else sys.argv[1:]

    if args_list and args_list[0] in COMMANDS:
        parser = build_command_cli()
        args = parser.parse_args(args_list)
        command = args.command
        file_path = args.file
    elif args_list and args_list[0].endswith(".qn"):
        command = "run"
        file_path = args_list[0]
    else:
        legacy_parser = build_legacy_cli()
        args = legacy_parser.parse_args(args_list)

        if args.file is None:
            build_command_cli().print_help()
            return 1

        if args.show_tokens:
            command = "tokens"
        elif args.show_ast:
            command = "ast"
        elif args.show_ir:
            command = "ir"
        else:
            command = "run"

        file_path = args.file

    source_path = Path(file_path)
    if not source_path.exists():
        print(f"Error: file not found: {source_path}", file=sys.stderr)
        return 1

    source = source_path.read_text(encoding="utf-8-sig")

    if command == "tokens":
        try:
            tokens = Lexer(source).tokenize()
        except LexerError as exc:
            print(format_error(source, "LexerError", exc.message, exc.line, exc.column))
            return 1

        print("TOKENS:")
        for token in tokens:
            print(token)
        return 0

    if command == "ast":
        try:
            tokens = Lexer(source).tokenize()
            ast = Parser(tokens).parse()
        except LexerError as exc:
            print(format_error(source, "LexerError", exc.message, exc.line, exc.column))
            return 1
        except ParseError as exc:
            print(format_error(source, "ParseError", exc.message, exc.line, exc.column, hint=exc.hint))
            return 1

        print("AST:")
        for node in ast:
            print(node)
        return 0

    try:
        tokens, ast, semantic_result = compile_source(source)
    except LexerError as exc:
        print(format_error(source, "LexerError", exc.message, exc.line, exc.column))
        return 1
    except ParseError as exc:
        print(format_error(source, "ParseError", exc.message, exc.line, exc.column, hint=exc.hint))
        return 1
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if command == "ir":
        print("IR:")
        ir = IRGenerator().generate(ast)
        if getattr(args, "optimize", False):
            ir = IROptimizer().optimize(ir)
        for instr in ir:
            print(instr)
        if semantic_result.ok:
            print("\nSemantic analysis: OK")
            return 0
        print("\nSemantic analysis: FAILED")
        for error in semantic_result.errors:
            print(format_error(source, "SemanticError", error.message, error.line, error.column, hint=error.message))
            print()
        return 1

    if command == "run":
        if not semantic_result.ok:
            print("Semantic analysis: FAILED")
            for error in semantic_result.errors:
                print(format_error(source, "SemanticError", error.message, error.line, error.column, hint=error.message))
                print()
            return 1

        try:
            Interpreter().interpret(ast)
            return 0
        except Exception as exc:
            print(str(exc), file=sys.stderr)
            return 1

    build_command_cli().print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
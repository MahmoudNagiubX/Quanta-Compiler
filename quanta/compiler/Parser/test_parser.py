from quanta.compiler.lexer.lexer import Lexer
from quanta.compiler.parser.parser import Parser
from quanta.compiler.parser.ast_nodes import FunctionDecl, ReturnStmt, VarDecl


def parse_source(source: str):
    tokens = Lexer(source).tokenize()
    return Parser(tokens).parse()


def test_parse_typed_function():
    source = """
    rakm add(rakm a, rakm b) {
        raga3 a + b;
    }
    """
    ast = parse_source(source)

    assert len(ast) == 1
    fn = ast[0]
    assert isinstance(fn, FunctionDecl)
    assert fn.return_type.lexeme == "rakm"
    assert fn.name.lexeme == "add"
    assert len(fn.params) == 2
    assert isinstance(fn.body[0], ReturnStmt)


def test_parse_void_function():
    source = """
    wasfa main() {
        rakm x = 5;
    }
    """
    ast = parse_source(source)

    assert len(ast) == 1
    fn = ast[0]
    assert isinstance(fn, FunctionDecl)
    assert fn.return_type.lexeme == "wasfa"
    assert fn.name.lexeme == "main"
    assert isinstance(fn.body[0], VarDecl)
from quanta.compiler.lexer.lexer import Lexer
from quanta.compiler.parser.parser import Parser
from quanta.compiler.parser.ast_nodes import (
    FunctionDecl,
    VarDecl,
    PrintStmt,
    IfStmt,
    ReturnStmt,
)
def parse_source(source: str):
    tokens = Lexer(source).tokenize()
    parser = Parser(tokens)
    return parser.parse()

def test_parse_function_declaration():
    source = """
    wasfa add(rakm a, rakm b) {
        raga3 a + b;
    }
    """

    ast = parse_source(source)

    assert len(ast) == 1
    assert isinstance(ast[0], FunctionDecl)
    assert ast[0].name.lexeme == "add"
    assert len(ast[0].params) == 2
    assert ast[0].params[0].param_type.lexeme == "rakm"
    assert ast[0].params[0].name.lexeme == "a"
    assert ast[0].params[1].name.lexeme == "b"
    assert isinstance(ast[0].body[0], ReturnStmt)


def test_parse_variable_declaration():
    source = "rakm x = 5;"
    ast = parse_source(source)

    assert len(ast) == 1
    assert isinstance(ast[0], VarDecl)
    assert ast[0].var_type.lexeme == "rakm"
    assert ast[0].name.lexeme == "x"
    assert ast[0].initializer is not None


def test_parse_print_statement():
    source = 'etba3("hello");'
    ast = parse_source(source)

    assert len(ast) == 1
    assert isinstance(ast[0], PrintStmt)


def test_parse_if_statement():
    source = """
    law (eshta) {
        etba3("yes");
    }
    tb law (fakes) {
        etba3("no");
    }
    ay haga {
        etba3("done");
    }
    """

    ast = parse_source(source)

    assert len(ast) == 1
    assert isinstance(ast[0], IfStmt)
    assert ast[0].else_branch is not None
    assert len(ast[0].elif_branches) == 1


if __name__ == "__main__":
    print("Running parser smoke test...")
    program = """
    wasfa main() {
        rakm x = 10;
        law (x > 5) {
            etba3("big");
        }
        raga3 x;
    }
    """
    ast = parse_source(program)
    print("Parsed successfully ✅")
    print(ast)
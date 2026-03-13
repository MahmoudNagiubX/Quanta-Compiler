from quanta.compiler.lexer.lexer import Lexer
from quanta.compiler.parser.parser import Parser
from quanta.compiler.semantic_analysis.analyser import SemanticAnalyzer

def analyze_source(source: str):
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    result = SemanticAnalyzer().analyze(ast)
    return result

def test_valid_program():
    source = """
    wasfa add(rakm a, rakm b) {
        raga3 a + b;
    }

    wasfa main() {
        rakm x = 5;
        rakm y = add(x, 2);
        law (eshta) {
            etba3("ok");
        }
    }
    """
    result = analyze_source(source)
    assert result.ok


def test_type_mismatch():
    source = """
    wasfa main() {
        rakm x = "hello";
    }
    """
    result = analyze_source(source)
    assert not result.ok
    assert len(result.errors) > 0


def test_undeclared_variable():
    source = """
    wasfa main() {
        rakm x = y + 1;
    }
    """
    result = analyze_source(source)
    assert not result.ok
    assert any("undeclared" in error.message.lower() for error in result.errors)


def test_wrong_argument_count():
    source = """
    wasfa add(rakm a, rakm b) {
        raga3 a + b;
    }

    wasfa main() {
        rakm x = add(1);
    }
    """
    result = analyze_source(source)
    assert not result.ok
    assert any("expects" in error.message.lower() for error in result.errors)
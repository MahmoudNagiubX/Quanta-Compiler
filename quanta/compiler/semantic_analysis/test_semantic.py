from quanta.compiler.lexer.lexer import Lexer
from quanta.compiler.parser.parser import Parser
from quanta.compiler.semantic_analysis.analyser import SemanticAnalyzer


def analyze_source(source: str):
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    return SemanticAnalyzer().analyze(ast)


def test_valid_typed_return():
    source = """
    rakm add(rakm a, rakm b) {
        raga3 a + b;
    }
    """
    result = analyze_source(source)
    assert result.ok


def test_wrong_return_type():
    source = """
    rakm add(rakm a, rakm b) {
        raga3 "hello";
    }
    """
    result = analyze_source(source)
    assert not result.ok
    assert any("should return" in e.message.lower() for e in result.errors)


def test_missing_return_value():
    source = """
    rakm add(rakm a, rakm b) {
        raga3;
    }
    """
    result = analyze_source(source)
    assert not result.ok
    assert any("must return a value" in e.message.lower() for e in result.errors)


def test_void_function_returning_value():
    source = """
    wasfa main() {
        raga3 5;
    }
    """
    result = analyze_source(source)
    assert not result.ok
    assert any("void function" in e.message.lower() for e in result.errors)


def test_void_function_plain_return():
    source = """
    wasfa main() {
        raga3;
    }
    """
    result = analyze_source(source)
    assert result.ok
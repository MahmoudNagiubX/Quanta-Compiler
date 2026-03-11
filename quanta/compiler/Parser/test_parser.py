from quanta.compiler.Lexer.lexer import Lexer
from quanta.compiler.Parser.parser import Parser

source_code = """
rakm x = 5;
fatafet y = 3.14;
kalam msg = "hello";

etba3(x);

law (x > 3) {
    etba3(msg);
}

khalik (x > 0) {
    x = x - 1;
}

wasfa add(a, b) {
    raga3 a + b;
}
"""

# 1. Lexing
lexer = Lexer(source_code)
tokens = lexer.tokenize()

print("TOKENS:")
for token in tokens:
    print(token)

print("\n" + "=" * 50 + "\n")

# 2. Parsing
parser = Parser(tokens)
ast = parser.parse()

print("AST:")
for node in ast:
    print(node)
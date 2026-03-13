from quanta.compiler.lexer.lexer import Lexer
from quanta.compiler.lexer.token import TokenType

def dump_types(source: str) -> list[TokenType]:
    return [token.type for token in Lexer(source).tokenize()]

if __name__ == "__main__":
    source_code = '''
    wasfa main() {
        ya_ah_ya_la ready = eshta;
        law (ready) {
            etba3("Ahlan");
        }
        tb law (fakes) {
            etba3("La2");
        }
        ay haga {
            etba3("Done");
        }
    }
    '''

    print("Scanning Quanta code...")
    for token in Lexer(source_code).tokenize():
        print(f"Type: {token.type.name:<15} | Lexeme: {token.lexeme!r}")

    expected_prefix = [
        TokenType.WASFA,
        TokenType.IDENTIFIER,
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.LBRACE,
    ]

    assert dump_types(source_code)[:5] == expected_prefix
    print("\nBasic lexer smoke test passed.")
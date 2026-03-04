from quanta.compiler.Lexer.lexer import Lexer

# 1️⃣ Write some Egyptian Quanta code!
source_code = """
hewar main() {
    law (eshta) {
        sam3na(100);
    }
}
"""

# 2️⃣ Give the code to our Lexer
print("🚀 Scanning Egyptian code....")
lexer = Lexer(source_code)
tokens = lexer.tokenize()

# 3️⃣ Print out all the tokens it found
for token in tokens:
    print(f"Type: {token.type.name:<20} | Lexeme: '{token.lexeme}'")
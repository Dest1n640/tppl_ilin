import sys 
from enum import Enum

class ErrorType(Enum):
    LEXICAL = "lexical"
    SYNTAX = "syntax"  # На будущее: синтаксический анализ.
    SEMANTIC = "semantic"  # На будущее: проверка смысла программы.
    RUNTIME = "runtime"  # На будущее: ошибки выполнения программы.
    FILE = "file"  # На будущее: ошибки чтения файла.
    


class TokenizerError(Exception):
    def __init__(self, file_name: str, row: int, col: int,
                 error_type: ErrorType, message: str):
        self.file_name = file_name
        self.row = row
        self.col = col
        self.error_type = error_type
        self.message = message
        super().__init__(f"{file_name}:{row}:{col}: {error_type.value}: {message}")

class Tokenizer:
    def __init__(self, stdin_file: str, file_name: str = "<input>"):
        self.stdin_file = stdin_file
        self.file_name = file_name
        self.ind = 0
        self.col = 1
        self.row = 1
        self.key_words = {"if", "else", "while", "return", "for", "def"}
        self.operator = {"+", "-", "*", "/", "=", "<", ">", "==", "<=", ">="}
        self.delimiters = {"(", ")", "{", "}", ",", ";"}

    def read_identifier(self):
        start = self.ind
        start_col = self.col
        while self.ind < len(self.stdin_file):
            current = self.stdin_file[self.ind]
            if not (current.isalnum() or current == "_"):
                break
            self.ind += 1
            self.col += 1
        identifier = self.stdin_file[start:self.ind]
        token_type = "KEYWORD" if identifier in self.key_words else "IDENT"
        return f"({token_type}, {identifier}, {self.row}:{start_col})"

    def read_number(self):
        num = ""
        start_col = self.col
        while self.ind < len(self.stdin_file) and (
            self.stdin_file[self.ind].isdigit() or self.stdin_file[self.ind] == "."
        ):
            if self.stdin_file[self.ind] == "." and "." in num:
                break
            num += self.stdin_file[self.ind]
            self.ind += 1
            self.col += 1
        token_type = "FLOAT" if "." in num else "INT"
        return f"({token_type}, {num}, {self.row}:{start_col})"

    def read_string(self):
        string = ""
        start_col = self.col
        self.ind += 1
        self.col += 1
        while self.ind < len(self.stdin_file) and self.stdin_file[self.ind] not in '"\r\n':
            string += self.stdin_file[self.ind]
            self.ind += 1
            self.col += 1
        if self.ind == len(self.stdin_file) or self.stdin_file[self.ind] != '"':
            raise TokenizerError(
                self.file_name, self.row, start_col, ErrorType.LEXICAL,
                "unterminated string literal",
            )
        self.ind += 1
        self.col += 1
        return f"(STRING, {string}, {self.row}:{start_col})"
            

    def read_operator(self):
        start_col = self.col
        operator = self.stdin_file[self.ind:self.ind + 2]
        if operator not in self.operator:
            operator = self.stdin_file[self.ind]
        self.ind += len(operator)
        self.col += len(operator)
        return f"(OP, {operator}, {self.row}:{start_col})"

    def read_delimeter(self):
        start_col = self.col
        delimeter = self.stdin_file[self.ind]
        self.ind += 1
        self.col += 1
        return f"(SEP, {delimeter}, {self.row}:{start_col})"
                
    def tokenizer(self):
        tokens = []
        while self.ind < len(self.stdin_file):
            current = self.stdin_file[self.ind]
            if current in " \t\r\n":
                self.ind += 1
                if current == "\n":
                    self.row += 1
                    self.col = 1
                else:
                    self.col += 1
            elif current.isalpha() or current == "_":
                tokens.append(self.read_identifier())
            elif current.isdigit():
                tokens.append(self.read_number())
            elif current == '"':
                tokens.append(self.read_string())
            elif current in self.operator:
                tokens.append(self.read_operator())
            elif current in self.delimiters:
                tokens.append(self.read_delimeter())
            elif current == "#":
                while self.ind < len(self.stdin_file) and self.stdin_file[self.ind] != "\n":
                    self.ind += 1
                    self.col += 1
            else:
                raise TokenizerError(
                    self.file_name, self.row, self.col, ErrorType.LEXICAL,
                    f"unexpected character {current!r}",
                )
        return tokens


if __name__ == "__main__":
    file_name = sys.argv[1]
    try:
        with open(file_name, encoding="utf-8") as source_file:
            source = source_file.read()
    except (OSError, UnicodeError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)

    tokenizer = Tokenizer(source, file_name)
    try:
        for token in tokenizer.tokenizer():
            print(token)
    except TokenizerError as error:
        print(error, file=sys.stderr)
        sys.exit(1)

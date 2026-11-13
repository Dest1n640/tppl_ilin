import pytest

from main import Tokenizer, TokenizerError


@pytest.mark.parametrize(
    "source, expected",
    [
        ("", []),
        (" \t\n", []),
        ("# comment", []),
        ("name", ["(IDENT, name, 1:1)"]),
        ("_name2", ["(IDENT, _name2, 1:1)"]),
        ("if_count", ["(IDENT, if_count, 1:1)"]),
        ("if", ["(KEYWORD, if, 1:1)"]),
        ("else", ["(KEYWORD, else, 1:1)"]),
        ("while", ["(KEYWORD, while, 1:1)"]),
        ("return", ["(KEYWORD, return, 1:1)"]),
        ("for", ["(KEYWORD, for, 1:1)"]),
        ("def", ["(KEYWORD, def, 1:1)"]),
        ("0", ["(INT, 0, 1:1)"]),
        ("123", ["(INT, 123, 1:1)"]),
        ("12.5", ["(FLOAT, 12.5, 1:1)"]),
        ('"php suck"', ["(STRING, php suck, 1:1)"]),
        ('""', ["(STRING, , 1:1)"]),
        ('"#"', ["(STRING, #, 1:1)"]),
        ("+", ["(OP, +, 1:1)"]),
        ("-", ["(OP, -, 1:1)"]),
        ("*", ["(OP, *, 1:1)"]),
        ("/", ["(OP, /, 1:1)"]),
        ("=", ["(OP, =, 1:1)"]),
        ("<", ["(OP, <, 1:1)"]),
        (">", ["(OP, >, 1:1)"]),
        ("==", ["(OP, ==, 1:1)"]),
        ("<=", ["(OP, <=, 1:1)"]),
        (">=", ["(OP, >=, 1:1)"]),
        ("(", ["(SEP, (, 1:1)"]),
        (")", ["(SEP, ), 1:1)"]),
        ("{", ["(SEP, {, 1:1)"]),
        ("}", ["(SEP, }, 1:1)"]),
        (",", ["(SEP, ,, 1:1)"]),
        (";", ["(SEP, ;, 1:1)"]),
        ("x=2", ["(IDENT, x, 1:1)", "(OP, =, 1:2)", "(INT, 2, 1:3)"]),
        ("x<=2", ["(IDENT, x, 1:1)", "(OP, <=, 1:2)", "(INT, 2, 1:4)"]),
        ("x # comment\ny", ["(IDENT, x, 1:1)", "(IDENT, y, 2:1)"]),
        (" \tx\r\n  y", ["(IDENT, x, 1:3)", "(IDENT, y, 2:3)"]),
        ('"a" x', ["(STRING, a, 1:1)", "(IDENT, x, 1:5)"]),
        ("(x)", ["(SEP, (, 1:1)", "(IDENT, x, 1:2)", "(SEP, ), 1:3)"]),
    ],
)
def test_tokenizer(source, expected):
    assert Tokenizer(source).tokenizer() == expected


@pytest.mark.parametrize(
    "source, message",
    [
        ("a @ b", "input.txt:1:3: lexical: unexpected character '@'"),
        ("a\n  !", "input.txt:2:3: lexical: unexpected character '!'"),
        ("1.2.3", "input.txt:1:4: lexical: unexpected character '.'"),
        ('"unfinished', "input.txt:1:1: lexical: unterminated string literal"),
        ('  "text\n', "input.txt:1:3: lexical: unterminated string literal"),
    ],
)
def test_tokenizer_errors(source, message):
    with pytest.raises(TokenizerError) as error:
        Tokenizer(source, "input.txt").tokenizer()
    assert str(error.value) == message

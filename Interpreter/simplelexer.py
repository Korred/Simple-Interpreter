# simple Python-like lexer
# Follows PEP 8 but ignores E501 (line too long)

from rply import LexerGenerator
from rply.token import Token


def group(*choices, **namegroup):
    choices = list(choices)
    for name, value in namegroup.items():
        choices.append("(?P<%s>%s)" % (name, value))
    return '(' + '|'.join(choices) + ')'


def any(*choices):
    result = group(*choices) + '*'
    return result


def maybe(*choices):
    return group(*choices) + '?'

# Regex to select different tokens

Number = r'(?<![\.\d])(([+-])?[1-9][0-9]*)(?![\.\d])|(?<![\.\d])0(?![\.\d])'
Float = r'[-+]?([0-9]+[.][0-9]+)'
Boolean = r'(True|False)'


# ' or " string.
def make_single_string(delim):
    normal_chars = r"[^\n\%s]*" % (delim, )
    return "".join([delim, normal_chars,
                    any(r"\\." + normal_chars), delim])


String = group(make_single_string(r"\'"), make_single_string(r'\"'))

# ____________________________________________________________
# Stuff that should be ignored - stored as Ignore Token...

Whitespace = r'[ \f\t]'
Newline = r'\r?\n'
Linecontinue = r'\\' + Newline
Comment = r'#[^\r\n]*'
Indent = Newline + any(Whitespace)
Ignore = group(Whitespace + '+', Linecontinue, Comment)

# ____________________________________________________________

Name = r'[a-zA-Z_][a-zA-Z0-9_]*'
PrimitiveName = '\\$' + Name

Colon = r'\:'
Comma = r'\,'
Assign = r'\='

# ( and ) token
OpenBracket = r'[\(]'
CloseBracket = r'[\)]'

# [ and ] token for lists/arrays
ListOpenBracket = r'[\[]'
ListCloseBracket = r'[\]]'

# { and } token for dicts/maps
MapOpenBracket = r'[\{]'
MapCloseBracket = r'[\}]'

If = r'if'
Else = r'else'
While = r'while'
Def = r'def'
Object = r'object'

# Tokens used in parser rules
tokens = ["If", "Else", "While", "Def", "Object", "Boolean",
          "Number", "String", "Ignore", "Indent", "OpenBracket",
          "CloseBracket", "Comma", "Assign", "Colon", "Name",
          "PrimitiveName", "Float", "ListOpenBracket", "ListCloseBracket",
          "MapOpenBracket", "MapCloseBracket"]


def make_lexer():
    lg = LexerGenerator()
    for token in tokens:
        print(token)
        lg.add(token, globals()[token])
    return lg.build()


lexer = make_lexer()

tabsize = 4


def postprocess(tokens, source):
    parenthesis_level = 0
    indentation_levels = [0]
    output_tokens = []
    tokens = [token for token in tokens if token.name != "Ignore"]
    token = None
    for i in range(len(tokens)):
        token = tokens[i]
        if token.name == "OpenBracket":
            parenthesis_level += 1
            output_tokens.append(token)
        elif token.name == "CloseBracket":
            parenthesis_level -= 1
            if parenthesis_level < 0:
                err = "unmatched parenthesis"
                raise LexerError(source, token.source_pos, err)
            output_tokens.append(token)
        elif token.name == "Indent":
            if i + 1 < len(tokens) and tokens[i + 1].name == "Indent":
                continue
            if parenthesis_level == 0:
                s = token.value
                length = len(s)
                pos = 0
                column = 0
                # the token looks like this: \r?\n[ \f\t]*
                if s[0] == '\n':
                    pos = 1
                    start = 1
                else:
                    pos = 2
                    start = 2
                # count the indentation depth of the whitespace
                while pos < length:
                    c = s[pos]
                    if c == ' ':
                        column = column + 1
                    elif c == '\t':
                        column = (column // tabsize + 1) * tabsize
                    elif c == '\f':
                        column = 0
                    pos = pos + 1
                # split the token in two: one for the newline and one for the
                # in/dedent
                output_tokens.append(Token("Newline",
                                           s[:start],
                                           token.source_pos))
                if column > indentation_levels[-1]:  # count indents or dedents
                    indentation_levels.append(column)
                    token.name = "Indent"
                    token.value = s[start:]
                    token.source_pos.idx += start
                    token.source_pos.lineno += 1
                    token.source_pos.colno = 0
                    output_tokens.append(token)
                else:
                    dedented = False
                    while column < indentation_levels[-1]:
                        dedented = True
                        indentation_levels.pop()
                        output_tokens.append(Token("Dedent",
                                                   "",
                                                   token.source_pos))
                    if dedented:
                        token.name = "Dedent"
                        token.value = s[start:]
                        token.source_pos.idx += start
                        token.source_pos.lineno += 1
                        token.source_pos.colno = 0
                        output_tokens[-1] = token
            else:
                pass  # implicit line-continuations within parenthesis
        else:
            output_tokens.append(token)
    if token is not None:
        output_tokens.append(Token("EOF", "", token.source_pos))
    return output_tokens


def lex(s):
    if not s.endswith('\n'):
        s += '\n'
    return list(postprocess(lexer.lex(s), s))

from Tokens import Token

whitespaces = [' ', '\t', '\n']

def main():
    #t = parse("var (){100}print")
    t = parse("var x = 5;\nvar y = x * 5;\nx = 17;\nif (x == 5) {\nprint(y);\n}\nprint(x);")
    print("Tokens: {}".format(t[0]))
    print("identifier_table: {}".format(t[1]))

def parse(raw):
    print("Input: \n{}\n\n".format(raw))
    tokens  = []
    idx = 0
    value_table = {}
    ite = iter(raw)
    try:
        c = next(ite, None)
        doNext = True
        while c is not None:
            doNext = True
            if c == '=':
                c = next(ite, None)
                doNext = False
                if (c == '='):
                    tokens.append((Token.EQ, 0))
                else:
                    tokens.append((Token.SETEQ, 0))
            elif c == '<':
                c = next(ite, None)
                doNext = False
                if (c == '='):
                    tokens.append((Token.LT, 0))
                else:
                    tokens.append((Token.LTE, 0))
            elif c == '>':
                c = next(ite, None)
                doNext = False
                if (c == '='):
                    tokens.append((Token.GT, 0))
                else:
                    tokens.append((Token.GTE, 0))
            elif c == '+':
                tokens.append((Token.ADD, 0))
            elif c == '-':
                tokens.append((Token.SUB, 0))
            elif c == '*':
                tokens.append((Token.MUL, 0))
            elif c == '/':
                tokens.append((Token.DIV, 0))
            elif c == '%':
                tokens.append((Token.MOD, 0))

            elif c == '(':
                tokens.append((Token.LP, 0))
            elif c == ')':
                tokens.append((Token.RP, 0))
            elif c == '{':
                tokens.append((Token.LB, 0))
            elif c == '}':
                tokens.append((Token.RB, 0))
            elif c == ';':
                tokens.append((Token.SEMICOLON, 0))
            elif isNumeric(c):
                res = untilNotNumeric(ite)
                w = c + res[0]
                c = res[1]
                doNext = False
                try:
                    i = int(w)
                    tokens.append((Token.NUM, w))
                except:
                    error("not a valid int literal: {}", w)
            elif isLowerAlphabetic(c):
                res = untilNotAlphaNumeric(ite)
                w = c + res[0]
                c = res[1]
                doNext = False
                if w == 'var':
                    if c != ' ':
                        error('expected space before identifier name {}', c)
                    else:
                        c = next(ite, None)
                        if not isLowerAlphabetic(c):
                            error('Error: invalid starting character for identifier {}', c)
                        res = getIdentifier(ite)
                        w = c
                        if res[0] is not None:
                            w += res[0]
                        c = res[1]
                        doNext = False
                        value_table[idx] = w
                        tokens.append((Token.VAR, idx))
                        idx += 1

                elif w == "print":
                    tokens.append((Token.PRINT, 0))
                elif w == 'read':
                    tokens.append((Token.READ, 0))
                elif w == 'if':
                    tokens.append((Token.IF, 0))
                elif w == 'while':
                    tokens.append((Token.WHILE,0 ))
                elif c is not None:
                    tokens.append((Token.IDENT, idx))
                    value_table[idx] = w
                    idx += 1
                    
                elif c is None:
                    break
        
            elif not c in whitespaces:
                error("Parsing Error: Character {}", c)
            

            if doNext:
                c = next(ite, None)
        tokens.append((Token.END, 0))
        return (tokens, value_table)
    except StopIteration:
        print("dont expect to get here")
        quit()

def getIdentifier(ite):
    c = next(ite, None)
    buf = c
    while isLowerAlphabetic(c) or isNumeric(c):
        buf += c
    return (buf, c)

def untilNotNumeric(ite):
    buf = ''
    c = next(ite, None)
    while isNumeric(c):
        buf += c
        c = next(ite, None)
    return (buf, c)

def untilNotAlphaNumeric(ite):
    buf = ''
    c = next(ite, None)
    while isNumeric(c) or isLowerAlphabetic(c):
        buf += c
        c = next(ite, None)
    return (buf, c)

def isNumeric(c):
    return c is not None and ord(c) >= 48 and ord(c) <= 57

def isLowerAlphabetic(c):
    return c is not None and ord(c) >= 97 and ord(c) <= 122

def error(msg, chars = []):
    print("Parse Error: {}".format(msg.format(chars)))
    quit()

if __name__ == '__main__':
    main()

# currently unused

def untilCharacters(ite, chars):
    buf = ''
    c = next(ite, None)
    while not c in [None, ' ', '\t']:
        buf += c
        c = next(ite, None)
    return buf

def untilWhiteSpace(ite):
    buf = ''
    c = next(ite, None)
    while not c in [None, ' ', '\t']:
        buf += c
        c = next(ite, None)
    return (buf, c)
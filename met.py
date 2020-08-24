from helping import *

tokentk = ""
current_position = 0
token = ""
linecounter = 0
tokenList = []
programName = ""
counter = -1

# scope
currentScope = 0
entities = [[]]
quads = []

# variables for checking Loops and Functions
inLoop = 0
exitQuad = -1
inFunction = 0
foundReturn = 0

characters, totalcharacters = getCodeFromFileAndCharacterLength()


#
#   ~~~~~~~~ ERROR ~~~~~~~~~
#

def error(message):
    global linecounter
    print(message)
    linecounter += 1
    print("in line :", linecounter)
    quit()


#
#   ~~~~~~~~ LEXER ~~~~~~~~~
#

def lexer():
    global counter
    counter += 1
    lex()


def lex():
    global current_position
    global token
    global tokentk
    global tokenList
    global linecounter

    token = characters[current_position]
    if characters[current_position] == '\n': linecounter += 1

    if token.isalpha():
        token, current_position = completeTokenIfIsAlpha(characters, current_position, totalcharacters)
        tokenList = appendToTokenList(token, tokenList)

    elif token.isdigit():
        token, current_position = completeTokenIfIsDigit(characters, current_position, totalcharacters)
        tokenList = checkDigitIfValidAndAddToList(token, tokenList)

    elif token == "/":
        if current_position == totalcharacters - 1:
            error("you can't use / at the end of the file")

        if characters[current_position + 1] == "/":
            tokentk = "linecommenttk"
            tokenList.append([tokentk, '//'])
            current_position += 1
            while (characters[current_position] != "\n"):
                if current_position == totalcharacters - 1: quit()
                current_position += 1
            linecounter += 1
            lexer()

        elif characters[current_position + 1] == "*":
            tokentk = "startcommenttk"
            tokenList.append([tokentk, '/*'])
            current_position += 2
            if current_position == totalcharacters:
                error("File reached it's end but your comment didn't")
            while characters[current_position] + characters[current_position + 1] != "*/":
                if characters[current_position] == '\n': linecounter += 1
                current_position += 1
                if current_position == totalcharacters - 1:  # elegxos gia eof gia na doume an kleinoun ta sxolia
                    error("File reached it's end but your comment didn't")
                if characters[current_position] + characters[current_position + 1] == "/*" \
                        or characters[current_position] + characters[current_position + 1] == "//":
                    error("You have to end a comment before starting a new one")
            if current_position == totalcharacters - 2:  # elegxos gia eof se periptwsh pou sto telos exei comment pou kleinei kanonika
                exit()
            current_position += 2
            lexer()
        elif characters[current_position + 1].isalpha() or characters[current_position + 1].isdigit() \
                or characters[current_position + 1] == " " or characters[current_position + 1] == "\t":
            tokentk = "divtk"
            tokenList.append([tokentk, '/'])
            current_position += 1
        else:
            error("invalid symbol: " + token)

    elif token == "+":
        tokentk = "plustk"
        tokenList.append([tokentk, '+'])
        current_position += 1

    elif token == "-":
        tokentk = "minustk"
        tokenList.append([tokentk, '-'])
        current_position += 1

    elif token == "*":
        tokentk = "multtk"
        tokenList.append([tokentk, '*'])
        current_position += 1

    elif token == "<":
        next_symbol = characters[current_position + 1]
        isAlphaOrDigit = next_symbol.isalpha() or next_symbol.isdigit()

        if next_symbol != '=' and next_symbol != '>' and not isAlphaOrDigit:
            error("invalid symbol: " + characters[current_position] + next_symbol)

        if next_symbol == "=":
            tokentk = "lessorequaltk"
            token = "<="
            tokenList.append([tokentk, token])
            current_position += 2

        if next_symbol == ">":
            tokentk = "differenttk"
            token = "<>"
            tokenList.append([tokentk, token])
            current_position += 2

        if next_symbol.isalpha() or next_symbol.isdigit():
            tokentk = "lesstk"
            tokenList.append([tokentk, '<'])
            current_position += 1

    elif token == ">":
        next_symbol = characters[current_position + 1]
        isAlphaOrDigit = next_symbol.isalpha() or next_symbol.isdigit()
        if not isAlphaOrDigit and next_symbol != '==':
            error("invalid symbol: " + characters[current_position] + next_symbol)
        if next_symbol == "=":
            tokentk = "moreorequaltk"
            token = ">="
            tokenList.append([tokentk, token])
            current_position += 2

        if next_symbol.isdigit() or next_symbol.isalpha():
            tokentk = "moretk"
            tokenList.append([tokentk, '>'])
            current_position += 1

    elif token == "=":
        next_symbol = characters[current_position + 1]
        isAlphaOrDigit = next_symbol.isalpha() or next_symbol.isdigit()
        if not isAlphaOrDigit:
            error("invalid symbol: " + characters[current_position] + next_symbol)
        tokentk = "equaltk"
        current_position += 1
        tokenList.append([tokentk, '='])

    elif token == ":":
        next_symbol = characters[current_position + 1]
        if next_symbol != '=' and not next_symbol.isalpha() and next_symbol != ' ':
            error("invalid symbol: " + characters[current_position] + next_symbol)
        if next_symbol == '=':
            tokenList.append(["assignmenttk", ':='])
            current_position += 2
        if next_symbol.isalpha() or next_symbol == " ":
            tokenList.append(["separatortk", ':'])
            current_position += 1

    elif token == ";":
        tokentk = "semicolontk"
        tokenList.append([tokentk, ';'])
        current_position += 1

    elif token == ",":
        tokentk = "commatk"
        tokenList.append([tokentk, ','])
        current_position += 1

    elif token == "(":
        tokentk = "opbrackettk"
        tokenList.append([tokentk, '('])
        current_position += 1

    elif token == ")":
        tokentk = "clbrackettk"
        tokenList.append([tokentk, ')'])
        current_position += 1

    elif token == "[":
        tokentk = "opsqrbrackettk"
        tokenList.append([tokentk, '['])
        current_position += 1

    elif token == "]":
        tokentk = "clsqrbrackettk"
        tokenList.append([tokentk, ']'])
        current_position += 1

    elif token == " " or "\t" or "\n":
        if (current_position == totalcharacters - 1):
            exit()
        else:
            current_position += 1
            lex()

    else:
        print(current_position)
        error("invalid symbol: " + token)

#
#   ~~~~~~~~ GRAMMAR ~~~~~~~
#

def program():
    global programName
    lexer()
    if checkExpectedKeywordName(counter, tokenList) != "programtk":
        error("The keyword 'program' was expected")
    lexer()
    if checkExpectedKeywordName(counter, tokenList) != "idtk":
        error("A keyword id was expected")
    programName = getKeywordName(counter, tokenList)
    name = programName
    lexer()
    block(name)
    finalCodeGenerator()
    printFinalCodeInFile()
    closeScope()
    if checkExpectedKeywordName(counter, tokenList) != "endprogramtk":
        error("The keyword 'endprogram' was expected")
    if current_position != totalcharacters - 1:
        error("You can't have anything under endprogram!")
    print("Everything worked normally!")


def block(name):
    global programName
    declarations()
    genquad("begin_block", name, "_", "_")
    subprograms()
    statements()
    if programName == name : genquad("halt", "_", "_", "_")
    genquad("end_block", name, "_", "_")


def declarations():
    while checkExpectedKeywordName(counter, tokenList) == "declaretk":
        lexer()
        varlist()


def subprograms():
    global inFunction
    while checkExpectedKeywordName(counter, tokenList) == "functiontk":
        inFunction += 1
        lexer()
        subprogram()


def statements():
    statement()
    while checkExpectedKeywordName(counter, tokenList) == "semicolontk":
        lexer()
        statement()


def statement():
    next_keyword_name = checkExpectedKeywordName(counter, tokenList)
    if next_keyword_name == "idtk":
        checkVar(getKeywordName(counter, tokenList))
        lexer()
        assignmentstat()
    elif next_keyword_name == "iftk":
        lexer()
        ifstat()
    elif next_keyword_name == "whiletk":
        lexer()
        whilestat()
    elif next_keyword_name == "dowhiletk":
        lexer()
        dowhilestat()
    elif next_keyword_name == "looptk":
        lexer()
        loopstat()
    elif next_keyword_name == "exittk":
        lexer()
        exitstat()
    elif next_keyword_name == "forcasetk":
        lexer()
        forcasestat()
    elif next_keyword_name == "incasetk":
        lexer()
        incasestat()
    elif next_keyword_name == "returntk":
        lexer()
        returnstat()
    elif next_keyword_name == "inputtk":
        lexer()
        inputstat()
    elif next_keyword_name == "printtk":
        lexer()
        printstat()


def assignmentstat():
    if checkExpectedKeywordName(counter, tokenList) != "assignmenttk":
        error("The keyword ':=' was expected")
    id = getKeywordName(counter-1, tokenList)
    lexer()
    Eplace = expression()
    genquad(":=", Eplace, "_", id)


def ifstat():
    if checkExpectedKeywordName(counter, tokenList) != "opbrackettk":
        error("The Keyword '(' was expected")
    lexer()
    (bTrue, bFalse) = condition()
    if checkExpectedKeywordName(counter, tokenList) != "clbrackettk":
        error("The Keyword ')' was expected")
    lexer()
    if checkExpectedKeywordName(counter, tokenList) != "thentk":
        error("The Keyword 'thentk' was expected")
    backpatch(quads[bTrue[0]], nextquad())
    lexer()
    statements()
    out = nextquad()
    genquad("jump", "_", "_", "_")
    backpatch(quads[bFalse[0]], nextquad())
    elsepart()
    backpatch(quads[out], nextquad())
    if checkExpectedKeywordName(counter, tokenList) != "endiftk":
        error("the Keyword 'endif' was expected")
    lexer()


def elsepart():
    if checkExpectedKeywordName(counter, tokenList) == "elsetk":
        lexer()
        statements()


def whilestat():
    if checkExpectedKeywordName(counter, tokenList) != "opbrackettk":
        error("The keyword '(' was expected")
    lexer()
    condQuad = nextquad()
    (bTrue, bFalse) = condition()
    if checkExpectedKeywordName(counter, tokenList) != "clbrackettk":
        error("The Keyword ')' was expected")
    lexer()
    backpatch(quads[bTrue[0]], nextquad())
    statements()
    genquad("jump", "_", "_", condQuad)
    backpatch(quads[bFalse[0]], nextquad())
    if checkExpectedKeywordName(counter, tokenList) != "endwhiletk":
        error("The keyword 'endwhile' was expected")
    lexer()


def dowhilestat():
    s = nextquad()
    statements()
    if checkExpectedKeywordName(counter, tokenList) == "enddowhiletk":
        lexer()
        if checkExpectedKeywordName(counter, tokenList) != "opbrackettk":
            error("the keyword '(' was expected")
        lexer()
        (condTrue, condFalse) = condition()
        backpatch(quads[condTrue[0]], s)
        backpatch(quads[condFalse[0]], nextquad())
        if tokenList[counter][0] != "clbrackettk":
            error("The keyword ')' was expected")
        lexer()


loopCount = -1
exitPointer = -1


def loopstat():
    global exitQuad
    global inLoop
    global loopCount
    inLoop = 1
    loopCount += 1
    sQuad = nextquad()
    statements()
    genquad("jump", "_", "_", sQuad)
    if checkExpectedKeywordName(counter, tokenList) != "endlooptk":
        error("The keyword 'endloop' was expected")
    backpatch(quads[exitPointer], nextquad())
    exitQuad = nextquad()
    inLoop = 0
    lexer()


def exitstat():
    global exitQuad
    global inLoop
    global loopCount
    global exitPointer
    if inLoop != 1: error("Exit was found outside of a loop")
    exitPointer = nextquad()
    genquad("jump", "_", "_", "_")


def forcasestat():
    t = newTemp()
    flagQuad = nextquad()
    genquad(":=", "0", "_", t)
    while checkExpectedKeywordName(counter, tokenList) == "whentk":
        lexer()
        if checkExpectedKeywordName(counter, tokenList) != "opbrackettk":
            error("The keyword '(' was expected")
        lexer()
        (condTrue, condFalse) = condition()
        backpatch(quads[condTrue[0]], nextquad())
        genquad(":=", "1", "_", t)
        if checkExpectedKeywordName(counter, tokenList) != "clbrackettk":
            error("The keyword ')' was expected")
        lexer()
        if checkExpectedKeywordName(counter, tokenList) != "separatortk":
            error("The keyword ':' was expected")
        lexer()
        statements()
        backpatch(quads[condFalse[0]], nextquad())

    if checkExpectedKeywordName(counter, tokenList) != "defaulttk":
        error("The keyword 'default' was expected")
    lexer()
    exitQuad = nextquad()
    genquad("=", "1", t, "_")
    if checkExpectedKeywordName(counter, tokenList) != "separatortk":
        error("The keyword ':' was expected")
    lexer()
    statements()
    genquad("=", "0", t, flagQuad)
    if checkExpectedKeywordName(counter, tokenList) != "enddefaulttk":
        error("The keyword 'enddefault' was expected")
    lexer()
    if checkExpectedKeywordName(counter, tokenList) != "endforcasetk":
        error("The keyword 'endforcase' was expected")
    lexer()
    lastQuad = nextquad()
    backpatch(quads[exitQuad], lastQuad)


def incasestat():
    t = newTemp()
    flagQuad = nextquad()
    genquad(":=", "0", "_", t)
    while checkExpectedKeywordName(counter, tokenList) == "whentk":
        lexer()
        if checkExpectedKeywordName(counter, tokenList) != "opbrackettk":
            error("The keyword '(' was expected")
        lexer()
        (condTrue, condFalse) = condition()
        backpatch(quads[condTrue[0]], nextquad())
        genquad(":=", "1", "_", t)
        if checkExpectedKeywordName(counter, tokenList) != "clbrackettk":
            error("The keyword ')' was expected")
        lexer()
        if checkExpectedKeywordName(counter, tokenList) != "separatortk":
            error("The keyword ':' was expected")
        lexer()
        statements()
        backpatch(quads[condFalse[0]], nextquad())
    genquad("=", "1", t, flagQuad)

    if checkExpectedKeywordName(counter, tokenList) != "endincasetk":
        error("The keyword 'endincase' was expected")
    lexer()


def returnstat():
    global inFunction
    global foundReturn
    if inFunction <= 0: error("Keyword return can only be inside a function")
    foundReturn = 1
    returnValue = expression()
    genquad("ret", returnValue, "_", "_")
    return returnValue


def printstat():
    printValue = expression()
    genquad("OUT", printValue, "_", "_")
    return printValue


def inputstat():
    if checkExpectedKeywordName(counter, tokenList) != "idtk":
        error("A keyword id was expected")
    id = getKeywordName(counter, tokenList)
    genquad("INP", id, "_", "_")
    lexer()


def varlist():
    if checkExpectedKeywordName(counter, tokenList) != "idtk":
        error("missing semicolon ;")
    addVar(getKeywordName(counter, tokenList))
    lexer()
    while checkExpectedKeywordName(counter, tokenList) == "commatk":
        lexer()
        if checkExpectedKeywordName(counter, tokenList) != "idtk":
            error("A keyword id was expected")
        addVar(getKeywordName(counter, tokenList))
        lexer()
    if checkExpectedKeywordName(counter, tokenList) == "semicolontk":
        lexer()


def subprogram():
    global inFunction
    global foundReturn
    if checkExpectedKeywordName(counter, tokenList) != "idtk":
        error("The keyword 'id' was expected")
    subprogramName = tokenList[counter][1]
    lexer()
    funcbody(subprogramName)
    if checkExpectedKeywordName(counter, tokenList) != "endfunctiontk":
        error("The Keyword 'endfunction' was expected")
    inFunction -= 1
    if foundReturn != 1: error("All functions must contain the return keyword.")
    lexer()
    foundReturn = 0



def funcbody(name):
    addFunc(name)
    changeScope()
    formalpars()
    block(name)
    finalCodeGenerator()
    quadCount = len(quads)
    off = closeScope()
    setFuncOffset(off)


def formalpars():
    if checkExpectedKeywordName(counter, tokenList) != "opbrackettk":
        error("The keyword '(' was expected")
    lexer()
    formalparlist()
    if checkExpectedKeywordName(counter, tokenList) != "clbrackettk":
        error("The keyword ')' was expected")
    lexer()


def formalparlist():
    keywordtk = checkExpectedKeywordName(counter, tokenList)
    if keywordtk == "intk" or keywordtk == "inouttk" or keywordtk == "inandouttk":
        formalparitem()
        while checkExpectedKeywordName(counter, tokenList) == "commatk":
            lexer()
            formalparitem()


def formalparitem():
    keywordtk = checkExpectedKeywordName(counter, tokenList)
    if keywordtk != "intk" and keywordtk != "inouttk" and keywordtk != "inandouttk":
        error("The keywords 'in', 'inout', 'inandout' was expected")
    fillFuncVariableType(getKeywordName(counter, tokenList))
    lexer()
    if checkExpectedKeywordName(counter, tokenList) != "idtk":
        error("The keyword id was expected")
    fillFuncVariables(getKeywordName(counter, tokenList))
    lexer()


def actualpars(id):
    if checkExpectedKeywordName(counter, tokenList) != "opbrackettk":
        error("The keyword '(' was expected")
    lexer()
    actualparlist(id)
    if checkExpectedKeywordName(counter, tokenList) != "clbrackettk":
        error("The keyword ')' was expected")
    lexer()


def actualparlist(id):
    keywordtk = checkExpectedKeywordName(counter, tokenList)
    parameter = 0
    if keywordtk == "intk" or keywordtk == "inouttk" or keywordtk == "inandouttk":
        actualparitem(id, parameter)
        parameter += 1
        while checkExpectedKeywordName(counter, tokenList) == "commatk":
            lexer()
            actualparitem(id, parameter)
            parameter += 1

def actualparitem(id, parameter):
    parameterType = getKeywordName(counter, tokenList)
    checkParameterType(id, parameter, parameterType)
    keywordNameTk = checkExpectedKeywordName(counter, tokenList)

    if keywordNameTk != 'intk' and keywordNameTk != 'inouttk' and \
            keywordNameTk != 'inandouttk':
        error("The keywords 'in', 'inout', 'inandout' was expected")

    if keywordNameTk == "intk":
        lexer()
        expr = expression()
        genquad("par", expr, "CV", "_")

    if keywordNameTk == "inouttk":
        lexer()
        if checkExpectedKeywordName(counter, tokenList) != "idtk":
            error("A keyword id was expected")
        id = getKeywordName(counter, tokenList)
        lexer()
        genquad("par", id, "REF", "_")

    if keywordNameTk == "inandouttk":
        lexer()
        if checkExpectedKeywordName(counter, tokenList) != "idtk":
            error("A keyword id was expected")
        id = getKeywordName(counter, tokenList)
        lexer()
        genquad("par", id, "CP", "_")


def condition():
    (q1True, q1False) = boolterm()
    bTrue = q1True
    bFalse = q1False
    while checkExpectedKeywordName(counter, tokenList) == "ortk":
        lexer()
        backpatch(quads[bFalse[0]], nextquad())
        (q2True, q2False) = boolterm()
    return (bTrue, bFalse)


def boolterm():
    (r1True, r1False) = boolfactor()
    qTrue = r1True
    qFalse = r1False
    while checkExpectedKeywordName(counter, tokenList) == "andtk":
        lexer()
        backpatch(quads[qTrue[0]], nextquad())
        (r2True, r2False) = boolfactor()
        qFalse = mergelist(qFalse, r2False)
        qTrue = r2True
    return (qTrue, qFalse)


def boolfactor():
    keyword_name = checkExpectedKeywordName(counter, tokenList)
    if keyword_name != "nottk" and keyword_name != 'opsqrbrackettk':
        expr1 = expression()
        relop = relationoper()
        expr2 = expression()
        rTrue = makelist(nextquad())
        genquad(relop, expr1, expr2, "_")
        rFalse = makelist(nextquad())
        genquad("jump", "_", "_", "_")
        return (rTrue, rFalse)

    if keyword_name == 'nottk':
        lexer()
        if checkExpectedKeywordName(counter, tokenList) != "opsqrbrackettk":
            error("The keyword '[' was expected")
        lexer()
        (q1True, q1False) = condition()
        if checkExpectedKeywordName(counter, tokenList) != "clsqrbrackettk":
            error("the keyword ']' was expected")
        lexer()
        return (q1True, q1False)

    if keyword_name == "opsqrbrackettk":
        lexer()
        (q1True, q1False) = condition()
        if checkExpectedKeywordName(counter, tokenList) != "clsqrbrackettk":
            error("The keyword ']' was expected")
        lexer()
        return (q1True, q1False)


def expression():
    optionalsign()
    t1 = term()

    while checkExpectedKeywordName(counter, tokenList) == "plustk" or \
            checkExpectedKeywordName(counter, tokenList) == "minustk":
        oper = getKeywordName(counter, tokenList)
        lexer()
        t2 = term()
        w = newTemp()
        genquad(oper, t1, t2, w)
        t1 = w
    return t1


def term():
    f1 = factor()
    while checkExpectedKeywordName(counter, tokenList) == "multtk" or \
            checkExpectedKeywordName(counter, tokenList) == "divtk":
        oper = getKeywordName(counter, tokenList)
        lexer()
        f2 = factor()
        w = newTemp()
        genquad(oper, f1, f2, w)
        f1 = w  # f1 = total result
    return f1


def factor():
    if tokenList[counter][0] == "opbrackettk":
        lexer()
        expr = expression()
        if tokenList[counter][0] == "clbrackettk":
            lexer()
            return expr
        else:
            error("They keyword ')' was expected")
    elif tokenList[counter][0] == "idtk":
        id = tokenList[counter][1]
        lexer()
        idtail(id)
        return id

    elif tokenList[counter][0] == "constanttk":
        constant = tokenList[counter][1]
        lexer()
        return constant
    else:
        error("A constant or id or '(' was expected")


def idtail(id):
    if tokenList[counter][0] == "opbrackettk":
        actualpars(id)
        checkFunc(id)
        genquad("call", id, "_", "_")
        w = newTemp()
        genquad("par", w, "RET", "_")
    else:
        checkVar(
            id)  # Checks if variable is being used as a variable and if it was visible (if id was not a function name)


def relationoper():
    oper = tokenList[counter][1]
    if tokenList[counter][0] == "equaltk":
        lexer()
    elif tokenList[counter][0] == "lessorequaltk":
        lexer()
    elif tokenList[counter][0] == "moreorequaltk":
        lexer()
    elif tokenList[counter][0] == "moretk":
        lexer()
        return tokenList[counter - 1][1]
    elif tokenList[counter][0] == "lesstk":
        lexer()
    elif tokenList[counter][0] == "differenttk":
        lexer()
    else:
        error("An operator was expected")
    return oper


def optionalsign():
    if tokenList[counter][0] == "plustk" or tokenList[counter][0] == "minustk":
        lexer()


################### INTERMEDIATE ##################################

tempCount = 1


def newTemp():
    global tempCount
    temp = "T_" + str(tempCount)
    tempCount = tempCount + 1
    addVar(temp)
    return temp


def genquad(op, x, y, z):
    global quads
    quads.append([op, x, y, z])


def nextquad():
    global quads
    return len(quads)


def emptylist():
    return []


def makelist(x):
    return [x]


def mergelist(x, y):
    x += y
    return x


def backpatch(x, z):
    for i in range(len(quads)):
        if quads[i] == x:
            quads[i][3] = z


def printQuads():
    for i in range(len(quads)):
        print(str(i) + ": " + str(quads[i]))


def changeScope():  # vrhka sunarthsh
    global entities
    global currentScope
    entities.append([])
    currentScope += 1


def closeScope():
    global entities
    global currentScope
    checkNames()
    print(entities[currentScope])
    funcOffset = findCurrentOffset() + 4  # get offset of last var in function
    entities.pop(currentScope)
    currentScope -= 1
    return funcOffset


def addFunc(func):
    global entities
    global currentScope
    entities[currentScope].append([func, 0, "func", []])


def addVar(var):
    global entities
    global currentScope
    currentOffset = findCurrentOffset() + 4
    entities[currentScope].append([var, currentOffset, "var", []])


def findCurrentOffset():
    global entities
    global currentScope
    lastVar = -1
    for i in range(len(entities[currentScope])):
        if entities[currentScope][i][2] == "var":
            lastVar = i
    if (lastVar == -1):
        offset = 8
    else:
        offset = entities[currentScope][lastVar][1]
    return offset


def fillFuncVariableType(type):
    global entities
    global currentScope
    entities[currentScope - 1][len(entities[currentScope - 1]) - 1][3].append(type)


def fillFuncVariables(id):
    addVar(id)


def setFuncOffset(num):
    global entities
    global currentScope
    entities[currentScope][len(entities[currentScope]) - 1][1] = num


def checkNames():
    global entities
    global currentScope
    seen = set()
    for i in range(len(entities[currentScope])):
        if entities[currentScope][i][0] in seen:
            error("The name " + entities[currentScope][i][0] + " is being used more than once within the same scope.")
        else:
            seen.add(entities[currentScope][i][0])


def checkVar(id):
    found = 0
    global entities
    for i in range(len(entities)):
        for j in range(len(entities[i])):
            if entities[i][j][0] == id:
                if entities[i][j][2] == "var":
                    found = 1
                else:
                    error("The function " + id + " is being used as a variable")
    if found == 0:
        error("Variable " + id + " was not declared or is not visible")


def checkFunc(id):
    found = 0
    global entities
    for i in range(len(entities)):
        for j in range(len(entities[i])):
            if entities[i][j][0] == id:
                if entities[i][j][2] == "func":
                    found = 1
                else:
                    error("The variable " + id + " is being used as a function")
    if found == 0:
        error("Function " + id + " was not declared or is not visible")


def checkParameterType(id, num, type):
    global entities
    for i in range(len(entities)):
        for j in range(len(entities[i])):
            if entities[i][j][0] == id:
                if len(entities[i][j][3]) == num:
                    error("You cannot use more arguments than those declared in a function")
                if entities[i][j][3][num] == type:
                    return
                else:
                    error("The variable " + id + " is not being passed as the declared type")


def printCFile():
    file = open(sys.argv[1] + ".c", "w")
    file.write("int main(void)\n{\n")
    for i in range(len(quads)):
        if quads[i][0] in ["begin_block", "end_block", "halt", "ret", "par"]:
            pass
        elif quads[i][0] == ":=":
            file.write("\tL_" + str(i) + ": " + quads[i][3] + " = " + str(quads[i][1]) + "; //" + str(quads[i]) + "\n")
        elif quads[i][0] == "=":
            file.write(
                "\tL_" + str(i) + ": " + "if (" + str(quads[i][1]) + " == " + str(quads[i][2]) + ") goto L_" + str(
                    quads[i][3]) + "; //" + str(quads[i]) + "\n")
        elif quads[i][0] in ["<", ">", "<=", ">="]:
            file.write(
                "\tL_" + str(i) + ": " + str(quads[i][3]) + " = " + str(quads[i][1]) + "; //" + str(quads[i]) + "\n")
        elif quads[i][0] == "<>":
            file.write("\tL_" + str(i) + ": " + "if (" + quads[i][1] + " != " + str(quads[i][2]) + ") goto L_" + str(
                quads[i][3]) + "; //" + str(quads[i]) + "\n")
        elif quads[i][0] in ["+", "-", "*", "/"]:
            file.write("\tL_" + str(i) + ": " + str(quads[i][3]) + " = " + str(quads[i][1]) + " " + str(
                quads[i][0]) + " " + str(quads[i][2]) + "; //" + str(quads[i]) + "\n")
        elif quads[i][0] == "jump":
            file.write("\tL_" + str(i) + ": " + "goto L_" + str(quads[i][3]) + "; //" + str(quads[i]) + "\n")
        elif quads[i][0] == "INP":
            file.write("\tL_" + str(i) + ": " + "scanf(\"%d\", " + "&" + str(quads[i][1]) + ")" + "; //" + str(
                quads[i]) + "\n")
        elif quads[i][0] == "OUT":
            file.write(
                "\tL_" + str(i) + ": " + "printf(\"%d\", " + str(quads[i][1]) + ")" + "; //" + str(quads[i]) + "\n")
    file.write("}\n")
    file.close()


def printQuadsInFile():
    file = open(sys.argv[1] + ".int", "w")
    for i in range(len(quads)):
        file.write(str(i) + ": " + str(quads[i]) + "\n")
    file.close()


################################## FINAL CODE ######################################

finalCode = []


def printFinalCodeInFile():
    file = open(sys.argv[1] + ".asm", "w")
    for i in range(len(finalCode)):
        file.write(str(finalCode[i]) + "\n")
    file.close()


def findScopeAndOffset(id):
    global entities
    for i in range(currentScope, -1, -1):
        for j in range(len((entities)[currentScope])):
            if entities[currentScope][j][0] == id:
                return (currentScope, entities[currentScope][j][1])
    return None, None


def gnvlcode(id):
    global finalCode
    scope, offset = findScopeAndOffset(id)
    finalCode.append("lw $t0, -4($sp)")
    for i in range(scope - 1):
        finalCode.append("lw $t0, -4($t0)")
    finalCode.append("addi $t0, t0, -" + str(offset))


def loadvr(v, r):
    global finalCode
    global currentScope
    scope, offset = findScopeAndOffset(v)
    typeOfPar = None

    if scope == None:  # None if constant
        finalCode.append("li $t" + str(r) + " ," + str(v))

    elif scope == 0:
        finalCode.append("lw $t" + str(r) + " ,-" + str(offset) + "($s0)")

    elif scope == currentScope:
        functionParameters = len(entities[currentScope - 1][len(entities[currentScope - 1]) - 1][
                                     3])  # poses parametrous exei h sunarthsh sthn opoia vriskomaste
        for i in range(functionParameters):
            if entities[currentScope][i][0] == v:  # onoma ths i parametrou
                typeOfPar = entities[currentScope - 1][len(entities[currentScope - 1]) - 1][3][
                    i]  # save the tye of parameter if it's in the arguments
        if (typeOfPar == "in" or typeOfPar == None):
            finalCode.append("lw $t" + str(r) + " ,-" + str(offset) + "($sp)")
        elif (typeOfPar == "inout" or typeOfPar == "inandout"):
            finalCode.append("lw $t0 ,-" + str(offset) + "($sp)")
            finalCode.append("lw $t" + str(r) + " ,($t0)")

    elif scope < currentScope:
        functionParameters = len(entities[scope - 1][len(entities[scope - 1]) - 1][
                                     3])  # poses parametrous exei h sunarthsh sthn opoia vriskomaste
        for i in range(functionParameters):
            if entities[scope][i][0] == v:  # onoma ths i parametrou
                typeOfPar = entities[scope - 1][len(entities[scope - 1]) - 1][3][
                    i]  # save the tye of parameter if it's in the arguments
        gnvlcode(v)
        if (typeOfPar == "in" or typeOfPar == None):
            finalCode.append("lw $t" + str(r) + " ,($t0)")
        elif (typeOfPar == "inout" or typeOfPar == "inandout"):
            finalCode.append("lw $t0 ,($t0)")
            finalCode.append("lw $t" + str(r) + " ,($t0)")
    else:
        print("Opou na nai th valate thn loadvr")


def storerv(r, v):
    global finalCode
    global currentScope
    scope, offset = findScopeAndOffset(v)
    typeOfPar = None
    if scope == None:
        pass  # stops us if we try to store a variable that cannot currently be used (not in an open scope)
    elif scope == 0:
        finalCode.append("sw $t" + str(r) + " , -" + str(offset) + "($s0)")

    elif scope == currentScope:
        functionParameters = len(entities[currentScope - 1][len(entities[currentScope - 1]) - 1][3])  # best thing ever!
        for i in range(functionParameters):
            if entities[currentScope][i][0] == v:
                typeOfPar = entities[currentScope - 1][len(entities[currentScope - 1]) - 1][3][i]  # best thing ever + 1
        if (typeOfPar == "in" or typeOfPar == None):
            finalCode.append("sw $t" + str(r) + " ,-" + str(offset) + "($sp)")
        elif (typeOfPar == "inout" or typeOfPar == "inandout"):
            finalCode.append("lw $t0 ,-" + str(offset) + "($sp)")
            finalCode.append("sw $t" + str(r) + ", ($t0)")

    elif scope < currentScope:
        functionParameters = len(entities[scope - 1][len(entities[scope - 1]) - 1][
                                     3])  # poses parametrous exei h sunarthsh sthn opoia vriskomaste
        for i in range(functionParameters):
            if entities[scope][i][0] == v:  # onoma ths i parametrou
                typeOfPar = entities[scope - 1][len(entities[scope - 1]) - 1][3][
                    i]  # save the tye of parameter if it's in the arguments
        gnvlcode(v)
        if (typeOfPar == "in" or typeOfPar == None):
            finalCode.append("sw $t" + str(r) + " ,($t0)")
        elif (typeOfPar == "inout" or typeOfPar == "inandout"):
            finalCode.append("lw $t0 ,($t0)")
            finalCode.append("sw $t" + str(r) + " ,($t0)")
    else:
        print("aderfeeeeee ti vazeis sthn storerv ? ")


quadCount = 0


def finalCodeGenerator():
    global finalCode
    parameterNum = 0
    currentFunction = ""
    for i in range(quadCount, len(quads)):
        finalCode.append("L" + str(i) + ":")
        if (quads[i][0] == "+" or quads[i][0] == "-" or quads[i][0] == "*" or quads[i][0] == "/"):
            loadvr(quads[i][1], 1)
            loadvr(quads[i][2], 2)
            finalCode.append(matchOperator(quads[i][0]) + " $t1, $t1, $t2")
            storerv(1, quads[i][3])
        elif quads[i][0] == "<" or quads[i][0] == ">" or quads[i][0] == "<>" or quads[i][0] == "<=" or quads[i][
            0] == ">=" or quads[i][0] == "=":
            loadvr(quads[i][1], 1)
            loadvr(quads[i][2], 2)
            finalCode.append(matchRelop(quads[i][0]) + " $t1, $t2, L" + str(quads[i][3]))
        elif quads[i][0] == "jump":
            finalCode.append("j L" + str(quads[i][3]))
        elif quads[i][0] == ":=":
            loadvr(quads[i][1], 1)
            storerv(1, str(quads[i][3]))
        elif quads[i][0] == "OUT":
            finalCode.append("li $v0, 1")
            loadvr(quads[i][1], 1)
            finalCode.append("add $a0, $t1, 0")
            finalCode.append("syscall")
        elif quads[i][0] == "INP":
            finalCode.append("li $v0, 5")
            finalCode.append("syscall")
            finalCode.append("move $t1, $v0")
        elif quads[i][0] == "RET":
            loadvr(quads[i][3], 1)
            finalCode.append("lw $t0, -8($sp)")
            finalCode.append("sw $t1, ($t0)")
        elif quads[i][0] == "par":
            if parameterNum == 0:
                finalCode.append("add $fp, $sp, _")
            elif quads[i][2] == "CV":
                loadvr(quads[i][1], 0)
                finalCode.append("sw $t0, -" + str(12 + 4 * parameterNum) + "($fp)")
            elif quads[i][2] == "REF":
                generateRefParameter(quads[i][1], parameterNum)
            elif quads[i][2] == "RET":
                scope, offset = findScopeAndOffset(quads[i][1])
                finalCode.append("add $t0, $sp, -" + str(offset))
                finalCode.append("sw $t0, -8($fp)")
                parameterNum = parameterNum + 1
        elif quads[i][0] == "call":
            scope, offset = findScopeAndOffset(currentFunction)
            scopeCall, offsetCall = findScopeAndOffset(quads[i][1])  # cope ths klh8eisas
            frameLength = findCurrentOffset() + 4
            if scope == scopeCall:
                finalCode.append("lw $t0, -4($sp)")
                finalCode.append("sw $t0, -4($fp)")
            else:
                finalCode.append("sw $sp, -4($fp)")
            # finalCode.replace("_", str(frameLength))
            finalCode = [w.replace("_", str(frameLength)) for w in finalCode]
            finalCode.append("add $sp, $sp, " + str(frameLength))
            finalCode.append("jal L" + str(functionlabels[currentFunction]))
            finalCode.append("add $sp, $sp, -" + str(frameLength))
            parameterNum = 0
        elif quads[i][0] == "end_block":
            if currentScope != 0:
                finalCode.append("lw $ra, ($sp)")
                finalCode.append("jr $ra")
        elif quads[i][0] == "begin_block":
            currentFunction = quads[i][1]
            functionlabels[currentFunction] = i
            if currentScope == 0:
                finalCode.append("Lmain:")
                finalCode.append("add $sp, $sp, " + str(findCurrentOffset() + 4))
                finalCode.append("move $s0, $sp")
            else:
                finalCode.append("sw $ra, ($sp)")


functionlabels = {}


def generateRefParameter(parameter, number):
    global finalCode
    global currentScope
    scope, offset = findScopeAndOffset(parameter)
    typeOfPar = None

    if scope == currentScope:
        ammountOfFunctionParameters = len(entities[currentScope - 1][len(entities[currentScope - 1]) - 1][3])
        for i in range(ammountOfFunctionParameters):
            if entities[currentScope][i][0] == parameter:  # onoma ths i parametrou
                typeOfPar = entities[currentScope - 1][len(entities[currentScope - 1]) - 1][3][
                    i]  # save the tye of parameter if it's in the arguments
        if (typeOfPar == "in" or typeOfPar == None):
            finalCode.append("add $t0, $sp, -" + offset)
            finalCode.append("sw $t0, -" + str(12 + 4 * number) + "($fp)")

        elif (typeOfPar == "inout" or typeOfPar == "inandout"):
            finalCode.append("lw $t0 ,-" + str(offset) + "($sp)")
            finalCode.append("sw $t0, -" + str(12 + 4 * number) + "($fp)")

    elif scope < currentScope:
        ammountOfFunctionParameters = len(entities[scope - 1][len(entities[scope - 1]) - 1][3])
        for i in range(ammountOfFunctionParameters):
            if entities[scope][i][0] == parameter:  # onoma ths i parametrou
                typeOfPar = entities[scope - 1][len(entities[scope - 1]) - 1][3][
                    i]  # save the tye of parameter if it's in the arguments
        gnvlcode(parameter)
        if (typeOfPar == "in" or typeOfPar == None):
            finalCode.append("sw $t0, -" + str(12 + 4 * parameter) + "($fp)")
        elif (typeOfPar == "inout" or typeOfPar == "inandout"):
            finalCode.append("lw $t0 ,($t0)")
            finalCode.append("sw $t0, -" + str(12 + 4 * parameter) + "($fp)")
    else:
        print("Edw paidia den einai REF")


def matchOperator(oper):
    if oper == '+': return 'add'
    if oper == '-': return 'sub'
    if oper == '*': return 'mul'
    return 'div'


def matchRelop(relop):
    if relop == '<' : return 'blt'
    if relop == '>' : return 'bgt'
    if relop == '>' : return 'bgt'
    if relop == '<=': return 'ble'
    if relop == '>=': return 'bge'
    if relop == '=' : return 'beq'
    return 'bne'


# call function program() for checking, Quads for scopes on the screen and file .C and .int
program()
printCFile()
printQuadsInFile()
# printQuads() #Remove comment to print quads on the screen
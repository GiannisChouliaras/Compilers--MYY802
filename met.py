##  EPWNYMO      ONOMA      AM
##  KALOUDIS     SPYRIDWN   2447
##  CHOULIARAS   IOANNIS    2631

#imports
import sys

# variables
tokentk = ""
numberofchar = 0
token = ""
linecounter = 0
tokenList = []
programName = ""
counter = -1

#scope
currentScope = 0
entities = [[]]
quads = []

#variables for checking Loops and Functions
inLoop = 0
exitQuad = -1
inFunction = 0
foundReturn = 0

#open / close file
with open(sys.argv[1] + ".stl") as file:
    c = file.read()
totalcharacters = len(c)

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

def lexer() :
    global counter
    counter += 1
    lex()

def lex():

    global numberofchar
    global token
    global tokentk
    global tokenList
    global linecounter

    token = c[numberofchar]
    if c[numberofchar] == '\n': linecounter += 1

    if c[numberofchar].isalpha():
        while(c[numberofchar].isalpha() or c[numberofchar].isdigit()):
            if (numberofchar == totalcharacters-1):
                break
            else:
                numberofchar += 1
            if c[numberofchar].isalpha() or c[numberofchar].isdigit():
                token = token + c[numberofchar]
            else:
                break

        if token == "program":
            tokentk = "programtk"
            tokenList.append([tokentk, token])

        elif token == "endprogram":
            tokentk = "endprogramtk"
            tokenList.append([tokentk, token])

        elif token == "declare":
            tokentk = "declaretk"
            tokenList.append([tokentk, token])

        elif token == "if":
            tokentk = "iftk"
            tokenList.append([tokentk, token])

        elif token == "then":
            tokentk = "thentk"
            tokenList.append([tokentk, token])

        elif token == "else":
            tokentk = "elsetk"
            tokenList.append([tokentk, token])

        elif token == "endif":
            tokentk = "endiftk"
            tokenList.append([tokentk, token])

        elif token == "dowhile":
            tokentk = "dowhiletk"
            tokenList.append([tokentk, token])

        elif token == "enddowhile":
            tokentk = "enddowhiletk"
            tokenList.append([tokentk, token])

        elif token == "while":
            tokentk = "whiletk"
            tokenList.append([tokentk, token])

        elif token == "endwhile":
            tokentk = "endwhiletk"
            tokenList.append([tokentk, token])

        elif token == "loop":
            tokentk = "looptk"
            tokenList.append([tokentk, token])

        elif token == "endloop":
            tokentk = "endlooptk"
            tokenList.append([tokentk, token])

        elif token == "exit":
            tokentk = "exittk"
            tokenList.append([tokentk, token])

        elif token == "forcase":
            tokentk = "forcasetk"
            tokenList.append([tokentk, token])

        elif token == "endforcase":
            tokentk = "endforcasetk"
            tokenList.append([tokentk, token])

        elif token == "incase":
            tokentk = "incasetk"
            tokenList.append([tokentk, token])

        elif token == "endincase":
            tokentk = "endincasetk"
            tokenList.append([tokentk, token])

        elif token == "when":
            tokentk = "whentk"
            tokenList.append([tokentk, token])

        elif token == "endwhen":
            tokentk = "endwhentk"
            tokenList.append([tokentk, token])

        elif token == "default":
            tokentk = "defaulttk"
            tokenList.append([tokentk, token])

        elif token == "enddefault":
            tokentk = "enddefaulttk"
            tokenList.append([tokentk, token])

        elif token == "function":
            tokentk = "functiontk"
            tokenList.append([tokentk, token])

        elif token == "endfunction":
            tokentk = "endfunctiontk"
            tokenList.append([tokentk, token])

        elif token == "return":
            tokentk = "returntk"
            tokenList.append([tokentk, token])

        elif token == "in":
            tokentk = "intk"
            tokenList.append([tokentk, token])

        elif token == "inout":
            tokentk = "inouttk"
            tokenList.append([tokentk, token])

        elif token == "inandout":
            tokentk = "inandouttk"
            tokenList.append([tokentk, token])

        elif token == "and":
            tokentk = "andtk"
            tokenList.append([tokentk, token])

        elif token == "or":
            tokentk = "ortk"
            tokenList.append([tokentk, token])

        elif token == "not":
            tokentk = "nottk"
            tokenList.append([tokentk, token])

        elif token == "input":
            tokentk = "inputtk"
            tokenList.append([tokentk, token])

        elif token == "print":
            tokentk = "printtk"
            tokenList.append([tokentk, token])

        else:
            tokentk = "idtk"
            token = token[:30]  # only 30 first characters
            tokenList.append([tokentk, token])

    elif c[numberofchar].isdigit():
        while(c[numberofchar].isdigit()):
            if (numberofchar == totalcharacters - 1):
                break
            else:
                numberofchar += 1
            if c[numberofchar].isdigit():
                token = token + c[numberofchar]
            elif c[numberofchar].isalpha():
                error("Cannot write a letter after a number")
            else:
                break
        if int (token) < -32767:
            error("Invalid number, numbers cannnot be lower than -32767")
        elif int (token) > 32767:
            error("Invalid number, numbers cannnot exceed 32767")
        else:
            tokentk = "constanttk"
            tokenList.append([tokentk, int (token)])


    elif c[numberofchar] == "/":
        if numberofchar != totalcharacters - 1:
            if c[numberofchar+1] == "/":
                tokentk = "linecommenttk"
                tokenList.append([tokentk, '//'])
                numberofchar += 1
                while (c[numberofchar] != "\n") :
                    if numberofchar == totalcharacters-1: quit()
                    numberofchar += 1
                linecounter += 1
                lexer()

            elif c[numberofchar+1] == "*":
                tokentk = "startcommenttk"
                tokenList.append([tokentk, '/*'])
                numberofchar += 2
                if numberofchar == totalcharacters:
                    error("File reached it's end but your comment didn't")
                while c[numberofchar]+c[numberofchar+1] != "*/":
                    if c[numberofchar] == '\n' : linecounter += 1
                    numberofchar += 1
                    if numberofchar == totalcharacters - 1:  # elegxos gia eof gia na doume an kleinoun ta sxolia
                        error("File reached it's end but your comment didn't")
                    if c[numberofchar]+c[numberofchar+1] == "/*" or c[numberofchar]+c[numberofchar+1] == "//":
                        error("You have to end a comment before starting a new one")
                if numberofchar == totalcharacters-2:  # elegxos gia eof se periptwsh pou sto telos exei comment pou kleinei kanonika
                    exit()
                numberofchar += 2
                lexer()
            elif c[numberofchar+1].isalpha() or c[numberofchar+1].isdigit() or c[numberofchar+1] == " " or c[numberofchar+1] == "\t":
                tokentk = "divtk"
                tokenList.append([tokentk, '/'])
                numberofchar += 1
            else: error("invalid symbol: " + token)
        else:
            error("you can't use / at the end of the file")

    elif c[numberofchar] == "+":
        tokentk = "plustk"
        tokenList.append([tokentk, '+'])
        numberofchar += 1

    elif c[numberofchar] == "-":
        tokentk = "minustk"
        tokenList.append([tokentk, '-'])
        numberofchar += 1

    elif c[numberofchar] == "*":
        tokentk = "multtk"
        tokenList.append([tokentk, '*'])
        numberofchar += 1

    elif c[numberofchar] == "<":
        if c[numberofchar+1] == "=":
            tokentk = "lessorequaltk"
            token = "<="
            tokenList.append([tokentk, token])
            numberofchar += 2

        elif c[numberofchar+1] == ">":
            tokentk = "differenttk"
            token = "<>"
            tokenList.append([tokentk, token])
            numberofchar += 2

        elif c[numberofchar+1].isalpha():
            tokentk = "lesstk"
            tokenList.append([tokentk, '<'])
            numberofchar += 1

        elif c[numberofchar+1].isdigit():
            tokentk = "lesstk"
            tokenList.append([tokentk, '<'])
            numberofchar += 1

        else:
            error("invalid symbol: " + c[numberofchar] + c[numberofchar+1])

    elif c[numberofchar] == ">":
        if c[numberofchar+1] == "=":
            tokentk = "moreorequaltk"
            token = ">="
            tokenList.append([tokentk, token])
            numberofchar += 2

        elif c[numberofchar+1].isalpha():
            tokentk = "moretk"
            tokenList.append([tokentk, '>'])
            numberofchar += 1

        elif c[numberofchar+1].isdigit():
            tokentk = "moretk"
            tokenList.append([tokentk, '>'])
            numberofchar += 1

        else:
            error("invalid symbol: " + c[numberofchar] + c[numberofchar+1])


    elif c[numberofchar] == "=":
        if c[numberofchar+1].isalpha():
                tokentk = "equaltk"
                numberofchar += 1
                tokenList.append([tokentk, '='])
        elif c[numberofchar+1].isdigit():
                tokentk = "equaltk"
                numberofchar += 1
                tokenList.append([tokentk, '='])
        else:
            error("invalid symbol: " + c[numberofchar] + c[numberofchar+1])

    elif c[numberofchar] == ":":
            if c[numberofchar + 1] == '=':
                tokentk = "assignmenttk"
                tokenList.append([tokentk, ':='])
                numberofchar += 2
            elif c[numberofchar + 1].isalpha() or c[numberofchar + 1] == " ":
                tokentk = "separatortk"
                tokenList.append([tokentk, ':'])
                numberofchar += 1
            else :
                error("invalid symbol: " + c[numberofchar] + c[numberofchar + 1])

    elif c[numberofchar] == ";":
            tokentk = "semicolontk"
            tokenList.append([tokentk, ';'])
            numberofchar += 1

    elif c[numberofchar] == ",":
            tokentk = "commatk"
            tokenList.append([tokentk, ','])
            numberofchar += 1

    elif c[numberofchar] == "(":
            tokentk = "opbrackettk"
            tokenList.append([tokentk, '('])
            numberofchar += 1

    elif c[numberofchar] == ")":
            tokentk = "clbrackettk"
            tokenList.append([tokentk, ')'])
            numberofchar += 1

    elif c[numberofchar] == "[":
            tokentk = "opsqrbrackettk"
            tokenList.append([tokentk, '['])
            numberofchar += 1

    elif c[numberofchar] == "]":
            tokentk = "clsqrbrackettk"
            tokenList.append([tokentk, ']'])
            numberofchar += 1

    elif c[numberofchar] == " " or "\t" or "\n":
        if( numberofchar == totalcharacters -1):
            exit()
        else:
            numberofchar+=1
            lex()

    else:
        print(numberofchar)
        error("invalid symbol: " + token)

#
#   ~~~~~~~~ GRAMMAR ~~~~~~~
#

def program():
    global programName
    lexer()
    if tokenList[counter][0] == "programtk" :
        lexer()
        if tokenList[counter][0] == "idtk":
            programName=tokenList[counter][1]
            name = programName
            lexer()
            block(name)
            finalCodeGenerator()
            printFinalCodeInFile()
            closeScope()
            if tokenList[counter][0] == "endprogramtk":
                if numberofchar != totalcharacters - 1:
                    error("You can't have anything under endprogram!")
                else :
                    print("Everything is fine! [Would print error message and line number if something was wrong]") #Print to check if everything works
            else:
                error("The keyword 'endprogram' was expected")
        else:
            error("A keyword id was expected")
    else:
        error("The keyword 'program' was expected")

def block(name):
    global programName
    declarations()
    genquad("begin_block",name,"_","_")
    subprograms()
    statements()
    if programName == name:
        genquad("halt","_","_","_")
    genquad("end_block",name,"_","_")

def declarations():
    while tokenList[counter][0] == "declaretk":
        lexer()
        varlist()

def subprograms():
    global inFunction
    while tokenList[counter][0] == "functiontk":
        inFunction += 1
        lexer()
        subprogram()

def statements():
    statement()
    while tokenList[counter][0] == "semicolontk":
        lexer()
        statement()


def statement():
    if tokenList[counter][0] == "idtk":
        checkVar(tokenList[counter][1])
        lexer()
        assignmentstat()
    elif tokenList[counter][0] == "iftk":
        lexer()
        ifstat()
    elif tokenList[counter][0] == "whiletk":
        lexer()
        whilestat()
    elif tokenList[counter][0] == "dowhiletk":
        lexer()
        dowhilestat()
    elif tokenList[counter][0] == "looptk":
        lexer()
        loopstat()
    elif tokenList[counter][0] == "exittk":
        lexer() #not sure
        exitstat()
    elif tokenList[counter][0] == "forcasetk":
        lexer()
        forcasestat()
    elif tokenList[counter][0] == "incasetk":
        lexer()
        incasestat()
    elif tokenList[counter][0] == "returntk":
        lexer()
        returnstat()
    elif tokenList[counter][0] == "inputtk":
        lexer()
        inputstat()
    elif tokenList[counter][0] == "printtk":
        lexer()
        printstat()

def assignmentstat():
    if tokenList[counter][0] == "assignmenttk":
        id = tokenList[counter-1][1]
        lexer()
        Eplace = expression()
        genquad(":=",Eplace,"_",id)
    else:
        error("The keyword ':=' was expected")

def ifstat():
    if tokenList[counter][0] == "opbrackettk":
        lexer()
        (bTrue, bFalse) = condition()
        if tokenList[counter][0] == "clbrackettk":
            lexer()
            if tokenList[counter][0] == "thentk":
                backpatch(quads[bTrue[0]],nextquad())
                lexer()
                statements()
                out = nextquad()
                genquad("jump","_","_","_")
                backpatch(quads[bFalse[0]],nextquad())
                elsepart()
                backpatch(quads[out], nextquad())
                if tokenList[counter][0] == "endiftk":
                    lexer()
                else: error("the Keyword 'endif' was expected")
            else: error("The Keyword 'thentk' was expected")
        else:
            error("The Keyword ')' was expected")
    else: error("The Keyword '(' was expected")

def elsepart():
    if tokenList[counter][0] == "elsetk":
        lexer()
        statements()

def whilestat():
    if tokenList[counter][0] == "opbrackettk":
        lexer()
        condQuad = nextquad()
        (bTrue, bFalse) = condition()
        if tokenList[counter][0] == "clbrackettk":
            lexer()
            backpatch(quads[bTrue[0]],nextquad())
            statements()
            genquad("jump","_","_",condQuad)
            backpatch(quads[bFalse[0]],nextquad())
            if tokenList[counter][0] == "endwhiletk":
                lexer()
            else: error("The keyword 'endwhile' was expected")
        else: error("The Keyword ')' was expected")
    else: error("The keyword '(' was expected")

def dowhilestat():
    s = nextquad()
    statements()
    if tokenList[counter][0] == "enddowhiletk":
        lexer()
        if tokenList[counter][0] == "opbrackettk":
            lexer()
            (condTrue,condFalse) = condition()
            backpatch(quads[condTrue[0]], s)
            backpatch(quads[condFalse[0]], nextquad())
            if tokenList[counter][0] == "clbrackettk":
                lexer()
            else: error("The keyword ')' was expected")
        else: error("the keyword '(' was expected")

loopCount = -1
exitPointer = -1

def loopstat():
    global exitQuad
    global inLoop
    global loopCount
    inLoop = 1
    loopCount+=1
    sQuad = nextquad()
    statements()
    genquad("jump","_","_",sQuad)
    if tokenList[counter][0] == "endlooptk":
        backpatch(quads[exitPointer],nextquad())
        exitQuad = nextquad()
        inLoop = 0
        lexer()
    else: error("The keyword 'endloop' was expected")

def exitstat():
    global exitQuad
    global inLoop
    global loopCount
    global exitPointer
    if inLoop == 1:
        exitPointer = nextquad()
        genquad("jump","_","_","_")
    else:
        error("Exit was found outside of a loop")

def forcasestat():
    t = newTemp()
    flagQuad = nextquad()
    genquad(":=","0","_",t)
    while tokenList[counter][0] == "whentk":
        lexer()
        if tokenList[counter][0] == "opbrackettk":
            lexer()
            (condTrue,condFalse) = condition()
            backpatch(quads[condTrue[0]],nextquad())
            genquad(":=","1","_",t)
            if tokenList[counter][0] == "clbrackettk":
                lexer()
                if tokenList[counter][0] == "separatortk":
                    lexer()
                    statements()
                    backpatch(quads[condFalse[0]],nextquad())
                else: error("The keyword ':' was expected")
            else: error("The keyword ')' was expected")
        else: error("The keyword '(' was expected")

    if tokenList[counter][0] == "defaulttk":
        lexer()
        exitQuad = nextquad()
        genquad("=","1",t,"_")
        if tokenList[counter][0] == "separatortk":
            lexer()
            statements()
            genquad("=","0",t,flagQuad)
            if tokenList[counter][0] == "enddefaulttk":
                lexer()
                if tokenList[counter][0] == "endforcasetk":
                    lexer()
                    lastQuad = nextquad()
                    backpatch(quads[exitQuad],lastQuad)
                else: error("The keyword 'endforcase' was expected")
            else: error("The keyword 'enddefault' was expected")
        else: error("The keyword ':' was expected")
    else: error("The keyword 'default' was expected")


def incasestat():
    t = newTemp()
    flagQuad = nextquad()
    genquad(":=","0","_",t)
    while tokenList[counter][0] == "whentk" :
        lexer()
        if tokenList[counter][0] == "opbrackettk":
            lexer()
            (condTrue, condFalse) = condition()
            backpatch(quads[condTrue[0]],nextquad())
            genquad(":=","1","_",t)
            if tokenList[counter][0] == "clbrackettk":
                lexer()
                if tokenList[counter][0] == "separatortk":
                    lexer()
                    statements()
                    backpatch(quads[condFalse[0]],nextquad())
                else: error("The keyword ':' was expected")
            else: error("The keyword ')' was expected")
        else: error("The keyword '(' was expected")
    genquad("=","1",t,flagQuad)
    if tokenList[counter][0] == "endincasetk":
        lexer()
    else: error("The keyword 'endincase' was expected")

def returnstat():
    global inFunction
    global foundReturn
    if inFunction > 0:
        foundReturn = 1
        returnValue = expression()
        genquad("ret", returnValue,"_","_")
        return returnValue
    else:
        error("Keyword return can only be inside a function")

def printstat():
    printValue = expression()
    genquad("OUT",printValue,"_","_")
    return printValue

def inputstat():
    if tokenList[counter][0] == "idtk":
        id = tokenList[counter][1]
        genquad("INP",id,"_","_")
        lexer()
    else: error("A keyword id was expected")

def varlist():
    if tokenList[counter][0] == "idtk":
        addVar(tokenList[counter][1])
        lexer()
        while tokenList[counter][0] == "commatk":
            lexer()
            if tokenList[counter][0] == "idtk":
                addVar(tokenList[counter][1])
                lexer()
            else: error("A keyword id was expected")
        if tokenList[counter][0] == "semicolontk":
            lexer()
        else: error("missing semicolon ;")

def subprogram():
    global inFunction
    global foundReturn
    if tokenList[counter][0] == "idtk":
        subprogramName = tokenList[counter][1]
        lexer()
        funcbody(subprogramName)
        if tokenList[counter][0] == "endfunctiontk":
            inFunction -= 1
            if foundReturn == 1:
                lexer()
                foundReturn = 0
            else:
                error("All functions must contain the return keyword.")
        else:
            error("The Keyword 'endfunction' was expected")
    else: error("The keyword 'id' was expected")

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
    if tokenList[counter][0] == "opbrackettk":
        lexer()
        formalparlist()
        if tokenList[counter][0] == "clbrackettk":
            lexer()
        else: error("The keyword ')' was expected")
    else: error("The keyword '(' was expected")

def formalparlist():
    if tokenList[counter][0] == "intk" or tokenList[counter][0] == "inouttk" or tokenList[counter][0] == "inandouttk":
        formalparitem()
        while tokenList[counter][0] == "commatk":
            lexer()
            formalparitem()

def formalparitem():
    if tokenList[counter][0] == "intk" or tokenList[counter][0] == "inouttk" or tokenList[counter][0] == "inandouttk" :
        fillFuncVariableType(tokenList[counter][1])
        lexer()
        if tokenList[counter][0] == "idtk":
            fillFuncVariables(tokenList[counter][1])
            lexer()
        else: error("The keyword id was expected")
    else: error("The keywords 'in', 'inout', 'inandout' was expected")

def actualpars(id):
    if tokenList[counter][0] == "opbrackettk":
        lexer()
        actualparlist(id)
        if tokenList[counter][0] == "clbrackettk":
            lexer()
        else: error("The keyword ')' was expected")
    else: error("The keyword '(' was expected")

def actualparlist(id):
    parameter = 0
    if tokenList[counter][0] == "intk" or tokenList[counter][0] == "inouttk" or tokenList[counter][0] == "inandouttk":
        actualparitem(id, parameter)
        parameter +=1
        while tokenList[counter][0] == "commatk":
            lexer()
            actualparitem(id, parameter)
            parameter +=1

def actualparitem(id, parameter):
    parameterType = tokenList[counter][1]
    checkParameterType(id,parameter,parameterType)
    if tokenList[counter][0] == "intk":
        lexer()
        expr = expression()
        genquad("par", expr, "CV", "_")

    elif tokenList[counter][0] == "inouttk":
        lexer()
        if tokenList[counter][0] == "idtk":
            id = tokenList[counter][1]
            lexer()
            genquad("par", id, "REF", "_")
        else: error("A keyword id was expected")
    elif tokenList[counter][0] == "inandouttk":
        lexer()
        if tokenList[counter][0] == "idtk":
            id = tokenList[counter][1]
            lexer()
            genquad("par", id, "CP", "_")
        else: error("A keyword id was expected")
    else: error("The keywords 'in', 'inout', 'inandout' was expected")

def condition():
    (q1True, q1False) = boolterm()
    bTrue = q1True
    bFalse = q1False
    while tokenList[counter][0] == "ortk":
        lexer()
        backpatch(quads[bFalse[0]], nextquad())
        (q2True,q2False) = boolterm()
    return (bTrue, bFalse)

def boolterm():
    (r1True, r1False) = boolfactor()
    qTrue = r1True
    qFalse = r1False
    while tokenList[counter][0] == "andtk":
        lexer()
        backpatch(quads[qTrue[0]], nextquad())
        (r2True,r2False) = boolfactor()
        qFalse = mergelist(qFalse,r2False)
        qTrue = r2True
    return (qTrue,qFalse)

def boolfactor():
    if tokenList[counter][0] == "nottk":
        lexer()
        if tokenList[counter][0] == "opsqrbrackettk":
            lexer()
            (q1True,q1False) = condition()
            if tokenList[counter][0] == "clsqrbrackettk":
                lexer()
                return (q1True,q1False)
            else: error("the keyword ']' was expected")
        else: error("The keyword '[' was expected")

    elif tokenList[counter][0] == "opsqrbrackettk":
        lexer()
        (q1True,q1False) = condition()
        if tokenList[counter][0] == "clsqrbrackettk":
            lexer()
            return(q1True,q1False)
        else: error("The keyword ']' was expected")
    else:
        expr1 = expression()
        relop = relationoper()
        expr2 = expression()
        rTrue = makelist(nextquad())
        genquad(relop,expr1,expr2,"_")
        rFalse = makelist(nextquad())
        genquad("jump","_","_","_")
        return (rTrue,rFalse)

def expression():
    optionalsign()
    t1 = term()

    while tokenList[counter][0] == "plustk" or tokenList[counter][0] == "minustk":
        oper = tokenList[counter][1]
        lexer()
        t2 = term()
        w = newTemp()
        genquad(oper,t1,t2,w)
        t1 = w #t1 = total sum
    return t1


def term():
    f1 = factor()
    while tokenList[counter][0] == "multtk" or tokenList[counter][0] == "divtk":
        oper = tokenList[counter][1]
        lexer()
        f2 = factor()
        w = newTemp()
        genquad(oper,f1,f2,w)
        f1 = w #f1 = total result
    return f1

def factor():
    if tokenList[counter][0] == "opbrackettk" :
        lexer()
        expr = expression()
        if tokenList[counter][0] == "clbrackettk":
            lexer()
            return expr
        else: error("They keyword ')' was expected")
    elif tokenList[counter][0] == "idtk" :
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
        genquad("call",id,"_","_")
        w = newTemp()
        genquad("par", w, "RET", "_")
    else:
        checkVar(id) #Checks if variable is being used as a variable and if it was visible (if id was not a function name)




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
        return tokenList[counter-1][1]
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

#Functions for scope and symbol table
tempCount = 1

def newTemp():
    global tempCount
    temp = "T_" + str(tempCount)
    tempCount = tempCount + 1
    addVar(temp)
    return temp

def genquad(op,x,y,z):
    global quads
    quads.append([op,x,y,z])

def nextquad():
    global quads
    return len(quads)

def emptylist():
    return []

def makelist(x):
    return [x]

def mergelist(x,y):
    x += y
    return x

def backpatch(x,z):
    for i in range(len(quads)):
        if quads[i]==x:
            quads[i][3]=z

def printQuads():
    for i in range (len(quads)) :
        print(str(i) + ": " + str(quads[i]))

def changeScope(): #vrhka sunarthsh
    global entities
    global currentScope
    entities.append([])
    currentScope+=1

def closeScope():
    global entities
    global currentScope
    checkNames()
    print(entities[currentScope])
    funcOffset = findCurrentOffset()+4 #get offset of last var in function
    entities.pop(currentScope)
    currentScope-=1
    return funcOffset

def addFunc(func):
    global entities
    global currentScope
    entities[currentScope].append([func,0,"func",[]])

def addVar(var):
    global entities
    global currentScope
    currentOffset=findCurrentOffset()+4
    entities[currentScope].append([var,currentOffset,"var",[]])

def findCurrentOffset():
    global entities
    global currentScope
    lastVar = -1
    for i in range(len(entities[currentScope])):
        if entities[currentScope][i][2] == "var":
            lastVar = i
    if (lastVar==-1):
        offset = 8
    else:
        offset = entities[currentScope][lastVar][1]
    return offset

def fillFuncVariableType(type):
    global entities
    global currentScope
    entities[currentScope-1][len(entities[currentScope-1])-1][3].append(type)

def fillFuncVariables(id):
    addVar(id)

def setFuncOffset(num):
    global entities
    global currentScope
    entities[currentScope][len(entities[currentScope])-1][1]=num

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

def checkParameterType(id,num,type):
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

#Prints in files

def printCFile():
    file = open(sys.argv[1] + ".c", "w")
    file.write("int main(void)\n{\n")
    for i in range(len(quads)):
        if quads[i][0] in ["begin_block", "end_block", "halt",  "ret", "par"]:
            pass
        elif quads[i][0] == ":=":
            file.write("\tL_" + str(i) + ": " + quads[i][3] + " = " + str(quads[i][1]) + "; //" + str(quads[i]) + "\n")
        elif quads[i][0] == "=":
            file.write("\tL_" + str(i) + ": " + "if (" + str(quads[i][1]) + " == " + str(quads[i][2]) + ") goto L_" + str(quads[i][3]) + "; //" + str(quads[i]) + "\n")
        elif quads[i][0] in ["<", ">", "<=", ">="]:
            file.write("\tL_" + str(i) + ": " + str(quads[i][3]) + " = " + str(quads[i][1]) + "; //" + str(quads[i]) + "\n")
        elif quads[i][0] == "<>":
            file.write("\tL_" + str(i) + ": " + "if (" + quads[i][1] + " != " + str(quads[i][2]) + ") goto L_" + str(quads[i][3]) + "; //" + str(quads[i]) + "\n")
        elif quads[i][0] in ["+","-","*","/"]:
            file.write("\tL_" + str(i) + ": " + str(quads[i][3]) + " = " + str(quads[i][1]) + " " +str(quads[i][0]) + " " + str(quads[i][2]) + "; //" + str(quads[i]) + "\n")
        elif quads[i][0] == "jump":
            file.write("\tL_" + str(i) + ": " + "goto L_" + str(quads[i][3]) + "; //" + str(quads[i]) + "\n")
        elif quads[i][0] == "INP":
            file.write("\tL_" + str(i) + ": " + "scanf(\"%d\", " + "&" + str(quads[i][1]) + ")" + "; //" + str(quads[i]) + "\n")
        elif quads[i][0] == "OUT":
            file.write("\tL_" + str(i) + ": " + "printf(\"%d\", " + str(quads[i][1]) + ")" + "; //" + str(quads[i]) + "\n")
    file.write("}\n")
    file.close()

def printQuadsInFile():
    file = open(sys.argv[1] + ".int", "w")
    for i in range(len(quads)):
        file.write(str(i) + ": " + str(quads[i])+"\n")
    file.close()

################################## FINAL CODE ######################################

finalCode = []

def printFinalCodeInFile():
    file = open(sys.argv[1] + ".asm", "w")
    for i in range(len(finalCode)):
        file.write(str(finalCode[i])+"\n")
    file.close()


### for the final code ###
def findScopeAndOffset(id):
    global entities
    for i in range(currentScope, -1, -1):
        for j in range(len((entities)[currentScope])):
            if entities[currentScope][j][0] == id:
                return (currentScope, entities[currentScope][j][1])
    return None,None

def gnvlcode(id):
    global finalCode
    scope, offset = findScopeAndOffset(id)
    finalCode.append("lw $t0, -4($sp)")
    for i in range (scope-1):
        finalCode.append("lw $t0, -4($t0)")
    finalCode.append("addi $t0, t0, -"+str(offset)) #add or addi?

def loadvr(v,r):
    global finalCode
    global currentScope
    scope, offset = findScopeAndOffset(v)
    typeOfPar = None

    if scope == None: #None if constant
        finalCode.append("li $t" + str(r) + " ," + str (v))

    elif scope == 0:
        finalCode.append("lw $t" + str(r) + " ,-" + str (offset) + "($s0)")

    elif scope == currentScope:
        functionParameters = len(entities[currentScope-1][len(entities[currentScope-1])-1][3]) #poses parametrous exei h sunarthsh sthn opoia vriskomaste
        for i in range(functionParameters):
            if entities[currentScope][i][0] == v: #onoma ths i parametrou
                typeOfPar = entities[currentScope-1][len(entities[currentScope-1])-1][3][i] #save the tye of parameter if it's in the arguments
        if (typeOfPar == "in" or typeOfPar == None):
            finalCode.append("lw $t" + str(r) + " ,-" + str (offset) + "($sp)")
        elif (typeOfPar == "inout" or typeOfPar == "inandout"):
            finalCode.append("lw $t0 ,-" + str (offset) + "($sp)")
            finalCode.append("lw $t" + str(r) + " ,($t0)")

    elif scope < currentScope:
        functionParameters = len(entities[scope-1][len(entities[scope-1])-1][3]) #poses parametrous exei h sunarthsh sthn opoia vriskomaste
        for i in range(functionParameters):
            if entities[scope][i][0] == v: #onoma ths i parametrou
                typeOfPar = entities[scope-1][len(entities[scope-1])-1][3][i] #save the tye of parameter if it's in the arguments
        gnvlcode(v)
        if (typeOfPar == "in" or typeOfPar == None):
            finalCode.append("lw $t" + str(r) + " ,($t0)")
        elif (typeOfPar == "inout" or typeOfPar == "inandout"):
            finalCode.append("lw $t0 ,($t0)")
            finalCode.append("lw $t" + str(r) + " ,($t0)")
    else:
        print("Opou na nai th valate thn loadvr")


def storerv(r,v):
    global finalCode
    global currentScope
    scope, offset = findScopeAndOffset(v)
    typeOfPar = None
    if scope == None:
        pass # stops us if we try to store a variable that cannot currently be used (not in an open scope)
    elif scope == 0:
        finalCode.append("sw $t" + str(r) + " , -" + str (offset) + "($s0)")

    elif scope == currentScope:
        functionParameters = len(entities[currentScope-1][len(entities[currentScope-1])-1][3]) #best thing ever!
        for i in range (functionParameters):
            if entities[currentScope][i][0] == v:
                typeOfPar = entities[currentScope-1][len(entities[currentScope-1])-1][3][i] #best thing ever + 1
        if (typeOfPar == "in" or typeOfPar == None):
            finalCode.append("sw $t" + str(r) + " ,-" + str(offset) + "($sp)")
        elif (typeOfPar == "inout" or typeOfPar == "inandout"):
            finalCode.append("lw $t0 ,-" + str(offset) + "($sp)")
            finalCode.append("sw $t" + str(r) +", ($t0)")

    elif scope < currentScope:
        functionParameters = len(entities[scope-1][len(entities[scope-1])-1][3]) #poses parametrous exei h sunarthsh sthn opoia vriskomaste
        for i in range(functionParameters):
            if entities[scope][i][0] == v: #onoma ths i parametrou
                typeOfPar = entities[scope-1][len(entities[scope-1])-1][3][i] #save the tye of parameter if it's in the arguments
        gnvlcode(v)
        if (typeOfPar == "in" or typeOfPar == None):
            finalCode.append("sw $t" + str(r) + " ,($t0)")
        elif (typeOfPar == "inout" or typeOfPar == "inandout"):
            finalCode.append("lw $t0 ,($t0)")
            finalCode.append("sw $t" + str(r) + " ,($t0)")
    else:
        print ("aderfeeeeee ti vazeis sthn storerv ? ")

quadCount = 0
def finalCodeGenerator():
    global finalCode
    parameterNum = 0
    currentFunction=""
    for i in range(quadCount, len(quads)):
        finalCode.append("L" + str(i) + ":")
        if(quads[i][0] == "+" or quads[i][0] == "-" or quads[i][0] == "*" or quads[i][0] == "/"):
            loadvr(quads[i][1],1)
            loadvr(quads[i][2],2)
            finalCode.append(matchOperator(quads[i][0]) + " $t1, $t1, $t2")
            storerv(1,quads[i][3])
        elif quads[i][0] == "<" or quads[i][0] == ">" or quads[i][0] == "<>" or quads[i][0] == "<=" or quads[i][0] == ">=" or quads[i][0] == "=":
            loadvr(quads[i][1],1)
            loadvr(quads[i][2],2)
            finalCode.append(matchRelop(quads[i][0]) + " $t1, $t2, L" + str (quads[i][3]))
        elif quads[i][0] == "jump":
            finalCode.append("j L" + str(quads[i][3]))
        elif quads[i][0] == ":=":
            loadvr(quads[i][1],1)
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
                loadvr(quads[i][1],0)
                finalCode.append("sw $t0, -" + str(12+4*parameterNum) + "($fp)")
            elif quads[i][2] == "REF":
                generateRefParameter(quads[i][1], parameterNum)
            elif quads[i][2] == "RET":
                scope, offset = findScopeAndOffset(quads[i][1])
                finalCode.append("add $t0, $sp, -" + str (offset))
                finalCode.append("sw $t0, -8($fp)")
                parameterNum = parameterNum + 1
        elif quads[i][0] == "call":
                scope, offset = findScopeAndOffset(currentFunction)
                scopeCall, offsetCall = findScopeAndOffset(quads[i][1]) #cope ths klh8eisas
                frameLength = findCurrentOffset()+4
                if scope == scopeCall:
                    finalCode.append("lw $t0, -4($sp)")
                    finalCode.append("sw $t0, -4($fp)")
                else:
                    finalCode.append("sw $sp, -4($fp)")
                #finalCode.replace("_", str(frameLength))
                finalCode = [w.replace("_", str(frameLength)) for w in finalCode]
                finalCode.append("add $sp, $sp, " + str (frameLength))
                finalCode.append("jal L" + str (functionlabels[currentFunction]))
                finalCode.append("add $sp, $sp, -" + str (frameLength))
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
                    finalCode.append("add $sp, $sp, " + str (findCurrentOffset()+4))
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
        functionParameters = len(entities[currentScope-1][len(entities[currentScope-1])-1][3]) #poses parametrous exei h sunarthsh sthn opoia vriskomaste
        for i in range(functionParameters):
            if entities[currentScope][i][0] == parameter: #onoma ths i parametrou
                typeOfPar = entities[currentScope-1][len(entities[currentScope-1])-1][3][i] #save the tye of parameter if it's in the arguments
        if (typeOfPar == "in" or typeOfPar == None):
            finalCode.append("add $t0, $sp, -" + offset)
            finalCode.append("sw $t0, -" + str(12+4*number) + "($fp)")

        elif (typeOfPar == "inout" or typeOfPar == "inandout"):
            finalCode.append("lw $t0 ,-" + str (offset) + "($sp)")
            finalCode.append("sw $t0, -" + str(12+4*number) + "($fp)")

    elif scope < currentScope:
        functionParameters = len(entities[scope-1][len(entities[scope-1])-1][3]) #poses parametrous exei h sunarthsh sthn opoia vriskomaste
        for i in range(functionParameters):
            if entities[scope][i][0] == parameter: #onoma ths i parametrou
                typeOfPar = entities[scope-1][len(entities[scope-1])-1][3][i] #save the tye of parameter if it's in the arguments
        gnvlcode(parameter)
        if (typeOfPar == "in" or typeOfPar == None):
            finalCode.append("sw $t0, -" + str(12+4*parameter) + "($fp)")
        elif (typeOfPar == "inout" or typeOfPar == "inandout"):
            finalCode.append("lw $t0 ,($t0)")
            finalCode.append("sw $t0, -" + str(12+4*parameter) + "($fp)")
    else:
        print("Edw paidia den einai REF")

def matchOperator(oper):
    if oper == "+":
        return "add"
    elif oper == "-":
        return "sub"
    elif oper == "*":
        return "mul"
    else:
        return "div"

def matchRelop(relop):
    if relop == "<":
        return "blt"
    elif relop == ">":
        return "bgt"
    elif relop == "<=":
        return "ble"
    elif relop == ">=":
        return "bge"
    elif relop == "=":
        return "beq"
    else:
        return "bne"


# call function program() for checking, Quads for scopes on the screen and file .C and .int
program()
printCFile()
printQuadsInFile()
#printQuads() #Remove comment to print quads on the screen

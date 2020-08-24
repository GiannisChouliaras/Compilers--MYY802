from met import *
import sys

available_tokens = {'program', 'endprogram', 'declare', 'if', 'then', 'else', 'endif',
                    'dowhile', 'enddowhile', 'while', 'endwhile', 'loop', 'endloop',
                    'exit', 'forcase', 'endforcase', 'incase', 'endincase', 'when',
                    'endwhen', 'default', 'enddefault', 'function', 'endfunction', 'return',
                    'in', 'inout', 'inandout', 'and', 'or', 'not', 'input', 'print'}

def checkExpectedKeywordName(counter, tokenList): return tokenList[counter][0]

def getKeywordName(counter, tokenList): return tokenList[counter][1]

def getCodeFromFileAndCharacterLength():
    with open(sys.argv[1] + ".stl") as file:
        characters = file.read()
    return characters, len(characters)

def appendToTokenList(token, tokenList):
    is_a_token = token in available_tokens
    if is_a_token:
        tokentk = token + "tk"
        tokenList.append([tokentk, token])
        return tokenList
    tokentk = 'idtk'
    token = token[:30]
    tokenList.append([tokentk, token])
    return tokenList

def completeTokenIfIsAlpha(characters, position, total_characters):
    token = characters[position]
    while characters[position].isalpha() or characters[position].isdigit():
        if position == total_characters - 1 : break
        else : position += 1
        if not characters[position].isalpha() and not characters[position].isdigit():
            break
        token = token + characters[position]
    return token, position

def completeTokenIfIsDigit(characters, position, total_characters):
    token = characters[position]
    current_symbol = characters[position]
    while current_symbol.isdigit():
        if position == total_characters -1 : break
        position += 1
        current_symbol = characters[position]
        if current_symbol.isalpha():
            error("cannot write a letter after a number")
        if not current_symbol.isdigit(): break
        token = token + current_symbol
    return token, position

def checkDigitIfValidAndAddToList(token, tokenList):
    number = int(token)
    limit_of_numbers = 32767
    message = f"Invalid number, should be between {-limit_of_numbers} and {limit_of_numbers}"
    if number < -limit_of_numbers or number > limit_of_numbers:
        error(message)
    tokentk = 'constanttk'
    tokenList.append([tokentk, number])
    return tokenList





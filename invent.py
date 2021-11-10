import itertools
from common_environment.control_tokens import If
from string_environment.string_tokens import *

# Generates all permutations of elements in a set where maxLength > len(per) > 1
def generatePermutations(set, maxLength) -> list:
    if (maxLength <= 0):
        return []
    return list(itertools.permutations(set, maxLength)) + generatePermutations(set, maxLength - 1)

# Composes tokens into Invented tokens
# Returns a list of Invented tokens
def inventTokens(tokenSet, maxLength) -> list:
    perms = generatePermutations(tokenSet, maxLength)
    out = []

    # convert these into "invented tokens"
    for p in perms:
        out.append(InventedToken(p))
    
    return out
    
# Composes tokens into more elaborate Invented tokens
# Also generates Invented tokens with if statements
def invent2(tokenSet, boolTokenSet, maxLength) -> list:
    # Normal invention step
    out = generatePermutations(tokenSet, maxLength)

    # Generating if statements
    if maxLength > 3:
        if_list = []
        conditions = boolTokenSet
        bodies = generatePermutations(tokenSet, int(maxLength / 2))  # TODO Arbitrary length!!
        for c in conditions:
            for lb in bodies:
                for rb in bodies:
                    if_list.append(If(c, lb, rb))
        out = out + if_list
    return out


if __name__ == "__main__":
    # Test for string environment
    bool_tokens = {AtStart,	AtEnd, IsLetter, IsNotLetter, IsUppercase,	IsNotUppercase,
                   IsLowercase,	IsNotLowercase,	IsNumber,	IsNotNumber,	IsSpace,	IsNotSpace}
    normal_tokens = {MoveRight, MoveLeft, Drop, MakeLowercase, MakeUppercase}
    for t in invent2(normal_tokens, bool_tokens, 7):
        print(t)

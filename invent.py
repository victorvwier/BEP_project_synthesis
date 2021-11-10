import itertools
from common_environment.control_tokens import If
from string_environment.string_tokens import *

# Takes a list of tokens and returns a list of all permutations where len(tokenSet) > len(per) > 1
def generatePermutations(tokenSet, maxLength) -> list:
    if (maxLength <= 1):
        return []
    return list(itertools.permutations(tokenSet, maxLength)) + generatePermutations(tokenSet, maxLength - 1)

def inventTokens(tokenSet, maxLength) -> list:
    perms = generatePermutations(tokenSet, maxLength)
    out = []
    # convert these into "invented tokens"
    

def invent2(tokenSet, boolTokenSet, maxLength) -> list:
    # Normal invention step
    out = generatePermutations(tokenSet, maxLength)

    # Generating if statements
    if maxLength > 3:
        if_list = []
        conditions = boolTokenSet
        bodies = generatePermutations(tokenSet, int(maxLength / 2))
        for c in conditions:
            for lb in bodies:
                for rb in bodies:
                    #if_list.append(["IF", c, lb, rb])
                    if_list.append(If(c, lb, rb))
        out = out + if_list
    return out


if __name__ == "__main__":
    # Test for string environment
    bool_tokens = {AtStart,	AtEnd, IsLetter, IsNotLetter, IsUppercase,	IsNotUppercase,
                   IsLowercase,	IsNotLowercase,	IsNumber,	IsNotNumber,	IsSpace,	IsNotSpace}
    iftoken = "IF"
    normal_tokens = {MoveRight, MoveLeft, Drop, MakeLowercase, MakeUppercase}
    for t in invent2(normal_tokens, bool_tokens, 7):
        print(t)

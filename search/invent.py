import itertools
from common.tokens.control_tokens import If, LoopWhile
from common.tokens.string_tokens import *


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
        if len(p) > 1:
            p = list(map(lambda x: x, p))
            out.append(InventedToken(p))
        else:
            out.append(p[0])

    return out


# Composes tokens into more elaborate Invented tokens
# Also generates If and While tokens
def invent2(tokenSet, boolTokenSet, maxLength) -> list:
    # Normal invention step
    out = inventTokens(tokenSet, maxLength)

    # Generating if statements
    if_list = []
    conditions = boolTokenSet
    bodies = inventTokens(tokenSet, max(1, int(maxLength / 2)))  # TODO Arbitrary length!!
    for c in conditions:
        for lb in bodies:
            for rb in bodies:
                if_list.append(If(c, [lb], [rb]))
    out = out + if_list

    # Generating recurse statements
    # recurse_list = []
    # conditions = boolTokenSet
    # conditions
    # bodies = inventTokens(tokenSet, max(1, int(maxLength / 2)))  # TODO Arbitrary length!!
    # for c in conditions:
    #     for lb in bodies:
    #         for rb in bodies:
    #             recurse_list.append(Recurse(c(), [lb], [rb]))
    #         recurse_list.append(Recurse(c(), [lb], []))
    #         recurse_list.append(Recurse(c(), [], [lb]))

    # for lb in bodies:
    #     for rb in bodies:
    #         recurse_list.append(Recurse(None, [lb], [rb]))
    #     recurse_list.append(Recurse(None, [lb], []))
    #     recurse_list.append(Recurse(None, [], [lb]))
    # out = out + recurse_list
    loop_list = []
    # bodies = inventTokens(tokenSet, max(1, int(maxLength / 2)))  # TODO Arbitrary length!!
    bodies = inventTokens(tokenSet, 2)  # TODO Arbitrary length!!
    for c in conditions:
        for lb in bodies:
            loop_list.append(LoopWhile(c, [lb]))
    out = out + loop_list
    return out


if __name__ == "__main__":
    # Test for string environment
    bool_tokens = {AtStart, AtEnd, IsLetter, IsNotLetter, IsUppercase, IsNotUppercase, IsLowercase, IsNotLowercase,
                   IsNumber, IsNotNumber, IsSpace, IsNotSpace}
    normal_tokens = {MoveRight(), MoveLeft(), Drop(), MakeLowercase(), MakeUppercase()}

    tokens = inventTokens(normal_tokens, 4)
    # print(len(tokens))
    tokens = invent2(normal_tokens, bool_tokens, 2)
    print("\n".join([str(t) for t in tokens]))
    print(len(tokens))

    # out = invent2(normal_tokens, bool_tokens, 5)
    # print(len(out))
    # for t in out:
    #     if (not isinstance(t, Token)):
    #         print(t)

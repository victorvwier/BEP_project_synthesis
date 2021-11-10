import itertools

# Takes a list of tokens and returns a list of all permutations where len(tokenSet) > len(per) > 1 
def invent(tokenSet, maxLength):
    if (maxLength <= 1):
        return []
    return list(itertools.permutations(tokenSet, maxLength)) + invent(tokenSet, maxLength - 1)

def invent2(tokenSet, boolTokenSet, maxLength):
    # Normal invention step
    out = invent(tokenSet, maxLength)
    
    # Generating if statements
    if maxLength > 3:
        if_list = []
        conditions = boolTokenSet
        bodies = invent(tokenSet, int(maxLength / 2))
        for c in conditions:
            for lb in bodies:
                for rb in bodies:
                    if_list.append(["IF", c, lb, rb])
        out = out + if_list
    return out

if __name__ == "__main__":
    iftoken = "IF"
    bool_tokens = {"TRUE", "FALSE", "MAYBE"}
    normal_tokens = {"UP", "DOWN", "LEFT", "RIGHT", "PICKUP", "DROP"}
    for t in invent2(normal_tokens, bool_tokens, 7):
        print(t)
    

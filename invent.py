import itertools

# Takes a list of tokens and returns a list of all permutations where len(tokenSet) > len(per) > 1 
def invent(tokenSet, maxLength):
    if (maxLength <= 1):
        return []
    return list(itertools.permutations(tokenSet, maxLength)) + invent(tokenSet, maxLength - 1)


if __name__ == "__main__":
    print(invent({"UP", "DOWN", "LEFT", "RIGHT", "PICKUP", "DROP"}, 3))
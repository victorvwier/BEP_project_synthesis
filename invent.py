import itertools

def invent(tokenSet, maxLength):
    if (maxLength <= 1):
        return []
    return list(itertools.permutations(tokenSet, maxLength)) + invent(tokenSet, maxLength - 1)
        

    
if __name__ == "__main__":
    print(invent({"A", "B", "C", "D", "E", "F", "G"}, 4))
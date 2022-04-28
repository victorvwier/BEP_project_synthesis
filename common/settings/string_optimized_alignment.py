from common.settings.settings import Settings
from common.environment.string_environment import StringEnvironment
from common.tokens.string_tokens import TransTokens, BoolTokens


class StringOptimizedAlignment(Settings):
    """Sequence alignment settings measure"""

    """Maps (string, string) pairs to their levenshtein settings."""
    _map = {}

    def __init__(self):
        super().__init__("string", TransTokens, BoolTokens)

    def distance(self, inp: StringEnvironment, out: StringEnvironment) -> float:
        return self._alignment("".join(inp.string_array), "".join(out.string_array))

    @staticmethod
    def _alignment(inp, out):
        """Sequence alignment algorithm."""

        if (inp, out) in StringOptimizedAlignment._map:
            return StringOptimizedAlignment._map[(inp, out)]

        m = len(inp)
        n = len(out)

        if m == 0:
            result = 0 if n == 0 else float("inf")

        elif n == 0:
            result = m

        elif inp[0] == out[0]:
            result = StringOptimizedAlignment._alignment(inp[1:], out[1:])

        elif inp[0].lower() == out[0].lower():
            result = 1 + StringOptimizedAlignment._alignment(inp[1:], out[1:])


        else:
            result = 1 + StringOptimizedAlignment._alignment(inp[1:], out)

        StringOptimizedAlignment._map[(inp, out)] = result
        return result

        """

        mem = [float('inf')] * (m + 1)
        for i in range(m + 1):
            mem[i] = [float('inf')] * (n + 1)
        for i in range(m + 1):
            mem[i][0] = i * 1
        for j in range(1, n + 1):
            mem[0][j] = float('inf')
        for j in range(1, n + 1):
            for i in range(1, m + 1):
                cases = []
                if x[i - 1] == y[j - 1]:
                    cases.append(mem[i - 1][j - 1])
                elif x[i - 1].lower() == y[j - 1].lower():
                    cases.append(1 + mem[i - 1][j - 1])
                cases.append(1 + mem[i - 1][j])
                cases.append(float('inf'))
                mem[i][j] = min(cases)
        return mem[m][n]
        """

if __name__ == "__main__":
    ios = [
        ("AB", "AB", 0),
        ("AB", "A", 1),
        ("AB", "B", 1),
        ("AB", "", 2),

        ("AB", "Ab", 1),
        ("AB", "aB", 1),
        ("AB", "ab", 2),
        ("AB", "a", 2),
        ("AB", "b", 2),

        ("ab", "aB", 1),
        ("ab", "Ab", 1),
        ("ab", "AB", 2),
        ("ab", "A", 2),
        ("ab", "B", 2),

        ("AB", "C", -1),
        ("AB", "AA", -1),
        ("AB", "BB", -1),
        ("AB", "ABB", -1),
        ("AB", "AAB", -1),
        ("A", "AB", -1),
        ("B", "AB", -1),
        ("", "AB", -1),
    ]

    for (i, o, e) in ios:
        if e == -1:
            e = float("inf")
        print("\"{}\" -> \"{}\": {}".format(i, o, StringOptimizedAlignment._alignment(i, o) == e))


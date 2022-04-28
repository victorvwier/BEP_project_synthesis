from common.settings.settings import Settings
from common.environment.string_environment import StringEnvironment
from common.tokens.string_tokens import TransTokens, BoolTokens


class StringLevenshtein(Settings):
    """Levenshtein settings for StringEnvironment."""

    """Maps (string, string) pairs to their levenshtein settings."""
    _map = {}

    def __init__(self):
        super().__init__("string", TransTokens, BoolTokens)

    def distance(self, inp: StringEnvironment, out: StringEnvironment) -> float:
        return self._levenshtein("".join(inp.string_array), "".join(out.string_array))

    @staticmethod
    def _levenshtein(s1, s2):
        """Calculates the levenshtein settings recursively."""

        if (s1, s2) in StringLevenshtein._map:
            return StringLevenshtein._map[(s1, s2)]

        m = len(s1)
        n = len(s2)

        if m == 0:
            result = n

        elif n == 0:
            result = m

        elif s1[0] == s2[0]:
            result = StringLevenshtein._levenshtein(s1[1:], s2[1:])

        else:
            result = 1 + min(
                StringLevenshtein._levenshtein(s1[1:], s2),
                StringLevenshtein._levenshtein(s1, s2[1:]),
                StringLevenshtein._levenshtein(s1[1:], s2[1:])
            )

        StringLevenshtein._map[(s1, s2)] = result
        return result

    @staticmethod
    def _levenshtein_slow(str1, str2):
        m = len(str1)
        n = len(str2)
        d = [[i] for i in range(1, m + 1)]  # d matrix rows
        d.insert(0, list(range(0, n + 1)))  # d matrix columns
        for j in range(1, n + 1):
            for i in range(1, m + 1):
                if str1[i - 1] == str2[j - 1]:  # Python (string) is 0-based
                    substitutionCost = 0
                else:
                    substitutionCost = 1
                d[i].insert(j, min(d[i - 1][j] + 1,
                                   d[i][j - 1] + 1,
                                   d[i - 1][j - 1] + substitutionCost))
        return d[-1][-1]

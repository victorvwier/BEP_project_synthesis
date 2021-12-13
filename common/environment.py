from dataclasses import dataclass
import re


@dataclass(eq=True, unsafe_hash=True)
class Environment:
    """Abstract Environment class."""

    def __init__(self):
        self.program = None

    def distance(self, other: "Environment") -> float:
        """Returns the distance from this Environment to some other object."""
        raise NotImplementedError()

    def __deepcopy__(self, memdict={}):
        raise NotImplementedError()

    def correct(self, other: "Environment") -> bool:
        """Returns whether this state is the desired one given a desired output Environment."""
        raise NotImplementedError()

    def loop_limit(self) -> int:
        """Returns the max amount of loop iterations based on the environment."""
        return 100


@dataclass(eq=True)
class RobotEnvironment(Environment):
    """Environment for the robot. A robot lives on a square matrix in which it needs to pick up a ball lying somewhere
    in that same matrix."""
    size: int
    rx: int
    ry: int
    bx: int
    by: int
    holding: bool

    def __init__(self, size: int, rx: int, ry: int, bx: int, by: int, holding=False):
        """Creates new RobotEnvironment given a size, initial position of the robot (rx, ry), position of the ball
        (bx, by) and whether the robot is holding the ball."""
        super().__init__()

        self.size = size
        self.rx = rx
        self.ry = ry
        self.bx = bx
        self.by = by
        self.holding = holding

        assert (not holding or (rx == bx and ry == by))
        
    def __deepcopy__(self, memdict={}):
        return RobotEnvironment(self.size, self.rx, self.ry, self.bx, self.by, self.holding)

    def __str__(self):
        return "RobotEnvironment(Robot: (%s, %s), Bal: (%s, %s), Holding: %s, Size: %s)" % \
               (self.rx, self.ry, self.bx, self.by, self.holding, self.size)

    @staticmethod
    def parse(string_encoding: str) -> 'RobotEnvironment':
        # regex = r'RobotEnvironment\(\((?P<x>.*), (?P<y>.*)\), (?P<pixels>.*)\)'
        regex = r'RobotEnvironment\(Robot: \((?P<rx>.*), (?P<ry>.*)\), Bal: \((?P<bx>.*), (?P<by>.*)\), Holding: (?P<holding>.*), Size: (?P<size>.*)\)'
        args = re.search(regex, string_encoding).groupdict()
        rx = int(args['rx'])
        ry = int(args['ry'])
        bx = int(args['bx'])
        by = int(args['by'])
        holding = eval(args['holding'])
        size = int(args['size'])
        return RobotEnvironment(size, rx, ry, bx, by, holding)

    def __hash__(self):
        return hash((self.rx, self.ry, self.bx, self.by, self.holding, self.size))

    def original_distance(self, other: "RobotEnvironment") -> int:
        """
        Heurists that was originally used by Brute
        @param other:
        @return:
        """
        return abs(self.bx - other.bx) + abs(self.by - other.by)\
        + abs(self.rx - other.rx) + abs(self.ry - other.ry)\
        + abs(int(self.holding) - int(other.holding))

    def distance(self, other: "RobotEnvironment") -> int:
        assert self.size == other.size

        def d(xy1: 'tuple[int, int]', xy2: 'tuple[int, int]'):
            return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

        # position robot and position ball
        pr = (self.rx, self.ry)
        pb = (self.bx, self.by)

        # position goal robot and position goal bal
        pgr = (other.rx, other.ry)
        pgb = (other.bx, other.by)

        if pr != pb and pb != pgb:
            return d(pr, pb) + d(pb, pgb) + d(pgb, pgr) + 2
        elif pr == pb and pb != pgb:
            return d(pr, pgb) + d(pgb, pgr) + 1
        else:
            return d(pr, pgr)

    def correct(self, other: "RobotEnvironment") -> bool:
        return (self.rx, self.ry, self.bx, self.by, self.holding) \
               == (other.rx, other.ry, other.bx, other.by, other.holding)

    def to_formatted_string(self):
        char_empty = chr(11034)  # ⬚
        char_robot = chr(9632)  # ■ robot possibly holding ball
        char_ball = chr(9675)  # ○
        char_robot_on_ball = chr(9689)  # ◙ robot not holding ball
        rows = []
        for y in range(self.size):
            row = []
            for x in range(self.size):
                char = char_empty
                if (x, y) == (self.bx, self.by):
                    char = char_ball
                if (x, y) == (self.rx, self.ry):
                    char = char_robot
                if (x, y) == (self.bx, self.by) == (self.rx, self.ry) and not self.holding:
                    char = char_robot_on_ball
                row.append(char)
            rows.append(" ".join(row))
        result = "\n".join(rows[::-1])
        return result


@dataclass(eq=True)
class StringEnvironment(Environment):
    """Environment for string manipulation."""
    string_array: list[str]
    pos: int

    def __init__(self, string_array: list[str], pos: int = 0):
        """Creates new StringEnvironment given an initial string and starting position of the pointer, 0 by default."""
        super().__init__()

        # Manipulating strings as a list of characters is more efficient.
        self.string_array = string_array
        self.pos = pos
        
        assert 0 <= pos < len(string_array) or len(string_array) == 0

    def to_string(self) -> str:
        """Returns the string of this Environment. For efficiency strings are internally stored as an array instead of
        string, therefore this conversion method exists."""
        return "".join(self.string_array)

    def __deepcopy__(self, memdict={}):
        return StringEnvironment(string_array=copy.copy(self.string_array), pos=self.pos)

    def __hash__(self):
        return hash((self.to_string(), self.pos))

    @staticmethod
    def parse(string_encoding: str) -> 'StringEnvironment':
        regex = r'StringEnvironment\(Pointer at (?P<pos>.*) in "(?P<string>.*)"\)'
        args = re.search(regex, string_encoding).groupdict()
        return StringEnvironment(args['string'], int(args['pos']))

    @staticmethod
    def _levenshtein(str1, str2):
        m = len(str1)
        n = len(str2)
        d = [[i] for i in range(1, m + 1)]   # d matrix rows
        d.insert(0, list(range(0, n + 1)))   # d matrix columns
        for j in range(1, n + 1):
            for i in range(1, m + 1):
                if str1[i - 1] == str2[j - 1]:   # Python (string) is 0-based
                    substitutionCost = 0
                else:
                    substitutionCost = 1
                d[i].insert(j, min(d[i - 1][j] + 1,
                                d[i][j - 1] + 1,
                                d[i - 1][j - 1] + substitutionCost))
        return d[-1][-1]

    @staticmethod
    def _alignment(x, y):
        """
        Alternative to the Levenshtein distance
        @param x:
        @param y:
        @return:
        """
        m = len(x)
        n = len(y)
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
                if x[i-1] == y[j-1]:
                    cases.append(mem[i-1][j-1])
                elif x[i-1].lower() == y[j-1].lower():
                    cases.append(1 + mem[i-1][j-1])
                cases.append(1 + mem[i-1][j])
                cases.append(float('inf'))
                mem[i][j] = min(cases)
        return mem[m][n]

    distance_map = {}

    @staticmethod
    def _levenshtein_eff(s1, s2):
        if (s1, s2) not in StringEnvironment.distance_map:
            StringEnvironment.distance_map[(s1, s2)] = StringEnvironment._levenshtein_rec(s1, s2)

        return StringEnvironment.distance_map[(s1, s2)]

    @staticmethod
    def _levenshtein_rec(s1, s2):
        m = len(s1)
        n = len(s2)

        if m == 0:
            return n

        if n == 0:
            return m

        if s1[0] == s2[0]:
            return StringEnvironment._levenshtein_eff(s1[1:], s2[1:])

        return 1 + min(
            StringEnvironment._levenshtein_eff(s1[1:], s2),
            StringEnvironment._levenshtein_eff(s1, s2[1:]),
            StringEnvironment._levenshtein_eff(s1[1:], s2[1:])
        )

    def distance(self, other: "StringEnvironment") -> int:
        s1 = "".join(self.string_array)
        s2 = "".join(other.string_array)

        if (s1, s2) not in self.distance_map:
            self.distance_map[(s1,s2)] = self._levenshtein_eff(s1, s2)

        return self.distance_map[(s1,s2)]

    def correct(self, other: "StringEnvironment") -> bool:
        return self.to_string() == other.to_string()

    def loop_limit(self) -> int:
        return max(self.pos, len(self.string_array) - self.pos)

    def __str__(self):
        return "StringEnvironment(Pointer at {pos} in \"{string_array}\")".format(pos=self.pos, string_array=self.to_string())

    def to_formatted_string(self):
        arrow = ["^" if i == self.pos else " " for i in range(len(self.string_array))]
        result = self.to_string()
        if result:
            result += ("\n" + " " * self.pos + "^" + str(self.pos))
        else:
            result = "(empty string)"
        return result

    @staticmethod
    def parse(string_encoding: str) -> 'StringEnvironment':
        regex = r'StringEnvironment\(Pointer at (?P<pos>.*) in "(?P<string>.*)"\)'
        args = re.search(regex, string_encoding).groupdict()
        return StringEnvironment(args['string'], int(args['pos']))


@dataclass(eq=True, unsafe_hash=True)
class PixelEnvironment(Environment):
    width: int
    height: int
    x: int
    y: int
    pixels: tuple[bool]

    def __init__(self, width, height, x, y, pixels=None):
        super().__init__()

        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.pixels = pixels or tuple(False for _ in range(width * height))
        assert 0 <= x < width
        assert 0 <= y < height

    def __str__(self):
        return "PixelEnvironment((%s, %s), %s)" % (self.x, self.y, self.pixels)

    @staticmethod
    def parse(string_encoding: str) -> 'PixelEnvironment':
        regex = r'PixelEnvironment\(\((?P<x>.*), (?P<y>.*)\), (?P<pixels>.*)\)'
        args = re.search(regex, string_encoding).groupdict()
        x = int(args['x'])
        y = int(args['y'])
        pixels = eval(args['pixels'])
        width = len(pixels)
        height = len(pixels[0]) if pixels else 0
        return PixelEnvironment(width, height, x, y, pixels)

    def __deepcopy__(self, memdict={}):
        return PixelEnvironment(self.width, self.height, self.x, self.y, self.pixels)

    @staticmethod
    def _hamming_distance(tup1: tuple, tup2: tuple):
        assert len(tup1) == len(tup2)
        return sum([e1 != e2 for (e1, e2) in zip(tup1, tup2)])

    def correct(self, other: "PixelEnvironment") -> bool:
        return self.pixels == other.pixels

    def distance(self, other: "PixelEnvironment") -> int:
        return self._hamming_distance(self.pixels, other.pixels)

    def to_formatted_string(self):
        char_empty = chr(11034)  # ⬚
        char_filled = chr(9632)  # ■
        char_pointer_empty = chr(9675)  # ○
        char_pointer_filled = chr(9679)  # ●
        rows = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                pos = self.width * y + x
                char = char_filled if self.pixels[pos] else char_empty
                if (self.x, self.y) == (x, y):
                    char = char_pointer_filled if self.pixels[pos] else char_pointer_empty
                row.append(char)
            rows.append(" ".join(row))
        result = "\n".join(rows)
        return result

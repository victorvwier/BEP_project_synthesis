class Environment:
    def distance(self, other) -> float:
        raise NotImplementedError()

class RobotEnvironment(Environment):
    def __init__(self, size, rx, ry, bx, by, holding = False):
        self.size = size
        self.rx = rx
        self.ry = ry
        self.bx = bx
        self.by = by
        self.holding = holding

class StringEnvironment(Environment):
    def __init__(self, string, pos = 0):
        self.string = string
        self.pos = pos

class PixelEnvironment(Environment):
    def __init__(self, size, x, y, pixels):
        self.size = size
        self.x = x
        self.y = y
        self.pixels = pixels
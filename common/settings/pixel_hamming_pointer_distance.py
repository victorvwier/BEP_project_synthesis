from common.settings.settings import Settings
from common.environment.pixel_environment import PixelEnvironment
from common.tokens.pixel_tokens import TransTokens, BoolTokens


class PixelHammingPointerDistance(Settings):
    """Hamming settings for pixel environments."""

    def __init__(self):
        super().__init__("pixel", TransTokens, BoolTokens)

    def distance(self, inp: PixelEnvironment, out: PixelEnvironment) -> float:
        def f(e1, e2):
            if not e1 and e2:
                return 1

            if e1 and not e2:
                return float('inf')

            return 0

        return sum([f(e1, e2) for (e1, e2) in zip(inp.pixels, out.pixels)])

    def distance_n(self, inp: PixelEnvironment, out: PixelEnvironment) -> float:
        assert len(inp.pixels) == len(out.pixels)

        #min_d_pointer = float('inf')

        distance = 0

        for x in range(inp.width):
            for y in range(inp.height):
                pos = inp.width * y + x

                #distance += inp.pixels[pos] != out.pixels[pos]

                if inp.pixels[pos] and not out.pixels[pos]:
                    #distance += 5
                    #return inp.height * inp.width
                    return float("inf")

                #if not inp.pixels[pos] and out.pixels[pos]:
                    #min_d_pointer = min(abs(inp.x - x) + abs(inp.y - y), min_d_pointer)

        if distance == 0:
            return 0

        return distance# + min_d_pointer

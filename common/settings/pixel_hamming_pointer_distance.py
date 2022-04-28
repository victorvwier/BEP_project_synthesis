from common.settings.settings import Settings
from common.environment.pixel_environment import PixelEnvironment
from common.tokens.pixel_tokens import TransTokens, BoolTokens


class PixelHammingPointerDistance(Settings):
    """Hamming settings for pixel environments."""

    def __init__(self):
        super().__init__("pixel", TransTokens, BoolTokens)

    def distance(self, inp: PixelEnvironment, out: PixelEnvironment) -> float:
        assert len(inp.pixels) == len(out.pixels)

        min_d_pointer = float('inf')

        distance = 0

        for x in range(inp.width):
            for y in range(inp.height):
                pos = inp.width * y + x

                distance += inp.pixels[pos] == out.pixels[pos]

                if not inp.pixels[pos] and out.pixels[pos]:
                    min_d_pointer = min(abs(inp.x - x) + abs(inp.y - y), min_d_pointer)

        if distance == 0:
            return 0

        return distance + min_d_pointer / (inp.height + inp.width)

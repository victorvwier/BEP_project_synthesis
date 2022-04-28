from common.environment.pixel_environment import PixelEnvironment
from common.settings.settings import Settings
from common.tokens.pixel_tokens import TransTokens, BoolTokens


class PixelEntailment(Settings):

    def __init__(self):
        super().__init__("pixel", TransTokens, BoolTokens)

    def distance(self, inp: PixelEnvironment, out: PixelEnvironment) -> float:
        return 0 if inp.pixels == out.pixels else 1

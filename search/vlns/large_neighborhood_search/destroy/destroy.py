from common.prorgam import Program, EnvToken


class Destroy:
    """Interface for destroy methods."""

    def destroy(self, program: Program) -> list[list[EnvToken]]:
        """Destructs a given program. Returns a list of token sequences."""

        raise NotImplementedError()

    def set_search_depth(self, n: int):
        pass

    def increment_search_depth(self):
        pass
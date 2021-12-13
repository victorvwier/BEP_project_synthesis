from common.prorgam import Program


class Accept():
    """Abstract class for accept method in LNS."""

    def accept(self, cost_current: float, cost_temporary: float, program_current: Program, program_temporary: Program, iteration: int) -> bool:
        """Returns whether the temporary solution should be accepted based on the costs `cost_current` and
        `cost_temporary`."""

        raise NotImplementedError()

    def reset(self):
        pass

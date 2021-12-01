from common.prorgam import Program
from search.vlns.large_neighborhood_search.tokens.sequence_token import SequenceToken, SeqToken


class Destroy:
    """Interface for a Destroy method."""

    def destroy(self, solution: Program) -> SeqToken:
        """Destructs a given 'solution'. Returns a SequenceToken containing, among others, DestroyedTokens."""

        seq = SequenceToken.from_list(solution.sequence)
        return self.destroy_sequence(seq)

    def destroy_sequence(self, seq: SeqToken) -> SeqToken:
        """Destroys a given SequenceToken. Should return the destroyed SequenceToken"""

        raise NotImplementedError()

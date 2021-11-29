from string_environment.string_tokens import *
from vlns.large_neighborhood_search.implementations.greedy_lns.probabilistic_destroy import ProbabilisticProgramDestroy, \
    EnvToken, If, LoopWhile, InventedToken, Program
from vlns.large_neighborhood_search.implementations.wat_is_een_goeie_naam.marked_token import MarkedEnvToken, \
    MarkedBoolToken, IdToken


class ProbabilisticDestroyExpandingSequences(ProbabilisticProgramDestroy):
    """This Destroy method marks tokens with a given probability. Marked tokens are to be destructed. A new marked token
    is appended after each sequence so the program can expand."""

    def _destroy_sequence(self, tokens: list[EnvToken]) -> list[EnvToken]:
        # Destroys an entire sequence of EnvTokens.
        destroyed_seq = []

        for t in tokens:
            if self._p():
                destroyed_seq.append(MarkedEnvToken(t))
            elif isinstance(t, If):
                cond = MarkedBoolToken(t.cond) if self._p(False) else t.cond
                e1 = self._destroy_sequence(t.e1)
                e2 = self._destroy_sequence(t.e2)

                destroyed_seq.append(If(cond, e1, e2))
            elif isinstance(t, LoopWhile):
                cond = MarkedBoolToken(t.cond) if self._p(False) else t.cond
                loop_body = self._destroy_sequence(t.loop_body)

                destroyed_seq.append(LoopWhile(cond, loop_body))
            elif isinstance(t, InventedToken):
                n_seq = self._destroy_sequence(t.tokens)[:-1]
                destroyed_seq.append(InventedToken(n_seq))
            else:
                destroyed_seq.append(t)

        destroyed_seq.append(MarkedEnvToken(IdToken()))

        return destroyed_seq


if __name__ == "__main__":
    p1 = Program([
        MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft(),
        LoopWhile(
            AtStart(),
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft()]
        ),
        If(
            AtStart(),
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft()],
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft()]
        ),
    ])

    p2 = Program([
        InventedToken(
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft()]
        )
    ])

    d = ProbabilisticDestroyExpandingSequences(prob=0.2, p_env=0, p_bool=0)

    np = d.destroy(p2)

    print(str(np))
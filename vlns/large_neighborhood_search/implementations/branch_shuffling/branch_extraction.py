from common_environment.control_tokens import If
from interpreter.interpreter import Program
from string_environment.string_tokens import *
from vlns.large_neighborhood_search.destroy import Destroy


class BranchExtraction(Destroy[list[list[EnvToken]]]):

    def destroy(self, solution: Program) -> list[list[EnvToken]]:
        if (len(solution.sequence)) == 0:
            return []

        return self._destroy_seq(solution.sequence)

    def _destroy_seq(self, seq: list[EnvToken]) -> list[list[EnvToken]]:
        res_seqs = []

        if not isinstance(seq[0], ControlToken):
            res_seqs.append(self._pop_leading_branch(seq))

        while len(seq) != 0:
            t = seq.pop(0)

            if isinstance(t, If):
                res_seqs += self._destroy_seq(t.e1)
                res_seqs += self._destroy_seq(t.e2)
            elif isinstance(t, LoopWhile):
                res_seqs += self._destroy_seq(t.loop_body)

            if len(seq) != 0:
                res_seqs.append(self._pop_leading_branch(seq))

        return res_seqs

    @staticmethod
    def _pop_leading_branch(seq: list[EnvToken]) -> list[EnvToken]:
        res_seq = []

        while len(seq) != 0 and not isinstance(seq[0], (If, LoopWhile)):
            res_seq.append(seq.pop(0))

        return res_seq

if __name__ == "__main__":
    p1 = Program([
        MoveRight(), MoveLeft(), MoveLeft(), MoveLeft(),
        LoopWhile(
            AtStart(),
            [MoveLeft(), MoveRight(), MoveLeft(), MoveLeft()]
        ),
        If(
            AtStart(),
            [MoveLeft(), MoveLeft(), MoveRight(), MoveLeft()],
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveRight()]
        ),
        MoveLeft(), MoveLeft(), MoveLeft(), MoveRight()
    ])

    p2 = Program([If(
        AtStart(),
        [Drop()],
        [MoveLeft()]
    )])

    d = BranchExtraction()

    print(d.destroy(p2))
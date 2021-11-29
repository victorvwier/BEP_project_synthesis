import random

from common_environment.control_tokens import If
from interpreter.interpreter import Program
from string_environment.string_tokens import *
from vlns.large_neighborhood_search.destroy.block_destroy import BlockDestroy
from vlns.large_neighborhood_search.destroy.destroy import Destroy
from vlns.large_neighborhood_search.destroy.sequence_destroy import SequenceDestroy
from vlns.large_neighborhood_search.destroy.single_destroy import SingleDestroy


class MultiMethodDestroy(Destroy):

    def destroy(self, solution: Program) -> list[Token]:
        if not self.differ_method_per_sequence:
            self._select_method()

        return self._destroy_seq(solution.sequence)

    def __init__(self, methods: list[Destroy], weights: list[int], differ_method_per_sequence: bool = False):
        self.methods = methods
        self.weights = weights
        self.differ_method_per_sequence = differ_method_per_sequence

        self.method = methods[0]

    def seq_setup(self, seq: list[Token]):
        if self.differ_method_per_sequence:
            self._select_method()

        print(self.method)
        print(seq)

        self.method.seq_setup(seq)

    def destroy_env_if(self, seq: list[Token], token: Token, index: int) -> bool:
        return self.method.destroy_env_if(seq, token, index)

    def destroy_bool_if(self, seq: list[Token], token: Token, control_token: Token, index: int) -> bool:
        return self.method.destroy_bool_if(seq, token, control_token, index)

    def _select_method(self):
        self.method = random.choices(self.methods, weights=self.weights, k=1)[0]

if __name__ == "__main__":
    p = Program([
        MoveLeft(), MoveRight(), MakeUppercase(), MakeLowercase(),
        LoopWhile(
            AtStart(),
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft()]
        ),
        If(
            AtStart(),
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft()],
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft()]
        ),
        MoveLeft(), MoveRight(), MakeUppercase(), MakeLowercase(),
    ])

    d = MultiMethodDestroy(
        methods=[
            SingleDestroy(p_env=0.15, p_bool=0.0),
            SequenceDestroy(p_destroy=0.5, max_seq_size=3),
            BlockDestroy(p_destroy=1)
        ],
        weights=[1, 1, 1],
        differ_method_per_sequence=True
    )

    d.destroy(p)

    print(str(p))
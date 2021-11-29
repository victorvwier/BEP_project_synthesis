from collections import Iterator

from common_environment.abstract_tokens import Token
from common_environment.control_tokens import If, LoopWhile
from interpreter.interpreter import Program
from string_environment.string_tokens import *


class ProgramIterator(Iterator):
    def __init__(self, program: Program):
        self.program = program

    def __next__(self) -> Token:
        if len(self._seq) == 0:
            raise StopIteration

        return self._seq.pop(0)

    def __iter__(self):
        self._seq = []
        self._add_seq(self.program.sequence)

        return self

    def _add_seq(self, seq: list[Token]):
        for t in seq:
            self._seq.append(t)

            if isinstance(t, If):
                self._seq.append(t.cond)
                self._add_seq(t.e1)
                self._add_seq(t.e2)
            elif isinstance(t, LoopWhile):
                self._seq.append(t.cond)
                self._add_seq(t.loop_body)


if __name__ == "__main__":
    p = Program([
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

    for t in ProgramIterator(p):
        print(t)
from collections import deque
from typing import Deque

from common.environment import Environment
from common.tokens.abstract_tokens import EnvToken, Token
from common.tokens.control_tokens import If, LoopWhile


class SeqToken(EnvToken):

    def apply(self, env: Environment):
        return env

    def __len__(self):
        raise NotImplementedError()

    def to_list(self) -> list[EnvToken]:
        raise NotImplementedError()


class EmptySequenceToken(SeqToken):
    def __len__(self):
        return 0

    def __str__(self):
        return "End"

    def to_list(self) -> list[EnvToken]:
        return []


class SequenceToken(SeqToken):

    def __init__(self, head: EnvToken, tail: SeqToken):
        self.head = head
        self.tail = tail

        self._len = 1 + len(tail)

    @staticmethod
    def from_list(seq: list[EnvToken]) -> SeqToken:
        return SequenceToken.from_deque(deque(seq))

    @staticmethod
    def from_deque(seq: Deque[EnvToken]) -> SeqToken:
        if len(seq) == 0:
            return EmptySequenceToken()

        head = seq.popleft()

        if isinstance(head, If):
            head.e1 = [SequenceToken.from_list(head.e1)]
            head.e2 = [SequenceToken.from_list(head.e2)]
        elif isinstance(head, LoopWhile):
            head.loop_body = [SequenceToken.from_list(head.loop_body)]

        return SequenceToken(head, SequenceToken.from_deque(seq))

    def apply(self, env: Environment) -> Environment:
        return self.tail.apply(self.head.apply(env))

    def __str__(self):
        return "{}, {}".format(self.head, self.tail)

    def __len__(self):
        return self._len

    def to_list(self) -> list[EnvToken]:
        if isinstance(self.head, RemoveToken):
            return self.tail.to_list()

        t = self
        res = []

        while isinstance(t, SequenceToken):
            h = t.head

            if isinstance(h, RemoveToken):
                t = t.tail
                continue
            elif isinstance(h, If):
                h.e1 = h.e1[0].to_list()
                h.e2 = h.e2[0].to_list()
            elif isinstance(h, LoopWhile):
                h.loop_body = h.loop_body[0].to_list()

            res.append(h)
            t = t.tail

        return res


class RemoveToken(EnvToken):

    def apply(self, env: Environment) -> Environment:
        return env


class NoTailException(Exception):
    pass

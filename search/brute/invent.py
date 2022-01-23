import heapq
import itertools
from common.tokens.control_tokens import If, LoopWhile
from common.tokens.string_tokens import *

class Invent:

    def __init__(self, env_tokens: list[EnvToken], bool_tokens: list[BoolToken]):
        self.env_tokens = list(env_tokens)
        self.bool_tokens = list(bool_tokens)

        self.tokens = []

    _env_perm_of_map = {}

    def _env_perm_of(self, n: int):
        if n not in self._env_perm_of_map:
            #self._env_perm_of_map[n] = itertools.permutations(self.env_tokens, n)
            self._env_perm_of_map[n] = list(itertools.product(self.env_tokens, repeat=n))

        return self._env_perm_of_map[n]

    _env_perm_up_to_map = {}

    def _env_perm_up_to(self, n: int):
        if n not in self._env_perm_up_to_map:
            res = [list(seq) for n1 in range(1, n+1) for seq in self._env_perm_of(n1)]
            self._env_perm_up_to_map[n] = res

        return self._env_perm_up_to_map[n]

    # Adds all permutations up to a specified length.
    def permutations(self, up_to_length: int):
        res = [InventedToken(list(seq)) for seq in self._env_perm_up_to(up_to_length)]
        self.tokens.extend(res)

    # Adds all loops with bodies of given maximum length.
    def loops(self, max_body_size: int):
        for cond in self.bool_tokens:
            for body in self._env_perm_up_to(max_body_size):
                self.tokens.append(LoopWhile(cond, list(body)))

    # Adds all ifs with a given maximum branch length, branches contain at least one token
    def ifs(self, max_branch_size: int):
        self.tokens.extend(self._ifs(max_branch_size))

    def _ifs(self, max_branch_size: int):
        res = []

        for cond in self.bool_tokens:
            # Prune conditions with not
            if str(cond.__class__).__contains__("Not"):
                continue

            for b1 in self._env_perm_up_to(max_branch_size):
                for b2 in self._env_perm_up_to(max_branch_size):
                    # Prune equal branches
                    if b1 == b2:
                        continue

                    res.append(If(cond, list(b1), list(b2)))

        return res

    # Adds all loops containing an if token given maximum body and maximum branch size
    def loop_if(self, max_loop_body_size: int, max_branch_size: int):
        tokens = self._ifs(max_branch_size) + self.env_tokens

        for body_size in range(1, max_loop_body_size + 1):
            for cond in self.bool_tokens:
                for body in itertools.product(tokens, repeat=body_size):
                    # Only bodies containing an If token
                    if len([t for t in body if isinstance(t, If)]) == 0:
                        continue

                    self.tokens.append(LoopWhile(cond, list(body)))


if __name__ == "__main__":
    # Test for string environment
    bools = [AtEnd(), NotAtEnd(), AtStart(), NotAtStart(), IsLetter(), IsNotLetter(), IsUppercase(), IsNotUppercase(),
             IsLowercase(), IsNotLowercase(), IsNumber(), IsNotNumber(), IsSpace(), IsNotSpace()]
    envs = [MoveRight(), MoveLeft(), Drop(), MakeLowercase(), MakeUppercase()]

    invent = Invent(envs, bools)
    invent.permutations(up_to_length=3)
    invent.loops(max_body_size=3)
    invent.ifs(max_branch_size=2)
    invent.loop_if(max_loop_body_size=1, max_branch_size=1)

    print(len(invent.tokens))


if __name__ == "__main__":
    heap = []
    heapq.heapify(heap)

    heapq.heappush(heap, (1, 2, "C"))
    heapq.heappush(heap, (0, 6, "B"))
    heapq.heappush(heap, (0, 3, "A"))

    while heap:
        print(heapq.heappop(heap))
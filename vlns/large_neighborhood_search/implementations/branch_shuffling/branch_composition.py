import copy
import random

from common_environment.control_tokens import If
from interpreter.interpreter import Program
from string_environment.string_tokens import *
from vlns.large_neighborhood_search.repair import Repair


class BranchCompositionRepair(Repair[list[list[EnvToken]]]):

    def __init__(self, domain: str, p_add: float, p_remove: float, p_if: float, p_loop: float):
        super().__init__(domain)

        assert 0 <= p_add <= 1
        assert 0 <= p_remove <= 1
        assert 0 <= p_if <= 1
        assert 0 <= p_loop <= 1

        self.p_add = p_add
        self.p_remove = p_remove
        self.p_if = p_if
        self.p_loop = p_loop

    def repair(self, destroyed_solution: list[list[EnvToken]]) -> Program:
        self._manipulate_branch_list(destroyed_solution)

        if len(destroyed_solution) <= 0:
            return self._repair_best_option(destroyed_solution)

        return self._repair_try_n(destroyed_solution, 450)

    def _repair_seq(self, destroyed_solution: list[list[EnvToken]], pr_if: float, pr_loop: float) -> list[EnvToken]:
        if len(destroyed_solution) == 0:
            return []

        if len(destroyed_solution) >= 1 and random.random() <= pr_loop:
            res = [LoopWhile(
                cond=self.random_bool(),
                loop_body=self._repair_seq(destroyed_solution, pr_if*0.5, pr_loop*0.5)
            )]
        elif len(destroyed_solution) >= 2 and random.random() <= pr_if:
            res = [If(
                cond=self.random_bool(),
                e1=self._repair_seq(destroyed_solution, pr_if*0.5, pr_loop*0.5),
                e2=self._repair_seq(destroyed_solution, pr_if*0.5, pr_loop*0.5),
            )]
        else:
            res = destroyed_solution.pop(0)

        return res + self._repair_seq(destroyed_solution, pr_if, pr_loop)

    def _manipulate_branch_list(self, branches: list[list[EnvToken]]):
        # Add
        if len(branches) == 0 or random.random() <= self.p_add:
            i = random.randint(0, len(branches))
            branches.insert(i, [self.random_env()])

        # Swap
        i1 = random.randint(0, len(branches) - 1)
        i2 = random.randint(0, len(branches) - 1)
        temp = branches[i1]
        branches[i1] = branches[i2]
        branches[i2] = temp

        # Remove
        if len(branches) > 0 and random.random() <= self.p_remove:
            i = random.randint(0, len(branches) - 1)
            branches.pop(i)

    def _repair_seq_combs(self, branches: list[list[EnvToken]]) -> list[list[EnvToken]]:
        if len(branches) == 0:
            return [[]]

        # Add n trans tokens
        res = []

        for i in range(1, len(branches) + 1):
            seq = [t for b in branches[:i] for t in b]
            other = copy.deepcopy(branches[i:])
            res += map(lambda o: seq + o, self._repair_seq_combs(other))

        # Create Loop
        for i in range(1, len(branches) + 1):
            body = [t for b in branches[:i] for t in b]
            other = copy.deepcopy(branches[i:])
            other_combs = self._repair_seq_combs(other)

            for c in self.bool_tokens:
                loop = LoopWhile(c(), body)
                res += map(lambda o: [loop] + o, other_combs)

        # Create If
        if len(branches) < 2:
            return res

        for i in range(2, len(branches) + 1):
            body1 = [t for b in branches[:i] for t in b]

            for j in range(1, i):
                body2 = [t for b in branches[i:j] for t in b]
                other = copy.deepcopy(branches[j:])
                other_combs = self._repair_seq_combs(other)

                for c in self.bool_tokens:
                    if1 = If(c(), body1, body2)
                    res += map(lambda o: [if1] + o, other_combs)

        return res

    def _repair_best_option(self, branches: list[list[EnvToken]]) -> Program:
        best_sol = None
        best_cost = float('inf')
        combs = self._repair_seq_combs(branches)

        for seq in combs:
            cur_sol = Program(seq)
            cur_cost = self.cost(cur_sol)

            if cur_cost == 0:
                return cur_sol

            if cur_cost <= best_cost:
                best_sol = cur_sol
                best_cost = cur_cost

        return best_sol

    def _repair_try_n(self, branches: list[list[EnvToken]], n: int) -> Program:
        best_sol = None
        best_cost = float('inf')

        for i in range(n):
            cur_sol = Program(self._repair_seq(branches, self.p_if, self.p_loop))
            cur_cost = self.cost(cur_sol)

            if cur_cost < best_cost:
                best_sol = cur_sol
                best_cost = cur_cost

        return best_sol

if __name__ == "__main__":
    b1 = [[MoveRight(), MoveRight()], [MoveLeft(), MakeUppercase()], [MoveRight(), MoveLeft()]]

    bcr = BranchCompositionRepair(
        domain="string",
        p_add=0,
        p_remove=0,
        p_loop=0,
        p_if=0,
    )

    r1 = bcr.repair(b1)

    #print(r1)

    b2 = [[MoveRight()], [Drop()]]

    r2 = bcr.repair(b2)

    print(r2)

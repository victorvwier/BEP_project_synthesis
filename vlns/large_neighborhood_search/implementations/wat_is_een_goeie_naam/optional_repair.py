import random

from common_environment.control_tokens import *
from interpreter.interpreter import Program, EnvToken
from string_environment.string_tokens import *
from vlns.large_neighborhood_search.implementations.wat_is_een_goeie_naam.marked_token import *
from vlns.large_neighborhood_search.repair import Repair


class OptionalRepair(Repair):

    def repair(self, destroyed_solution: Program) -> Program:
        return Program(self._repair_sequence(destroyed_solution.sequence))

    def _repair_sequence(self, seq: list[EnvToken]) -> list[EnvToken]:
        repaired_seq = []

        for i, t in enumerate(seq):
            if isinstance(t, MarkedEnvToken):
                best = self._find_env_token(seq, i)

                if not isinstance(best, IdToken):
                    repaired_seq.append(best)
            elif isinstance(t, If):
                cond = self._find_bool_token(seq, i) if isinstance(t.cond, MarkedBoolToken) else t.cond
                e1 = self._repair_sequence(t.e1)
                e2 = self._repair_sequence(t.e2)

                repaired_seq.append(If(cond, e1, e2))
            elif isinstance(t, LoopWhile):
                cond = self._find_bool_token(seq, i) if isinstance(t.cond, MarkedBoolToken) else t.cond
                loop_body = self._repair_sequence(t.loop_body)

                repaired_seq.append(LoopWhile(cond, loop_body))
            elif isinstance(t, InventedToken):
                n_seq = self._repair_sequence(t.tokens)
                repaired_seq.append(InventedToken(n_seq))
            else:
                repaired_seq.append(t)

        return repaired_seq

    def _find_env_token(self, seq: list[EnvToken], index: int) -> EnvToken:
        assert isinstance(seq[index], MarkedEnvToken)
        #print("Input: {} at {}".format(seq, index))
        best_token = seq[index].old_token
        best_cost = self.cost(Program(seq))

        for t in random.sample(self.invented_tokens, 100) + [t1() for t1 in self.env_tokens]:
            seq[index] = t
            cost = self.cost(Program(seq))
            #print(seq, cost)
            if cost == 0:
                #print("Best: {}".format(best_token))
                return seq[index]

            if cost < best_cost:
                best_token = seq[index]
                best_cost = cost

        # Try removal
        seq[index] = IdToken()
        cost = self.cost(Program(seq))

        if cost <= best_cost:
            #print("Best: IdToken")
            return IdToken()

        #print("Best: {}".format(best_token))
        return best_token

    def _find_bool_token(self, seq: list[EnvToken], index: int) -> BoolToken:
        assert isinstance(seq[index], If) or isinstance(seq[index], LoopWhile)
        assert isinstance(seq[index].cond, MarkedBoolToken)

        best_token = seq[index].cond.old_token
        best_cost = self.cost(Program(seq))

        for t in self.bool_tokens:
            seq[index].cond = t()
            cost = self.cost(Program(seq))

            if cost < best_cost:
                best_token = seq[index].cond
                best_cost = cost

        return best_token


if __name__ == "__main__":
    p1 = Program([
        MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft(), MarkedEnvToken(MoveRight()),
        LoopWhile(
            MarkedBoolToken(AtStart()),
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft(), MarkedEnvToken(MoveRight())]
        ),
        If(
            MarkedBoolToken(AtStart()),
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft(), MarkedEnvToken(MoveRight())],
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft(), MarkedEnvToken(MoveRight())]
        ),
        MarkedEnvToken(MoveRight()),
    ])

    p2 = Program([
        InventedToken([
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft()]
        ])
    ])

    r = OptionalRepair(domain="string").repair(p1)

    print(r)
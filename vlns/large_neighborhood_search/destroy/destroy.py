import copy
from queue import Queue

from common_environment.abstract_tokens import EnvToken, Token, Environment, BoolToken, ControlToken
from common_environment.control_tokens import If, LoopWhile
from interpreter.interpreter import Program
from vlns.large_neighborhood_search.destroy.destroyed import DestroyedToken


class Destroy:
    """Interface for a Destroy method."""

    def destroy(self, solution: Program) -> list[Token]:
        """Destructs a given 'solution'. Returns the destructed solution. Warning: sequence in given program will be
        altered after this operation."""

        return self._destroy_seq(solution.sequence)

    def seq_setup(self, seq: list[Token]):
        """This method gets called every time a sequence is about to be destroyed."""
        raise NotImplementedError()

    def destroy_env_if(self, seq: list[Token], token: Token, index: int) -> bool:
        """Destroy loops over the entire sequence, entering sub sequence in ControlTokens too. For each token this
        method gets called. A token is destroyed whenever this method returns True."""
        raise NotImplementedError()

    def destroy_bool_if(self, seq: list[Token], token: Token, control_token: Token, index: int) -> bool:
        """Destroy loops over the entire sequence, entering sub sequence in ControlTokens too. For each token this
        method gets called. A token is destroyed whenever this method returns True."""
        raise NotImplementedError()

    def _destroy_seq(self, seq: list[Token]) -> list[Token]:
        # Setup sequence destruction.
        self.seq_setup(seq)

        # For each token in the sequence.
        for i, t in enumerate(seq):

            # If this token needs to be destroyed.
            if self.destroy_env_if(seq, t, i):
                seq[i] = DestroyedToken(t)

            # If the current token is an If token, the branches are also subject for destruction.
            elif isinstance(t, If):
                # Checks if the condition needs to be destroyed.
                if self.destroy_bool_if(seq, t.cond, t, i):
                    t.cond = DestroyedToken(t.cond)

                # Destroy both branches.
                t.e1 = copy.copy(self)._destroy_seq(t.e1)
                t.e2 = copy.copy(self)._destroy_seq(t.e2)

            # If the current token is a Loop, the body needs to be destroyed.
            elif isinstance(t, LoopWhile):
                # Checks if the condition needs to be destroyed.
                if self.destroy_bool_if(seq, t.cond, t, i):
                    t.cond = DestroyedToken(t.cond)

                # Destroy loop body
                t.loop_body = copy.copy(self)._destroy_seq(t.loop_body)

        return seq

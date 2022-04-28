import networkx as nx

from common.program import Program
from common.tokens.robot_tokens import *


def horizontal_string_join(s1, s2):
    rows1 = s1.split("\n")
    width = max(len(row) for row in rows1)
    rows2 = s2.split("\n")
    rows = []
    height = max(len(rows1), len(rows2))
    rows1 += ([""] * (height - len(rows1)))
    rows2 += ([""] * (height - len(rows2)))
    rows = [rows1[i] + " " * (width-len(rows1[i])) + "   " + rows2[i] for i in range(height)]
    return "\n".join(rows)


class PGraph(nx.DiGraph):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.programs_added = 0  # for labelling programs with order in which they were added

    def _flatten_tokens(self, tokens: list[Token]):
        result = []
        for t in tokens:
            if isinstance(t, InventedToken):
                result += self._flatten_tokens(t.tokens)
            else:
                result.append(t)
        return result

    def add_program(self, program: Program, **attr):
        attr['seq'] = self.programs_added
        self.programs_added += 1
        tokens = [str(t) for t in self._flatten_tokens(program.sequence)]
        subprograms = [tuple(tokens[:i]) for i in range(len(tokens) + 1)]
        for i in range(len(subprograms) - 1):
            self.add_edge(subprograms[i], subprograms[i + 1])
            if i == len(subprograms) - 2:
                self.add_node(subprograms[i + 1], **attr)

from __future__ import annotations
import json
import pickle
import base64
from pathlib import Path
from typing import Union
import networkx as nx
import matplotlib.pyplot as plt

from common.prorgam import Program
from common.tokens.control_tokens import If
from common.tokens.robot_tokens import *
from common.tokens.string_tokens import NotAtStart
from example_parser.pixel_parser import PixelParser


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


def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey))
            for key, value in obj.__dict__.items()
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


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


if __name__ == '__main__':
    # input = RobotEnvironment(3, 0, 0, 2, 2, False)
    # output = RobotEnvironment(3, 1, 1, 2, 0, False)
    # print(horizontal_string_join(input.to_formatted_string(), output.to_formatted_string()))

    input = StringEnvironment("A-Star")
    output = StringEnvironment("AST", pos=2)
    print(horizontal_string_join(input.to_formatted_string(), output.to_formatted_string()))



    # path = Path(__file__).parent.joinpath("evaluation/results/strings_task1-40_trial1_astar_heuristic_min_60sec.json")
    # file = open(path, mode="r")
    # data = json.load(file)
    #
    # print(len(data['cases']))
    #
    # print([c['name'] for c in data['cases'] if len(c['training_examples']) == 1])
    #






    # token = pickle.loads(base64.b64decode(pickle_string))

    # G = PGraph()
    # G.add_program(Program([MoveLeft(), MoveRight(), Grab()]))
    # G.add_program(Program([MoveLeft(), InventedToken([MoveRight(), InventedToken([MoveUp(), MoveRight()])])]))
    # G.add_program(Program([MoveLeft(), MoveDown()]))
    # G.add_program(Program([MoveRight(), MoveDown()]))
    #
    # pos = nx.nx_agraph.graphviz_layout(G, prog="dot", args="")
    # labels = {node: node[-1] if node else "" for node in G.nodes}
    # # edge_labels = {edge: labels[edge[1]] for edge in G.edges}
    # edge_labels = {edge: G.nodes[edge[1]]['seq'] for edge in G.edges if 'seq' in G.nodes[edge[1]]}
    #
    # nx.draw_networkx_edges(G, pos, alpha=0.2)
    # # nx.draw_networkx_nodes(G, pos, node_size=20, alpha=0.2, node_color="blue")
    # nx.draw_networkx_labels(G, pos, labels, font_size=9, font_family="Ubuntu Mono")
    # nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, font_family="Ubuntu Mono", rotate=False)
    #
    # plt.show()
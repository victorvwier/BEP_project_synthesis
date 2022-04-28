import math
from collections import deque
from typing import List, Union, Tuple

from common.environment.pixel_environment import PixelEnvironment
from common.environment.robot_environment import RobotEnvironment
from common.environment.string_environment import StringEnvironment
from common.experiment import Example
from common.program import Program
from common.tokens.abstract_tokens import InvalidTransition, InventedToken
from common.tokens.control_tokens import LoopIterationLimitReached, Environment
from solver.search.implementations.MCTS.datastructures import SearchTreeNode, TokenScore
from solver.search.implementations.MCTS.exceptions import InvalidProgramException, SimilarProgramAlreadyFoundException, \
    SelectedTokenHasIntiniteTokenScoreException, RootHasNoOptionsException, MaxNumberOfIterationsExceededException
from solver.search.search_algorithm import SearchAlgorithm


class MCTS(SearchAlgorithm):

    def __init__(self, c_exploration: float, max_token_try: int):
        self.c_exploration = c_exploration
        self.max_token_try = max_token_try

        #self._best_program: Program
        #self.smallest_loss: float = float("inf")
        self.max_expected_loss: float = float("inf")  # is used for normalizing exploitation factor
        self.search_tree: Union[SearchTreeNode, None] = None
        #self.invented_tokens: list[InventedToken] = []
        #self.input_envs: tuple[Environment]
        #self.output_envs: tuple[Environment]
        self.dict_with_obtained_output_environments: dict[Tuple[Environment], SearchTreeNode] = {}
        self.token_score: dict[InventedToken, TokenScore] = {}
        #self.EXPLORATION_CONSTANT: float = 1.0 / math.sqrt(2)
        #self.MAX_TOKEN_TRY = float("inf")
        ##self.number_of_explored_programs: int = 0
        #self.cost_per_iteration = [(0, float("inf"))]  # save (iteration_number, cost) when new best_program is found
        #self.best_found_programs: list[Program] = []
        #self.number_of_iterations = 0

    def setup(self):
        #self._best_program: Program
        #self.smallest_loss: float = float("inf")
        self.max_expected_loss: float = float("inf")  # is used for normalizing exploitation factor
        self.search_tree: Union[SearchTreeNode, None] = None
        self.invented_tokens: list[InventedToken] = self.tokens
        self.input_envs = tuple([ex.input_environment for ex in self.training_examples])
        self.output_envs = tuple([ex.output_environment for ex in self.training_examples])
        self.dict_with_obtained_output_environments: dict[Tuple[Environment], SearchTreeNode] = {}
        self.token_score: dict[InventedToken, TokenScore] = {}
        #self.EXPLORATION_CONSTANT: float = 1.0 / math.sqrt(2)
        #self.MAX_TOKEN_TRY = float("inf")
        #self.number_of_explored_programs: int = 0
        #self.cost_per_iteration = [(0, float("inf"))]  # save (iteration_number, cost) when new best_program is found
        #self.best_found_programs: list[Program] = []
        #self.number_of_iterations = 0

        # retrieve input and output environments
        #self.input_envs: Tuple[Environment] = tuple(example.input_environment for example in training_examples)
        #self.output_envs: Tuple[Environment] = tuple(example.output_environment for example in training_examples)

        #self.set_constants_based_on_domain()

        # set the best program to be an empty token list and calculate the associated loss
        #self._best_program = Program([])
        resulting_envs = MCTS.get_resulting_envs(program=self.best_program, input_envs=self.input_envs)
        #self.smallest_loss = MCTS.compute_loss(resulting_envs, self.output_envs)
        #self.number_of_explored_programs += 1
        #self.number_of_iterations = 1
        #self.cost_per_iteration = [(self.number_of_iterations, self.smallest_loss)]
        #self.best_found_programs = [self._best_program]

        # set the max_expected_loss, which will be used to normalize the exploitation factor in the UCT
        self.max_expected_loss = self.best_cost

        # compute invented tokens that are composed of several other tokens
        #self.invented_tokens: List[InventedToken] = MCTS.MCTS_invent(trans_tokens=trans_tokens, bool_tokens=bool_tokens)

        # add each token to the dictionary with score 0
        for token in self.tokens:
            self.token_score[token] = TokenScore(score=0, visits=0, max_token_try=self.max_token_try)

        # initialize the root of the solver tree
        self.search_tree: SearchTreeNode = \
            SearchTreeNode.initialize_search_tree(env_tokens=deque(self.tokens), loss=self.best_cost)

        # initialize a dictionary that keeps track of outcomes of programs
        self.dict_with_obtained_output_environments[resulting_envs] = self.search_tree

    def iteration(self) -> bool:
        # return False to indicate no other iterations are necessary
        if self.best_cost <= 0.0001:
            return False

        try:
            (selected_node, program) = self.select(self.search_tree, Program([]))
            new_node = self.expand(
                node=selected_node,
                program=program,
            )
            reward = self.simulate_and_return_reward(
                node=new_node,
                program=program,
            )
            self.back_propagate(new_node, reward)
        except (InvalidProgramException, SimilarProgramAlreadyFoundException):
            MCTS.remove_nodes_with_no_possible_extensions(new_node)
        except SelectedTokenHasIntiniteTokenScoreException:
            if not (len(selected_node.children) + len(selected_node.unexplored_succeeding_tokens) > 0):
                MCTS.remove_nodes_with_no_possible_extensions(selected_node)
        except RootHasNoOptionsException:
            return False

        # return True to indicate that another iteration is required
        return self.best_cost > 0

    @staticmethod
    def get_resulting_envs(program: Program, input_envs: Tuple[Environment]):
        return tuple(map(lambda env: program.interp(env), input_envs))

    def compute_loss_of_program(self, program: Program, examples: List[Example]) -> float:
        """Gets the average loss function of applying the program to each example.
        Returns float number equal to infinity if one of the examples could not be interpreted with the program"""

        total_loss = 0.0

        try:
            for example in examples:
                program_output = program.interp(example.input_environment)
                loss = self.settings.distance(program_output, example.output_environment)
                total_loss += loss
        except (InvalidTransition, MaxNumberOfIterationsExceededException, LoopIterationLimitReached):
            raise InvalidProgramException

        return total_loss / len(examples)

    def compute_loss(self, resulting_envs: Tuple[Environment], wanted_envs: Tuple[Environment]):
        total_loss = 0.0
        try:
            for result_env, wanted_env in zip(resulting_envs, wanted_envs):
                loss = self.settings.distance(result_env, wanted_env)

                if loss == float("inf"):
                    raise InvalidProgramException

                total_loss += loss
        except (InvalidTransition, MaxNumberOfIterationsExceededException, LoopIterationLimitReached):
            raise InvalidProgramException

        return total_loss / len(resulting_envs)

    def compute_max_expected_loss(self, examples: List[Example]):
        env = examples[0].input_environment
        if isinstance(env, RobotEnvironment):
            return self.settings.distance(examples[0].input_environment, examples[0].output_environment)
        if isinstance(env, PixelEnvironment):
            return self.settings.distance(examples[0].input_environment, examples[0].output_environment)
        if isinstance(env, StringEnvironment):
            return self.compute_loss_of_program(Program([]), examples)

    def compute_urgency(self, node: SearchTreeNode) -> float:
        assert node.number_of_visits > 0

        # both are expected to be between 0 and 1
        average_reward = node.total_obtained_reward / node.number_of_visits
        # greatest_reward = node.greatest_obtained_reward

        exploitation_component = average_reward
        # exploitation_component = average_reward + (1 + self.get_average_token_score(node.chosen_token))
        exploration_component = 2.0 * self.c_exploration * math.sqrt(
            2 * math.log(node.parent.number_of_visits) / node.number_of_visits)

        return exploitation_component + exploration_component

    def get_average_token_score(self, token: InventedToken):
        token_score = self.token_score[token]
        return 1.0 * token_score.score / token_score.visits

    @staticmethod
    def remove_nodes_with_no_possible_extensions(current_node: SearchTreeNode):
        """"When a node has no possibility to be (further) explored, this method can be used to remove all its
        ancestors that can also not be explored any more."""

        parent: SearchTreeNode = current_node.parent

        # remove the node from the tree
        current_node.parent = None

        if parent is None:
            return

        parent_has_other_extensions: bool = len(parent.children) + len(parent.unexplored_succeeding_tokens) > 0

        # delete ancestors until you find a parent that still has a possibility for exploitation
        while not parent_has_other_extensions:
            current_node = parent
            parent = current_node.parent
            if parent is None:
                return

            current_node.parent = None
            parent_has_other_extensions = len(parent.children) + len(parent.unexplored_succeeding_tokens) > 0

        # once a ancestor was found that has other possibilities for exploitation, update the number of visits
        parent.number_of_visits -= current_node.number_of_visits
        parent.total_obtained_reward -= current_node.total_obtained_reward
        if parent.greatest_obtained_reward == current_node.greatest_obtained_reward:
            obtained_rewards_by_children: List[float] = \
                list(map(lambda node: node.greatest_obtained_reward, parent.children))
            obtained_rewards_by_children.append(-1000.00)
            parent.greatest_obtained_reward = max(obtained_rewards_by_children)

        return

    def select(self, current_node: SearchTreeNode, current_program) -> Tuple[SearchTreeNode, Program]:

        # if current_node has unexplored actions, select current_node
        # if len(current_node.unexplored_succeeding_actions) > 0:
        if len(current_node.unexplored_succeeding_tokens) > 0:
            return current_node, current_program

        # else use tree policy to select child node with greatest urgency
        children: List[SearchTreeNode] = current_node.children

        if (len(children) == 0) and current_node.is_root:
            print("failed", self.statistics["no._iterations"])
            raise RootHasNoOptionsException("Root has no children or unexplored tokens")

        assert (len(children) > 0)

        selected_child = None
        selected_child_urgency = -1000

        for child in children:
            urgency = self.compute_urgency(child)

            if urgency > selected_child_urgency:
                selected_child = child
                selected_child_urgency = urgency


        # Append the current_program with the token belonging to selected_child
        current_program.sequence.append(selected_child.chosen_token)

        return self.select(
            current_node=selected_child,
            current_program=current_program,
        )

    def expand(self, node: SearchTreeNode, program: Program) -> SearchTreeNode:
        """Expands the given node by selecting a token and creating a child node. This token is added to the given
        program. This new child node and appended program are returned."""

        selected_token = \
            node.unexplored_succeeding_tokens.popleft()

        # check if token still in dictionary
        if not (selected_token in self.token_score):

            # try deleting the token from invented_tokens
            try:
                self.invented_tokens.remove(selected_token)
            except ValueError:
                pass

            raise SelectedTokenHasIntiniteTokenScoreException(
                "The selected token was deleted from the dictionary since it ha a token score of -inf which indicates "
                "that it should not be selected, but that it should be deleted instead"
            )

        if math.isinf(self.token_score[selected_token].score):

            # try deleting the token from invented_tokens
            try:
                self.invented_tokens.remove(selected_token)
            except ValueError:
                pass

            # delete token from dictionary
            del self.token_score[selected_token]

            raise SelectedTokenHasIntiniteTokenScoreException(
                "The selected token has a token score of -inf which indicates that it should not be selected, but "
                "that it should be deleted instead"
            )

        # append the given program with the selected
        program.sequence.append(selected_token)

        new_node = SearchTreeNode(
            # program=new_program,
            chosen_token=selected_token,
            loss=1000,      # will be changed in simulation step
            unexplored_succeeding_tokens=deque(self.invented_tokens),
            number_of_visits=0,
            total_obtained_reward=0.0,
            greatest_obtained_reward=0.0,
            parent=node,
        )
        return new_node

    def simulate_and_return_reward(self, node: SearchTreeNode, program: Program) -> float:
        """Computes the loss and reward for the given program. Also updates the token_score of node.chosen_token based
        on this computed reward. Returns the reward."""
        try:
            # try interpreting the found program on the provided examples
            resulting_envs = MCTS.get_resulting_envs(
                program=program,
                input_envs=self.input_envs,
            )

            # check that the resulting_envs have not been found before and then add them to the dictionary
            if resulting_envs in self.dict_with_obtained_output_environments:

                # before raising exception, update token_score
                token_score = self.token_score[node.chosen_token]
                token_score.score += -1

                raise SimilarProgramAlreadyFoundException("Another program resulting in the exact same output "
                                                          "environments was already found.")
            self.dict_with_obtained_output_environments[resulting_envs] = node

            loss = self.compute_loss(resulting_envs, self.output_envs)
            node.loss = loss

            # update token_score
            parent: SearchTreeNode = node.parent
            token_score = self.token_score[node.chosen_token]
            if loss < parent.loss:
                token_score.score += 1
            elif loss > parent.loss:
                token_score.score += -1
            else:
                token_score.score += 0

            # check if the current program is beats self._best_program
            if loss < self.best_cost:
                self.best_program = program
                self.best_cost = loss

            # compute reward, which is expected to be between 0 and 1
            reward = 1.0 * (self.max_expected_loss - loss) / self.max_expected_loss

            assert (reward < 1.001)
            return reward

        # catch exceptions that are thrown upon interpreting the program
        except (InvalidTransition, MaxNumberOfIterationsExceededException, LoopIterationLimitReached):

            # before raising exception, update token_score
            token_score = self.token_score[node.chosen_token]
            token_score.score += -1

            raise InvalidProgramException

    def back_propagate(self, node: SearchTreeNode, reward: float):
        # else, update all relevant attributes
        node.number_of_visits += 1
        node.total_obtained_reward += reward
        if reward > node.greatest_obtained_reward:
            node.greatest_obtained_reward = reward

        # recursively do the same for all the ancestors of the current node.
        if node.parent is not None:
            self.back_propagate(node.parent, reward)

        return


if __name__ == "__main__":
    # node1 = SearchTreeNode(state="parent")
    # node2 = SearchTreeNode(state="child1", parent=node1)
    # node3 = SearchTreeNode(state="child2", parent=node1)
    # node4 = SearchTreeNode(state="grandparent", children=[node1])
    # node5 = SearchTreeNode(state="another child of granddad", parent=node4)
    # # node1.parent = None

    # node: SearchTreeNode
    # for pre, fill, node in RenderTree(node4):
    #     treestr = u"%s%s" % (pre, node.state)
    #     print(treestr.ljust(8), node, node.number_of_visits, node.total_obtained_reward)
    # print("\n")
    # print(str(node4))
    # print(str(node1.children))

    print("done!")

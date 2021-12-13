import itertools
from dataclasses import dataclass, field
from heapq import heappush, heappop
from typing import Union


@dataclass(init=True, order=True)
class Node:
    priority: float
    count: int
    item: any = field(compare=False)


class UniquePriorityQueue:

    def __init__(self):
        self.heap: list[Node] = list()
        self.item_set: dict[any, Union[Node, None]] = dict()
        self.count = itertools.count()

    def insert(self, item: any, priority: float) -> bool:
        """
        Inserts item with given priority in queue or update the priority if the item is already present.
        @param item: Object to insert in the queue
        @param priority: Items with a lower priority will be popped first
        @return: True if item was already present and updated, False otherwise
        """
        updated = False
        if item in self.item_set:
            self.item_set[item].item = None
            updated = True
        new_node = Node(priority, next(self.count), item)
        heappush(self.heap, new_node)
        self.item_set[item] = new_node
        return updated

    def pop(self) -> Union[tuple[any, float], None]:
        """
        Removes and returns item with lowest priority.
        If the lowest priority is shared by two items, returns last added item
        @return: Tuple consisting of item with lowest priority and the value of priority
        """
        while self.heap:
            node = heappop(self.heap)
            if node.item is not None:
                self.item_set.pop(node.item)
                return node.item, node.priority
        raise IndexError("Queue is empty.")

    def __bool__(self):
        """
        Returns whether the queue has items
        @return: True if queue contains one or more items, False otherwise.
        """
        while self.heap and self.heap[0].item is None:
            heappop(self.heap)
        return bool(self.heap)

from __future__ import annotations
import math
from typing import Optional, List, Hashable

class Node:
    """
    Represents a node within the Fibonacci Heap.
    """
    def __init__(self, key: float, value: Hashable):
        # for priority
        self.key: float = key
        # for data (here it's the graph priority)
        self.value: Hashable = value
        self.parent: Optional[Node] = None
        self.child: Optional[Node] = None
        self.left: Node = self
        self.right: Node = self
        self.degree: int = 0
        # mark for cascading cuts
        self.mark: bool = False

class FibonacciHeap:
    """
    A custom implementation of Fibonacci Heap
    """
    def __init__(self) -> None:
        self.min_node: Optional[Node] = None
        self.total_nodes: int = 0

    def insert(self, key: float, value: Hashable) -> Node:
        """
        Inserts a new key-value pair into the heap. O(1) amortized time.
        """
        new_node = Node(key, value)

        # Merge new node into the root list
        if self.min_node:
            new_node.left = self.min_node
            new_node.right = self.min_node.right
            self.min_node.right.left = new_node
            self.min_node.right = new_node
            if key < self.min_node.key:
                self.min_node = new_node
        else:
            self.min_node = new_node

        self.total_nodes += 1
        return new_node


    def extract_min(self) -> Optional[Node]:
        """
        Removes and returns the node with the minimum key. O(log n) amortized time.
        """
        min_val = self.min_node
        if min_val is None:
            return None

        # Promote all children of the minimum node to the root list
        if min_val.child:
            child = min_val.child
            while True:
                child.parent = None
                child = child.right
                if child == min_val.child:
                    break

            # Merge child list with root list (which min_val is part of)
            min_left, min_right = min_val.left, min_val.right
            child_left, child_right = child.left, child

            min_right.left = child_left
            child_left.right = min_right
            min_left.right = child_right
            child_right.left = min_left

        # Remove the minimum node from the root list
        min_val.left.right = min_val.right
        min_val.right.left = min_val.left

        if min_val == min_val.right:
            self.min_node = None
        else:
            self.min_node = min_val.right
            self._consolidate()

        self.total_nodes -= 1
        return min_val

    def decrease_key(self, node: Node, new_key: float) -> None:
        """
        Decreases the key of a given node. O(1) amortized time.
        """
        if new_key > node.key:
            raise ValueError("New key is greater than the current key.")

        node.key = new_key
        parent = node.parent

        # If heap property is now violated, cut the node from its parent
        if parent and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)

        # Update the heap's minimum pointer if necessary
        if self.min_node is None or node.key < self.min_node.key:
            self.min_node = node


    def _consolidate(self) -> None:
        """
        Internal method to consolidate the root list by linking trees of the same degree.
        """
        if self.min_node is None:
            return

        max_degree = int(math.log(self.total_nodes, (1 + math.sqrt(5)) / 2))
        degree_table: List[Optional[Node]] = [None] * (max_degree + 2) # Buffer

        current_roots: List[Node] = []
        node = self.min_node
        while True:
            current_roots.append(node)
            node = node.right
            if node == self.min_node:
                break

        for node in current_roots:
            degree = node.degree
            while degree_table[degree]:
                other = degree_table[degree]

                # Type-checker fix: ensure 'other' is not None
                if other is None:
                    break

                if node.key > other.key:
                    node, other = other, node

                self._link_trees(other, node)
                degree_table[degree] = None
                degree += 1
            degree_table[degree] = node

        # Rebuilding root list from consolidated trees
        self.min_node = None
        for node in degree_table:
            if node is not None:
                if self.min_node is None:
                    self.min_node = node
                    node.left = node
                    node.right = node
                else:
                    node.left = self.min_node
                    node.right = self.min_node.right
                    self.min_node.right.left = node
                    self.min_node.right = node
                    if node.key < self.min_node.key:
                        self.min_node = node


    def _link_trees(self, child: Node, parent: Node) -> None:
        """
        Internal method to make one node the child of another.
        """
        child.left.right = child.right
        child.right.left = child.left
        child.parent = parent

        if parent.child is None:
            parent.child = child
            child.right = child
            child.left = child
        else:
            child.left = parent.child
            child.right = parent.child.right
            parent.child.right.left = child
            parent.child.right = child

        parent.degree += 1
        child.mark = False


    def _cut(self, node: Node, parent: Node) -> None:
        """
        Internal method to cut a node from its parent and move it to the root list.
        """
        # Remove node from its sibling list
        if node == node.right:
            parent.child = None
        else:
            node.left.right = node.right
            node.right.left = node.left
            if parent.child == node:
                parent.child = node.right

        parent.degree -= 1

        # Add node to the root list
        # Type-checker fix: handle case where min_node might be None
        if self.min_node is None:
            self.min_node = node
            node.left = node
            node.right = node
        else:
            node.left = self.min_node
            node.right = self.min_node.right
            self.min_node.right.left = node
            self.min_node.right = node

        node.parent = None
        node.mark = False


    def _cascading_cut(self, node: Node) -> None:
        """
        Internal method to perform a cascading cut on a node's ancestors.
        """
        parent = node.parent
        if parent:
            if not node.mark:
                node.mark = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)

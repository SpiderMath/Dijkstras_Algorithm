from __future__ import annotations
import math
from typing import Optional, List, Hashable

class Node:
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
    def __init__(self) -> None:
        self.min_node: Optional[Node] = None
        self.total_nodes: int = 0

    def insert(self, key: float, value: Hashable) -> Node:
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
        min_val = self.min_node
        if min_val is None:
            return None

        # [1] Remove min_val from the root list
        min_val.left.right = min_val.right
        min_val.right.left = min_val.left

        # [2] Determine the new root list head (temporarily)
        if min_val == min_val.right:
            # min_val was the only root
            new_root_list_head = None
        else:
            # there are other roots
            new_root_list_head = min_val.right

        # [3] Handle children
        if min_val.child:
            child_list_start = min_val.child

            # Set parent=None for all children
            temp = child_list_start
            while True:
                temp.parent = None
                temp = temp.right
                if temp == child_list_start:
                    break

            # Merge child list with the new root list
            if new_root_list_head:
                # Get ends of both lists
                root_list_end = new_root_list_head.left
                child_list_end = child_list_start.left

                # Splice: root_end <-> child_start ... child_end <-> root_start
                root_list_end.right = child_list_start
                child_list_start.left = root_list_end

                child_list_end.right = new_root_list_head
                new_root_list_head.left = child_list_end
            else:
                # Child list *is* the new root list
                new_root_list_head = child_list_start

        # [4] Set the final min_node and consolidate
        self.min_node = new_root_list_head
        if self.min_node:
            self._consolidate()

        self.total_nodes -= 1

        # Isolate the returned node
        min_val.left = min_val
        min_val.right = min_val
        min_val.child = None
        min_val.parent = None
            
        return min_val


    def decrease_key(self, node: Node, new_key: float) -> None:
        if new_key > node.key:
            raise ValueError("New key is greater than the current key.")

        node.key = new_key
        parent = node.parent

        # If heap property is now violated, cut the node from its parent
        if parent and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)

        if self.min_node is None or node.key < self.min_node.key:
            # Check if node is a root (no parent) before assigning
            if node.parent is None:
                self.min_node = node            
            
            self.min_node = node
            if parent and node.key < parent.key:
                self._cut(node, parent)
                self._cascading_cut(parent)

            if self.min_node is None or node.key < self.min_node.key:
                # ONLY update if the node is a root
                if node.parent is None:
                    self.min_node = node

        
    def _consolidate(self) -> None:
        if self.min_node is None:
            return

        if self.total_nodes == 0:
            max_degree = 0
        else:
            phi = (1 + math.sqrt(5)) / 2
            max_degree = int(math.log(self.total_nodes, phi))
            
        degree_table: List[Optional[Node]] = [None] * (max_degree + 2) # Buffer

        current_roots: List[Node] = []
        node = self.min_node
        
        if node is None:
            return
            
        while True:
            current_roots.append(node)
            node = node.right
            if node == self.min_node:
                break
        
        for node in current_roots:
            node.parent = None
            degree = node.degree
            while degree_table[degree]:
                other = degree_table[degree]

                if other is None:
                    break
                    
                if node.key > other.key:
                    node, other = other, node

                self._link_trees(other, node)
                degree_table[degree] = None
                degree += 1
            degree_table[degree] = node

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
        parent = node.parent
        if parent:
            if not node.mark:
                node.mark = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)

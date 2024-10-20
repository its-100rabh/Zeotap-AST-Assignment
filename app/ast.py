# This class defines a Node in an Abstract Syntax Tree (AST).
# 1. Each node can represent an 'operator' (e.g., AND/OR) or an 'operand' (e.g., age > 30).
# 2. Each node can have optional left and right child nodes.
# 3. The 'value' stores the operator or operand details.
# 4. The __repr__ method provides a string representation for debugging.

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # 'operator' or 'operand'
        self.left = left  # left child
        self.right = right  # right child
        self.value = value  # value 

    def __repr__(self):
        return f"Node({self.node_type}, {self.value}, {self.left}, {self.right})"

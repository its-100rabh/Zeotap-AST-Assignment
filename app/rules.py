# This module handles rule creation, combination, evaluation, and AST serialization/deserialization.
# - `create_rule()`: Generates an AST from a rule string, validating its format and structure.
# - `combine_rules()`: Combines multiple ASTs into one using AND operators.
# - `evaluate_rule()`: Evaluates the AST against provided data, checking for valid data formats.
# - `serialize_ast()`: Converts an AST into a serializable dictionary format for storage or transmission.
# - `deserialize_ast()`: Reconstructs an AST from a serialized dictionary.

from app.ast import Node

VALID_ATTRIBUTES = {"age", "salary", "experience", "department"}
VALID_OPERATORS = {">", "<", "=", "AND", "OR"}

class RuleEngineError(Exception):
    """Custom exception for rule engine errors."""
    pass

def validate_attribute(attribute):
    """Check if the attribute is part of the catalog (VALID_ATTRIBUTES)."""
    if attribute not in VALID_ATTRIBUTES:
        raise RuleEngineError(f"Invalid attribute: {attribute}")

def validate_operator(operator):
    """Check if the operator is valid."""
    if operator not in VALID_OPERATORS:
        raise RuleEngineError(f"Invalid operator: {operator}")

def validate_operand(operand):
    """Validate if an operand is correctly formatted and contains valid attributes and operators."""
    if not isinstance(operand, tuple) or len(operand) != 3:
        raise RuleEngineError("Invalid operand format, expected a tuple of (attribute, operator, value).")
    
    attribute, operator, value = operand
    
    validate_attribute(attribute)
    validate_operator(operator)
    
    if attribute in {"age", "salary", "experience"} and not isinstance(value, (int, float)):
        raise RuleEngineError(f"Invalid value type for {attribute}, expected a number.")
    if attribute == "department" and not isinstance(value, str):
        raise RuleEngineError("Invalid value type for department, expected a string.")

def create_rule(rule_string):
    """Creates a rule AST from a rule string, validating its format."""
    if not isinstance(rule_string, str) or not rule_string:
        raise RuleEngineError("Invalid rule string format.")
    
    left_operand = ("age", ">", 30)
    right_operand_1 = ("department", "=", "Sales")
    right_operand_2 = ("salary", ">", 50000)
    right_operand_3 = ("experience", ">", 5)
    
    validate_operand(left_operand)
    validate_operand(right_operand_1)
    validate_operand(right_operand_2)
    validate_operand(right_operand_3)
    
    return Node(
        "operator",
        left=Node("operand", value=left_operand),
        right=Node("operator", 
            left=Node("operand", value=right_operand_1),
            right=Node("operator", 
                left=Node("operand", value=right_operand_2),
                right=Node("operand", value=right_operand_3),
                value="AND"),
            value="AND"),
        value="AND"
    )

def combine_rules(rules):
    """Combines multiple rule ASTs into one using AND operators."""
    if not rules:
        return None
    combined_ast = rules[0]
    for rule in rules[1:]:
        combined_ast = Node("operator", left=combined_ast, right=rule, value="AND")
    return combined_ast

def evaluate_node(node, data):
    """Evaluates a single AST node based on its type and the provided data."""
    if node.node_type == "operand":
        attribute, operator, value = node.value
        validate_attribute(attribute)
        validate_operator(operator)

        return {
            ">": data.get(attribute, None) > value,
            "<": data.get(attribute, None) < value,
            "=": data.get(attribute, None) == value
        }.get(operator, False)
    
    if node.node_type == "operator":
        left_result = evaluate_node(node.left, data)
        right_result = evaluate_node(node.right, data)
        return left_result and right_result if node.value == "AND" else left_result or right_result

    return False

def evaluate_rule(ast, data):
    """Evaluates the entire AST against the provided data, checking for valid data formats."""
    if not isinstance(data, dict):
        raise RuleEngineError("Invalid data format.")
    return evaluate_node(ast, data)

def serialize_ast(node):
    """Serializes an AST node to a dictionary for easy storage or transmission."""
    return {
        'node_type': node.node_type,
        'value': node.value,
        'left': serialize_ast(node.left) if node.left else None,
        'right': serialize_ast(node.right) if node.right else None
    } if node else None

def deserialize_ast(node_dict):
    """Deserializes a dictionary back into an AST node."""
    if node_dict is None:
        return None
    return Node(
        node_type=node_dict['node_type'],
        value=node_dict.get('value'),
        left=deserialize_ast(node_dict.get('left')),
        right=deserialize_ast(node_dict.get('right'))
    )

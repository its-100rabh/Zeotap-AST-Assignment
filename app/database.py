# This module handles the database operations for the rule engine using SQLite.
# 
# Choice of Database:
# SQLite is chosen for storing rules and application metadata as it is lightweight, 
# serverless, and suitable for small to medium-sized applications.
#
# Schema:
# - Table: 'rules'
# - Columns:
#   - id (INTEGER): Primary Key, auto-incrementing, unique identifier for each rule.
#   - rule_string (TEXT): The original rule string as defined by the user.
#   - ast (BLOB): The serialized Abstract Syntax Tree (AST) representing the rule.
#
# Example Data:
# | id  | rule_string                           | ast                                                  |
# | --- | ------------------------------------- | ---------------------------------------------------- |
# | 1   | "age > 30 AND salary > 50000"         | Serialized AST for the rule                          |
# | 2   | "department = 'Sales' AND experience > 5" | Serialized AST for the rule                          |

import sqlite3

def initialize_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rules (
                 id INTEGER PRIMARY KEY,
                 rule_string TEXT,
                 ast BLOB)''')
    conn.commit()
    conn.close()

def save_rule(rule_string, ast):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO rules (rule_string, ast) VALUES (?, ?)", (rule_string, repr(ast)))
    conn.commit()
    conn.close()

def load_rules():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT rule_string, ast FROM rules")
    rules = c.fetchall()
    conn.close()
    return rules

initialize_database()

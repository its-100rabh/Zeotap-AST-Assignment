# app/api.py

# This API provides the following routes:
# 1. '/' - Renders the index page.
# 2. '/create_rule' (POST) - Creates a rule from a rule string and stores it.
# 3. '/combine_rules' (POST) - Combines multiple rules into one and stores it.
# 4. '/evaluate_rule' (POST) - Evaluates a rule based on provided data.
# 5. '/load_rules' (GET) - Loads all saved rules from the database.

from flask import Flask, request, jsonify, render_template
from app.rules import create_rule, combine_rules, evaluate_rule, serialize_ast, deserialize_ast, RuleEngineError
from app.database import save_rule, load_rules

def init_app(app: Flask):
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/create_rule', methods=['POST'])
    def create_rule_api():
        rule_string = request.json.get('rule_string')
        if not rule_string:
            return jsonify({"status": "error", "message": "No rule string provided."}), 400
        
        try:
            ast = create_rule(rule_string)
            ast_json = serialize_ast(ast)
            save_rule(rule_string, ast_json)
            return jsonify({"status": "success", "ast": ast_json})
        except RuleEngineError as e:
            return jsonify({"status": "error", "message": str(e)}), 400
        
    @app.route('/evaluate_rule', methods=['POST'])
    def evaluate_rule_api():
        ast_json = request.json.get('ast')
        data = request.json.get('data')

        if not ast_json or not data:
            return jsonify({"status": "error", "message": "Invalid input for evaluation."}), 400
        
        try:
            ast = deserialize_ast(ast_json)
            result = evaluate_rule(ast, data)
            return jsonify({"status": "success", "result": result})
        except RuleEngineError as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    @app.route('/combine_rules', methods=['POST'])
    def combine_rules_api():
        rule_strings = request.json.get('rule_strings')
        if not rule_strings or not isinstance(rule_strings, list):
            return jsonify({"status": "error", "message": "Invalid rule strings format."}), 400

        try:
            rules = [create_rule(rule) for rule in rule_strings]
            combined_ast = combine_rules(rules)
            combined_ast_json = serialize_ast(combined_ast)
            save_rule("combined_rule", combined_ast_json)
            return jsonify({"status": "success", "combined_ast": combined_ast_json})
        except RuleEngineError as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    

    @app.route('/load_rules', methods=['GET'])
    def load_rules_api():
        try:
            rules = load_rules()
            return jsonify({"status": "success", "rules": rules})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

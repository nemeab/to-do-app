from flask import Flask, request, jsonify
import os

app = Flask(__name__)
todos = []

@app.route('/')
def home():
    return "Welcome to the To-Do App!"

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    todos.append(data)
    return jsonify({"message": "Todo added!"}), 201

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

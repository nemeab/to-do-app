from flask import Flask, request, jsonify, render_template
import os
import uuid
from datetime import datetime

app = Flask(__name__)
todos = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/todos', methods=['GET'])
def get_todos():
    now = datetime.now()
    for todo in todos:
        if todo.get('deadline'):
            deadline = datetime.strptime(todo['deadline'], "%Y-%m-%dT%H:%M")
            time_left = deadline - now
            todo['time_left'] = str(time_left).split('.')[0] if time_left.total_seconds() > 0 else "Past Due"
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_todo = {
        "id": str(uuid.uuid4()),
        "text": data.get('text', ''),
        "deadline": data.get('deadline'),
        "completed": False
    }
    todos.append(new_todo)
    return jsonify({"message": "Todo added!"}), 201

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return jsonify({"message": "Todo deleted!"}), 200

@app.route('/todos/<todo_id>/complete', methods=['PATCH'])
def complete_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = True
            break
    return jsonify({"message": "Todo completed!"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

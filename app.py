from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates')
import uuid
from datetime import datetime, timedelta

todos = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/todos', methods=['GET'])
def get_todos():
    # Calculate time left for each todo if deadline is set
    result = []
    now = datetime.utcnow()
    for todo in todos:
        todo_copy = todo.copy()
        if 'deadline' in todo_copy and todo_copy['deadline']:
            try:
                deadline_dt = datetime.strptime(todo_copy['deadline'], '%Y-%m-%dT%H:%M')
                time_left = deadline_dt - now
                if time_left.total_seconds() > 0:
                    todo_copy['time_left'] = str(time_left).split('.')[0]  # Remove microseconds
                else:
                    todo_copy['time_left'] = 'Time is up!'
            except Exception:
                todo_copy['time_left'] = 'Invalid deadline'
        result.append(todo_copy)
    return jsonify(result)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    todo = {
        'id': str(uuid.uuid4()),
        'text': data.get('text', ''),
        'completed': False,
        'deadline': data.get('deadline', None)
    }
    todos.append(todo)
    return jsonify(todo), 201

# Delete a todo by id
@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return jsonify({'message': 'Todo deleted'})

# Mark a todo as complete
@app.route('/todos/<todo_id>/complete', methods=['PATCH'])
def complete_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = True
            return jsonify({'message': 'Todo marked as complete'})
    return jsonify({'error': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run()

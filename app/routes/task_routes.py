from flask import Blueprint, request, jsonify
from app import db
from app.models import Task, User
from datetime import datetime
from app.utils.auth import require_api_key

task_bp = Blueprint('task_bp', __name__, url_prefix='/tasks')

# POST /tasks - Create a task
@task_bp.route('', methods=['POST'])
@require_api_key
def create_task():
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    due_date_str = data.get('due_date')
    status = data.get('status', 'pending')
    assigned_user_id = data.get('assignedUserId')

    # Validate required field
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    # Convert due date
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Invalid due_date format. Use YYYY-MM-DD.'}), 400

    # Validate user if provided
    if assigned_user_id:
        user = User.query.get(assigned_user_id)
        if not user:
            return jsonify({'error': 'Assigned user not found'}), 404

    task = Task(
        title=title,
        description=description,
        due_date=due_date,
        status=status,
        assigned_user_id=assigned_user_id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({'message': 'Task created successfully', 'task': task.to_dict()}), 201


# GET /tasks/:id - Get task by ID
@task_bp.route('/<int:task_id>', methods=['GET'])
@require_api_key
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task.to_dict()), 200


# GET /tasks - List all tasks (with optional filters)
@task_bp.route('', methods=['GET'])
@require_api_key
def list_tasks():
    status = request.args.get('status')
    assigned_user_id = request.args.get('assignedUserId', type=int)
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)

    query = Task.query

    if status:
        query = query.filter_by(status=status)
    if assigned_user_id:
        query = query.filter_by(assigned_user_id=assigned_user_id)

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    tasks = [task.to_dict() for task in pagination.items]

    return jsonify({
        'tasks': tasks,
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages
    }), 200

# PUT /tasks/:id - Update task details
@task_bp.route('/<int:task_id>', methods=['PUT'])
@require_api_key
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date_str = data.get('due_date')
    status = data.get('status')
    assigned_user_id = data.get('assignedUserId')

    if title:
        task.title = title
    if description:
        task.description = description
    if status:
        task.status = status
    if due_date_str:
        try:
            task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Invalid due_date format. Use YYYY-MM-DD.'}), 400
    if assigned_user_id is not None:
        user = User.query.get(assigned_user_id)
        if not user:
            return jsonify({'error': 'Assigned user not found'}), 404
        task.assigned_user_id = assigned_user_id

    db.session.commit()
    return jsonify({'message': 'Task updated successfully', 'task': task.to_dict()}), 200

# DELETE /tasks/:id - Delete task
@task_bp.route('/<int:task_id>', methods=['DELETE'])
@require_api_key
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200

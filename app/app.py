from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
from config import Config
from models import User, Item
from auth import generate_token, login_required, token_required

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Web Routes (Jinja Templates)

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise to login."""
    if 'token' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('login.html')

        user = User.find_by_email(email)
        if not user or not User.verify_password(user['password'], password):
            flash('Invalid email or password', 'error')
            return render_template('login.html')

        token = generate_token(user['id'])
        session['token'] = token
        session['user_id'] = user['id']
        session['user_name'] = user['name']

        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        if not email or not password or not name:
            flash('All fields are required', 'error')
            return render_template('register.html')

        existing_user = User.find_by_email(email)
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('register.html')

        user = User.create(email, password, name)
        token = generate_token(user['id'])
        session['token'] = token
        session['user_id'] = user['id']
        session['user_name'] = user['name']

        flash('Registration successful!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout user."""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard(current_user):
    """Dashboard page showing all items."""
    items = Item.get_all(user_id=current_user['id'])
    return render_template('dashboard.html', items=items, user=current_user)

@app.route('/items/new', methods=['GET', 'POST'])
@login_required
def new_item(current_user):
    """Create new item page."""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if not title:
            flash('Title is required', 'error')
            return render_template('item_form.html')

        Item.create(title, description or '', current_user['id'])
        flash('Item created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('item_form.html', item=None)

@app.route('/items/<item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(current_user, item_id):
    """Edit item page."""
    item = Item.get_by_id(item_id)

    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('dashboard'))

    if item['user_id'] != current_user['id']:
        flash('Unauthorized', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if not title:
            flash('Title is required', 'error')
            return render_template('item_form.html', item=item)

        Item.update(item_id, title=title, description=description)
        flash('Item updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('item_form.html', item=item)

@app.route('/items/<item_id>/delete', methods=['POST'])
@login_required
def delete_item(current_user, item_id):
    """Delete item."""
    item = Item.get_by_id(item_id)

    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('dashboard'))

    if item['user_id'] != current_user['id']:
        flash('Unauthorized', 'error')
        return redirect(url_for('dashboard'))

    Item.delete(item_id)
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


# API Routes (JSON responses)

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """API endpoint for user registration."""
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not email or not password or not name:
        return jsonify({'message': 'All fields are required'}), 400

    existing_user = User.find_by_email(email)
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 400

    user = User.create(email, password, name)
    token = generate_token(user['id'])

    return jsonify({
        'message': 'Registration successful',
        'token': token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user['name']
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """API endpoint for user login."""
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.find_by_email(email)
    if not user or not User.verify_password(user['password'], password):
        return jsonify({'message': 'Invalid email or password'}), 401

    token = generate_token(user['id'])

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user['name']
        }
    }), 200

@app.route('/api/items', methods=['GET', 'POST'])
@token_required
def api_items(current_user):
    """API endpoint to get all items or create a new item."""
    if request.method == 'GET':
        items = Item.get_all(user_id=current_user['id'])
        return jsonify({'items': items}), 200

    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        description = data.get('description', '')

        if not title:
            return jsonify({'message': 'Title is required'}), 400

        item = Item.create(title, description, current_user['id'])
        return jsonify({'message': 'Item created', 'item': item}), 201

@app.route('/api/items/<item_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def api_item(current_user, item_id):
    """API endpoint to get, update, or delete a specific item."""
    item = Item.get_by_id(item_id)

    if not item:
        return jsonify({'message': 'Item not found'}), 404

    if item['user_id'] != current_user['id']:
        return jsonify({'message': 'Unauthorized'}), 403

    if request.method == 'GET':
        return jsonify({'item': item}), 200

    if request.method == 'PUT':
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')

        if not title:
            return jsonify({'message': 'Title is required'}), 400

        updated_item = Item.update(item_id, title=title, description=description)
        return jsonify({'message': 'Item updated', 'item': updated_item}), 200

    if request.method == 'DELETE':
        Item.delete(item_id)
        return jsonify({'message': 'Item deleted'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

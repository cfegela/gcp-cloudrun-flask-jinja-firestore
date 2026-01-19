from datetime import datetime
from db import db
import bcrypt

class User:
    collection = 'users'

    @staticmethod
    def create(email, password, name):
        """Create a new user."""
        user_ref = db.collection(User.collection).document()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_data = {
            'id': user_ref.id,
            'email': email,
            'password': hashed_password.decode('utf-8'),
            'name': name,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        user_ref.set(user_data)
        return user_data

    @staticmethod
    def find_by_email(email):
        """Find user by email."""
        users = db.collection(User.collection).where('email', '==', email).limit(1).stream()
        for user in users:
            return user.to_dict()
        return None

    @staticmethod
    def find_by_id(user_id):
        """Find user by ID."""
        user_ref = db.collection(User.collection).document(user_id)
        user = user_ref.get()
        if user.exists:
            return user.to_dict()
        return None

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify password."""
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))


class Item:
    collection = 'items'

    @staticmethod
    def create(title, description, user_id):
        """Create a new item."""
        item_ref = db.collection(Item.collection).document()

        item_data = {
            'id': item_ref.id,
            'title': title,
            'description': description,
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        item_ref.set(item_data)
        return item_data

    @staticmethod
    def get_all(user_id=None):
        """Get all items, optionally filtered by user."""
        query = db.collection(Item.collection)
        if user_id:
            query = query.where('user_id', '==', user_id)

        items = []
        for item in query.stream():
            items.append(item.to_dict())
        return items

    @staticmethod
    def get_by_id(item_id):
        """Get item by ID."""
        item_ref = db.collection(Item.collection).document(item_id)
        item = item_ref.get()
        if item.exists:
            return item.to_dict()
        return None

    @staticmethod
    def update(item_id, title=None, description=None):
        """Update an item."""
        item_ref = db.collection(Item.collection).document(item_id)
        update_data = {'updated_at': datetime.utcnow()}

        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description

        item_ref.update(update_data)
        return Item.get_by_id(item_id)

    @staticmethod
    def delete(item_id):
        """Delete an item."""
        item_ref = db.collection(Item.collection).document(item_id)
        item_ref.delete()
        return True

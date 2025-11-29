from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, create_user, get_all_users, check_user_exists
import psycopg2

app = Flask(__name__)
CORS(app)

# Initialize database on startup
try:
    init_db()
    print("Database initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize database: {e}")
    print("Make sure PostgreSQL is running and credentials are correct in .env file")

@app.route('/api/users', methods=['POST'])
def add_user():
    """Create a new user or return existing user."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'phone', 'customerEmail', 'location', 'storeName', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if user already exists by phone
        existing_user = check_user_exists(data['phone'])
        
        if existing_user:
            # User already exists
            user_dict = dict(existing_user)
            if user_dict.get('created_at'):
                user_dict['created_at'] = user_dict['created_at'].isoformat()
            
            return jsonify({
                'message': 'user_exists',
                'data': user_dict
            }), 200
        
        # Create new user
        user_id = create_user(data)
        
        return jsonify({
            'message': 'success',
            'data': data,
            'id': user_id
        }), 201
        
    except psycopg2.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/check/<phone>', methods=['GET'])
def check_phone(phone):
    """Check if a phone number already exists."""
    try:
        existing_user = check_user_exists(phone)
        
        if existing_user:
            user_dict = dict(existing_user)
            if user_dict.get('created_at'):
                user_dict['created_at'] = user_dict['created_at'].isoformat()
            
            return jsonify({
                'exists': True,
                'data': user_dict
            }), 200
        
        return jsonify({
            'exists': False
        }), 200
        
    except psycopg2.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def list_users():
    """Get all users."""
    try:
        users = get_all_users()
        
        # Convert datetime objects to strings for JSON serialization
        users_list = []
        for user in users:
            user_dict = dict(user)
            if user_dict.get('created_at'):
                user_dict['created_at'] = user_dict['created_at'].isoformat()
            users_list.append(user_dict)
        
        return jsonify({
            'message': 'success',
            'data': users_list
        }), 200
        
    except psycopg2.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)

import json
import os
import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, role="student"):
    try:
        user_data = {
            "username" : username,
            "password" : hash_password(password),
            "role" : role,
            "created_date" : datetime.now().strftime("%Y-%m-%d"),
            "stats" :   {
                "tests_taken": 0,
                "total_score": 0,
                "average_score": 0,
                "test_history": []
                        }
                    }
        
        user_file = f'users/{username}.json'
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=4)
            
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def authenticate_user(username, password):
    user_file = f'users/{username}.json'
    
    if not os.path.exists(user_file):
        return None
        
    try:
        with open(user_file, 'r') as f:
            user_data = json.load(f)
            
        if user_data['password'] == hash_password(password):
            return user_data
        else:
            return None
            
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None
    
def update_user_stats(username, score, max_score):
    user_file = f'users/{username}.json'
    
    try:
        with open(user_file, 'r') as f:
            user_data = json.load(f)
            
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        
        user_data['stats']['tests_taken'] += 1
        user_data['stats']['total_score'] += percentage
        user_data['stats']['average_score'] = user_data['stats']['total_score'] / user_data['stats']['tests_taken']
        test_record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "score": score,
            "max_score": max_score,
            "percentage": percentage
        }
        user_data['stats']['test_history'].append(test_record)
        
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=4)
            
        return True
    except Exception as e:
        print(f"Error updating user stats: {e}")
        return False
    
def get_all_users():
    users = []
    users_dir = 'users'
    
    try:
        for filename in os.listdir(users_dir):
            if filename.endswith('.json'):
                with open(os.path.join(users_dir, filename), 'r') as f:
                    user_data = json.load(f)
                    user_data.pop('password', None)
                    users.append(user_data)
    except Exception as e:
        print(f"Error getting users: {e}")
        
    return users
    
def save_analytics_data(data):
    try:
        analytics_file = 'analytics/analytics_data.json'
        
        if os.path.exists(analytics_file):
            with open(analytics_file, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = {"records": []}
            
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        existing_data['records'].append(data)
        
        with open(analytics_file, 'w') as f:
            json.dump(existing_data, f, indent=4)
            
            return True
    except Exception as e:
        print(f"Error saving analytics: {e}")
        return False
    
def get_analytics_data():
    
    try:
        analytics_file = 'analytics/analytics_data.json'
        if os.path.exists(analytics_file):
            with open(analytics_file, 'r') as f:
                return json.load(f)
        else:
            return {"records": []}
    except Exception as e:
        print(f"Error getting analytics: {e}")
        return {"records": []}
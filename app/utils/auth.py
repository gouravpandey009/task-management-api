from flask import request, jsonify
import os

def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if not api_key or api_key != os.getenv("API_KEY"):
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__ 
    return wrapper

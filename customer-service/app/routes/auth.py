# app/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from app.models import User
from app import db

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    # Check for required fields
    required_fields = ["username", "email", "password", "firstname", "lastname", "role"]
    if not all(data.get(field) for field in required_fields):
        return jsonify({"message": "Missing fields"}), 400
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "Username already exists"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400
    # Create user with new fields
    user = User(
        username=data["username"],
        email=data["email"],
        firstname=data["firstname"],
        lastname=data["lastname"],
        role=data["role"]
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()
    if user and user.check_password(data.get("password")):
        access_token = create_access_token(identity=str(user.id))  # <-- Cast to str
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401

from flask import current_app

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)  # Use Session.get() instead of Query.get()
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({
        "username": user.username,
        "email": user.email,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "role": user.role,
        "created_at": user.created_at.isoformat() if hasattr(user, "created_at") else None
    }), 200
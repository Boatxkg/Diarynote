from flask import Blueprint, request, jsonify
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# ✅ เพิ่มบรรทัดนี้
blacklist = set()

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.objects(username=data['username']):
        return jsonify({"msg": "Username already exists"}), 400
    hashed_pw = generate_password_hash(data['password'])
    user = User(username=data['username'], password=hashed_pw)
    user.save()
    return jsonify({"msg": "User registered successfully"})

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.objects(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"msg": "Invalid credentials"}), 401
    token = create_access_token(identity=str(user.id))
    return jsonify(access_token=token)

@auth.route('/showuser', methods=['GET'])
def showuser():
    all_users = User.objects()
    return jsonify([
        {
            "id": str(user.id),
            "username": user.username,
        } for user in all_users
    ])

@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify(msg="Logged out"), 200

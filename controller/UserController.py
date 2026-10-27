from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from models.extension import db
from models.User import User


user_api = Blueprint(
    "user_api",
    __name__,
    url_prefix="/api"
)


def admin_required():
    if not current_user.is_authenticated:
        return jsonify({
            "error": "Anda harus login."
        }), 401

    if str(current_user.role).upper() != "ADMIN":
        return jsonify({
            "error": "Hanya Admin yang dapat mengakses fitur ini."
        }), 403

    return None


# =========================================================
# GET SEMUA USER
# =========================================================

@user_api.route("/users", methods=["GET"])
@login_required
def get_users():

    error = admin_required()

    if error:
        return error

    users = User.query.order_by(
        User.id.desc()
    ).all()

    return jsonify([
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": str(user.role).upper(),
            "is_active": user.is_active,
            "created_at": (
                user.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if user.created_at
                else None
            )
        }
        for user in users
    ]), 200


# =========================================================
# GET USER BERDASARKAN ID
# =========================================================

@user_api.route("/users/<int:user_id>", methods=["GET"])
@login_required
def get_user(user_id):

    error = admin_required()

    if error:
        return error

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "Pengguna tidak ditemukan."
        }), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": str(user.role).upper(),
        "is_active": user.is_active
    }), 200


# =========================================================
# CREATE USER
# =========================================================

@user_api.route("/users", methods=["POST"])
@login_required
def create_user():

    error = admin_required()

    if error:
        return error

    data = request.get_json() or {}

    username = str(
        data.get("username", "")
    ).strip()

    nama_lengkap = (
        data.get('nama_lengkap') or username
    ).strip()

    email = str(
        data.get("email", "")
    ).strip().lower()

    password = data.get("password", "")

    role = str(
        data.get("role", "USER")
    ).strip().upper()

    # -----------------------------------------
    # VALIDASI
    # -----------------------------------------

    if not username:
        return jsonify({
            "error": "Username wajib diisi."
        }), 400

    if not email:
        return jsonify({
            "error": "Email wajib diisi."
        }), 400

    if not password:
        return jsonify({
            "error": "Password wajib diisi."
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password minimal 8 karakter."
        }), 400

    if role not in ["ADMIN", "PIC", "USER"]:
        return jsonify({
            "error": "Role tidak valid."
        }), 400

    # -----------------------------------------
    # CEK DUPLIKAT USERNAME
    # -----------------------------------------

    existing_username = User.query.filter_by(
        username=username
    ).first()

    if existing_username:
        return jsonify({
            "error": "Username sudah digunakan."
        }), 409

    # -----------------------------------------
    # CEK DUPLIKAT EMAIL
    # -----------------------------------------

    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        return jsonify({
            "error": "Email sudah digunakan."
        }), 409

    # -----------------------------------------
    # CREATE
    # -----------------------------------------

    user = User(
        username=username,
        nama_lengkap=nama_lengkap,
        email=email,
        role=role,
        is_active=True
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        # "message": "Pengguna berhasil dibuat.",
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }), 201


# =========================================================
# UPDATE USER
# =========================================================

@user_api.route("/users/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id):

    error = admin_required()

    if error:
        return error

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "Pengguna tidak ditemukan."
        }), 404

    data = request.get_json() or {}

    username = str(
        data.get("username", user.username)
    ).strip()

    email = str(
        data.get("email", user.email)
    ).strip().lower()

    role = str(
        data.get("role", user.role)
    ).strip().upper()

    password = data.get("password")

    # -----------------------------------------
    # VALIDASI
    # -----------------------------------------

    if not username:
        return jsonify({
            "error": "Username wajib diisi."
        }), 400

    if not email:
        return jsonify({
            "error": "Email wajib diisi."
        }), 400

    if role not in ["ADMIN", "PIC", "USER"]:
        return jsonify({
            "error": "Role tidak valid."
        }), 400

    # -----------------------------------------
    # CEK USERNAME
    # -----------------------------------------

    duplicate_username = User.query.filter(
        User.username == username,
        User.id != user.id
    ).first()

    if duplicate_username:
        return jsonify({
            "error": "Username sudah digunakan."
        }), 409

    # -----------------------------------------
    # CEK EMAIL
    # -----------------------------------------

    duplicate_email = User.query.filter(
        User.email == email,
        User.id != user.id
    ).first()

    if duplicate_email:
        return jsonify({
            "error": "Email sudah digunakan."
        }), 409

    # -----------------------------------------
    # UPDATE
    # -----------------------------------------

    user.username = username
    user.email = email
    user.role = role

    # Password hanya diubah jika diisi
    if password:

        if len(password) < 8:
            return jsonify({
                "error": "Password minimal 8 karakter."
            }), 400

        user.set_password(password)

    db.session.commit()

    return jsonify({
        "message": "Pengguna berhasil diperbarui.",
        "id": user.id,
        "username": user.username
    }), 200


# =========================================================
# DELETE USER
# =========================================================

@user_api.route("/users/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):

    error = admin_required()

    if error:
        return error

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "error": "Pengguna tidak ditemukan."
        }), 404

    # Tidak boleh menghapus akun sendiri
    if user.id == current_user.id:
        return jsonify({
            "error": "Anda tidak dapat menghapus akun sendiri."
        }), 400

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "message": "Pengguna berhasil dihapus."
    }), 200
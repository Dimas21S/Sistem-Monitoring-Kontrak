from flask import (
    Blueprint,
    request,
    jsonify,
    session
)

from models.extension import db
from models.User import User


user_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users"
)


# =========================================================
# CEK ADMIN
# =========================================================

def admin_required():
    """
    Memastikan hanya Administrator yang dapat
    mengakses fitur manajemen pengguna.
    """

    if "user_id" not in session:
        return False

    if session.get("role") != "Administrator":
        return False

    return True


# =========================================================
# DAFTAR USER
# =========================================================

@user_bp.route("", methods=["GET"])
def index():

    if not admin_required():
        return jsonify({
            "success": False,
            "message": "Akses ditolak."
        }), 403

    search = request.args.get(
        "search",
        "",
        type=str
    ).strip()

    role = request.args.get(
        "role",
        "",
        type=str
    ).strip()

    status = request.args.get(
        "status",
        "",
        type=str
    ).strip()

    query = User.query

    # SEARCH
    if search:
        query = query.filter(
            db.or_(
                User.nama.ilike(f"%{search}%"),
                User.username.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    # FILTER ROLE
    if role:
        query = query.filter(
            User.role == role
        )

    # FILTER STATUS
    if status:
        query = query.filter(
            User.status == status
        )

    users = query.order_by(
        User.id.desc()
    ).all()

    return jsonify({
        "success": True,
        "data": [
            user.to_dict()
            for user in users
        ]
    })


# =========================================================
# DETAIL USER
# =========================================================

@user_bp.route("/<int:user_id>", methods=["GET"])
def detail(user_id):

    if not admin_required():
        return jsonify({
            "success": False,
            "message": "Akses ditolak."
        }), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "Pengguna tidak ditemukan."
        }), 404

    return jsonify({
        "success": True,
        "data": user.to_dict()
    })


# =========================================================
# TAMBAH USER
# =========================================================

@user_bp.route("", methods=["POST"])
def create():

    if not admin_required():
        return jsonify({
            "success": False,
            "message": "Akses ditolak."
        }), 403

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Data pengguna tidak ditemukan."
        }), 400

    nama = data.get("nama", "").strip()
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    role = data.get("role", "User")
    status = data.get("status", "Aktif")

    # VALIDASI
    if not nama:
        return jsonify({
            "success": False,
            "message": "Nama wajib diisi."
        }), 400

    if not username:
        return jsonify({
            "success": False,
            "message": "Username wajib diisi."
        }), 400

    if not email:
        return jsonify({
            "success": False,
            "message": "Email wajib diisi."
        }), 400

    if not password:
        return jsonify({
            "success": False,
            "message": "Password wajib diisi."
        }), 400

    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password minimal 8 karakter."
        }), 400

    # CEK USERNAME
    existing_username = User.query.filter_by(
        username=username
    ).first()

    if existing_username:
        return jsonify({
            "success": False,
            "message": "Username sudah digunakan."
        }), 409

    # CEK EMAIL
    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        return jsonify({
            "success": False,
            "message": "Email sudah digunakan."
        }), 409

    # VALIDASI ROLE
    allowed_roles = [
        "Administrator",
        "User"
    ]

    if role not in allowed_roles:
        return jsonify({
            "success": False,
            "message": "Role tidak valid."
        }), 400

    # VALIDASI STATUS
    allowed_status = [
        "Aktif",
        "Nonaktif"
    ]

    if status not in allowed_status:
        return jsonify({
            "success": False,
            "message": "Status tidak valid."
        }), 400

    # CREATE USER
    user = User(
        nama=nama,
        username=username,
        email=email,
        role=role,
        status=status
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Pengguna berhasil ditambahkan.",
        "data": user.to_dict()
    }), 201


# =========================================================
# UPDATE USER
# =========================================================

@user_bp.route("/<int:user_id>", methods=["PUT"])
def update(user_id):

    if not admin_required():
        return jsonify({
            "success": False,
            "message": "Akses ditolak."
        }), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "Pengguna tidak ditemukan."
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Data tidak ditemukan."
        }), 400

    nama = data.get("nama", "").strip()
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    role = data.get("role")
    status = data.get("status")

    if not nama:
        return jsonify({
            "success": False,
            "message": "Nama wajib diisi."
        }), 400

    if not username:
        return jsonify({
            "success": False,
            "message": "Username wajib diisi."
        }), 400

    if not email:
        return jsonify({
            "success": False,
            "message": "Email wajib diisi."
        }), 400

    # CEK USERNAME MILIK USER LAIN
    existing_username = User.query.filter(
        User.username == username,
        User.id != user_id
    ).first()

    if existing_username:
        return jsonify({
            "success": False,
            "message": "Username sudah digunakan."
        }), 409

    # CEK EMAIL MILIK USER LAIN
    existing_email = User.query.filter(
        User.email == email,
        User.id != user_id
    ).first()

    if existing_email:
        return jsonify({
            "success": False,
            "message": "Email sudah digunakan."
        }), 409

    # VALIDASI ROLE
    allowed_roles = [
        "Administrator",
        "User"
    ]

    if role not in allowed_roles:
        return jsonify({
            "success": False,
            "message": "Role tidak valid."
        }), 400

    # VALIDASI STATUS
    allowed_status = [
        "Aktif",
        "Nonaktif"
    ]

    if status not in allowed_status:
        return jsonify({
            "success": False,
            "message": "Status tidak valid."
        }), 400

    # UPDATE
    user.nama = nama
    user.username = username
    user.email = email
    user.role = role
    user.status = status

    # PASSWORD OPSIONAL
    password = data.get("password")

    if password:
        if len(password) < 8:
            return jsonify({
                "success": False,
                "message": "Password minimal 8 karakter."
            }), 400

        user.set_password(password)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Pengguna berhasil diperbarui.",
        "data": user.to_dict()
    })


# =========================================================
# HAPUS USER
# =========================================================

@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete(user_id):

    if not admin_required():
        return jsonify({
            "success": False,
            "message": "Akses ditolak."
        }), 403

    # TIDAK BOLEH HAPUS DIRI SENDIRI
    if session.get("user_id") == user_id:
        return jsonify({
            "success": False,
            "message": "Anda tidak dapat menghapus akun sendiri."
        }), 400

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "Pengguna tidak ditemukan."
        }), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Pengguna berhasil dihapus."
    })


# =========================================================
# AKTIFKAN / NONAKTIFKAN USER
# =========================================================

@user_bp.route("/<int:user_id>/status", methods=["PATCH"])
def update_status(user_id):

    if not admin_required():
        return jsonify({
            "success": False,
            "message": "Akses ditolak."
        }), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "Pengguna tidak ditemukan."
        }), 404

    # Tidak boleh menonaktifkan diri sendiri
    if session.get("user_id") == user_id:
        return jsonify({
            "success": False,
            "message": "Anda tidak dapat menonaktifkan akun sendiri."
        }), 400

    data = request.get_json()

    status = data.get("status")

    if status not in ["Aktif", "Nonaktif"]:
        return jsonify({
            "success": False,
            "message": "Status tidak valid."
        }), 400

    user.status = status

    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"Status pengguna berhasil diubah menjadi {status}.",
        "data": user.to_dict()
    })
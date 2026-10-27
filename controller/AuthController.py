from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    get_flashed_messages
)

from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user
)

from werkzeug.security import check_password_hash
from itsdangerous import URLSafeTimedSerializer

from models.User import User
from models.extension import db


def auth_routes(app):

    @app.route("/login", methods=["GET", "POST"])
    def login():
        # Jika pengguna sudah login
        if current_user.is_authenticated:
            role = str(current_user.role).strip().upper()

            if role == "ADMIN":
                return redirect(url_for("index_pengguna"))

            elif role == "PIC":
                return redirect(url_for("data_kontrak"))

            elif role == "USER":
                return redirect(url_for("dashboard"))

            return redirect(url_for("dashboard"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            # Validasi input
            if not username or not password:
                flash(
                    "Username dan password wajib diisi.",
                    "warning"
                )
                return render_template("login.html")

            # Cari user berdasarkan username
            user = User.query.filter_by(
                username=username
            ).first()

            # Username tidak ditemukan
            if not user:
                flash(
                    "Username atau password salah.",
                    "error"
                )
                return render_template("login.html")

            # Akun tidak aktif
            if not user.is_active:
                flash(
                    "Akun Anda tidak aktif. Silakan hubungi administrator.",
                    "warning"
                )
                return render_template("login.html")

            # Verifikasi password
            if not check_password_hash(
                user.password_hash,
                password
            ):
                flash(
                    "Username atau password salah.",
                    "error"
                )
                return render_template("login.html")

            # Login menggunakan Flask-Login
            login_user(user)

            flash(
                f"Selamat datang, "
                f"{getattr(user, 'nama_lengkap', None) or user.username}.",
                "success"
            )

            # Redirect berdasarkan role
            role = str(user.role).strip().upper()

            if role == "ADMIN":
                return redirect(url_for("index_pengguna"))

            elif role == "PIC":
                return redirect(url_for("data_kontrak"))

            elif role == "USER":
                return redirect(url_for("dashboard"))

            return redirect(url_for("dashboard"))

        return render_template("login.html")


    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        get_flashed_messages(with_categories=True)
        logout_user()
        flash("Anda berhasil logout.", "success")
        return redirect(url_for("login"))


    # @app.route("/forgot-password")
    # def forgot_password():

    #     return render_template(
    #         "forgot-password.html"
    #     )

    @app.route("/forgot-password", methods=["GET", "POST"])
    def forgot_password():

        if request.method == "POST":

            username = request.form.get(
                "username",
                ""
            ).strip()

            if not username:
                flash(
                    "Username wajib diisi.",
                    "error"
                )
                return render_template(
                    "forgot-password.html"
                )

            user = User.query.filter_by(
                username=username
            ).first()

            if not user:
                flash(
                    "Username tidak ditemukan.",
                    "error"
                )
                return render_template(
                    "forgot-password.html"
                )

            if not user.is_active:
                flash(
                    "Akun tidak aktif. Silakan hubungi administrator.",
                    "error"
                )
                return render_template(
                    "forgot-password.html"
                )

            # =========================
            # BUAT TOKEN RESET
            # =========================

            serializer = URLSafeTimedSerializer(
                app.config["SECRET_KEY"]
            )

            token = serializer.dumps(
                user.id,
                salt="password-reset"
            )

            reset_url = url_for(
                "reset_password",
                token=token,
                _external=True
            )

            # Untuk sementara tampilkan link
            # di terminal Flask
            print("=" * 60)
            print("PASSWORD RESET LINK:")
            print(reset_url)
            print("=" * 60)

            flash(
                "Tautan reset password telah dibuat. "
                "Silakan periksa email Anda.",
                "success"
            )

            return redirect(
                url_for("forgot_password")
            )

        return render_template(
            "forgot-password.html"
        )


    @app.route("/reset-password/<token>", methods=["GET", "POST"])
    def reset_password(token):

        serializer = URLSafeTimedSerializer(
            app.config["SECRET_KEY"]
        )

        try:
            user_id = serializer.loads(
                token,
                salt="password-reset",
                max_age=1800
            )

        except Exception:
            flash(
                "Tautan reset password tidak valid atau sudah kedaluwarsa.",
                "error"
            )

            return redirect(
                url_for("forgot_password")
            )

        user = User.query.get(user_id)

        if not user:
            flash(
                "Akun tidak ditemukan.",
                "error"
            )

            return redirect(
                url_for("forgot_password")
            )

        if request.method == "POST":

            password = request.form.get(
                "password",
                ""
            )

            password_confirmation = request.form.get(
                "password_confirmation",
                ""
            )

            if not password:
                flash(
                    "Password baru wajib diisi.",
                    "error"
                )

                return render_template(
                    "reset-password.html"
                )

            if len(password) < 8:
                flash(
                    "Password minimal 8 karakter.",
                    "error"
                )

                return render_template(
                    "reset-password.html"
                )

            if password != password_confirmation:
                flash(
                    "Konfirmasi password tidak cocok.",
                    "error"
                )

                return render_template(
                    "reset-password.html"
                )

            from werkzeug.security import generate_password_hash

            user.password_hash = generate_password_hash(
                password
            )

            db.session.commit()

            flash(
                "Password berhasil diubah. Silakan login.",
                "success"
            )

            return redirect(
                url_for("login")
            )

        return render_template(
            "reset-password.html"
        )
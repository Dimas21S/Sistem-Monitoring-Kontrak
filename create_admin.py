from werkzeug.security import generate_password_hash

from app import app
from models.extension import db
from models.User import User


with app.app_context():

    # admin = User(
    #     username="mimin",
    #     nama_lengkap="Administrator",
    #     email="mimin@example.com",
    #     password_hash=generate_password_hash("mimin123"),
    #     role="ADMIN",
    #     is_active=True
    # )

    # pic = User(
    #     username="pic",
    #     nama_lengkap="PIC",
    #     email="pic@example.com",
    #     password_hash=generate_password_hash("pic123"),
    #     role="PIC",
    #     is_active=True
    # )

    pic1 = User(
        username="Rendy",
        nama_lengkap="Rendy",
        email="rendy@example.com",
        password_hash=generate_password_hash("rendy123"),
        role="PIC",
        is_active=True
    )

    # db.session.add(admin)
    # db.session.add(pic)
    db.session.add(pic1)
    db.session.commit()

    print("Admin dan PIC berhasil dibuat.")
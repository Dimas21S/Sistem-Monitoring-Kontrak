from .extension import db

class Dokumen(db.Model):
    __tablename__ = "document"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomor_thp = db.Column(db.Integer, nullable=False, unique=True)
    judul_dokumen = db.Column(db.String(255), nullable=False)
    subjudul = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    persyaratan = db.relationship("Persyaratan", backref="dokumen", lazy=True)

    status_tahapans = db.relationship("StatusTahapan", backref="dokumen", lazy=True)
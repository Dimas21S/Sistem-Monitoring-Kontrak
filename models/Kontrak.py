from .extension import db

class Kontrak(db.Model):
    __tablename__ = "kontrak"

    id = db.Column(db.Integer, primary_key=True)
    judul_kontrak = db.Column(db.String(255), nullable=False)
    lokasi_kontrak = db.Column(db.String(255), nullable=False)
    anggaran = db.Column(db.Float, nullable=False)
    tahun_wpb = db.Column(db.Integer, nullable=False)
    nilai = db.Column(db.Float, nullable=False)
    target_realisasi = db.Column(db.Date, nullable=False)
    pic = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    checklists = db.relationship("Checklist", backref="kontrak", lazy=True)
    status_tahapans = db.relationship("StatusTahapan", backref="kontrak", lazy=True)

    pic_user = db.relationship(
        'User',
        back_populates='kontrak'
    )
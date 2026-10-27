from .extension import db

class StatusTahapan(db.Model):
    __tablename__ = "status_tahapan"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_kontrak = db.Column(
        db.Integer,
        db.ForeignKey("kontrak.id"),
        nullable=False
    )

    id_document = db.Column(
        db.Integer,
        db.ForeignKey("document.id"),
        nullable=False
    )

    is_marked_done = db.Column(db.Boolean, default=False)
    marked_by = db.Column(db.String(100), nullable=True)
    marked_at = db.Column(db.DateTime, nullable=True)
    tanggal_mulai = db.Column(db.Date, nullable=True)
    target_hari = db.Column(db.Integer, nullable=True)
    tanggal_target = db.Column(db.Date, nullable=True)
    tanggal_selesai = db.Column(db.Date, nullable=True)
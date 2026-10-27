from .extension import db

class Checklist(db.Model):
    __tablename__ = "item_checklist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_kontrak = db.Column(
        db.Integer,
        db.ForeignKey("kontrak.id"),
        nullable=False
    )

    id_item = db.Column(
        db.Integer,
        db.ForeignKey("item_persyaratan.id"),
        nullable=False
    )

    is_done = db.Column(db.Boolean, default=False)
    catatan = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    tanggal_mulai = db.Column(db.Date, nullable=True)
    target_hari = db.Column(db.Integer, nullable=True)
    tanggal_target = db.Column(db.Date, nullable=True)
    tanggal_selesai = db.Column(db.Date, nullable=True)
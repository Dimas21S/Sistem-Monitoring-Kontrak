from .extension import db

class Persyaratan(db.Model):
    __tablename__ = "item_persyaratan"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    nomor_doc = db.Column(
        db.Integer,
        db.ForeignKey("document.id"),
        nullable=False
    )

    nomor_item = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String(255), nullable=False)

    tipe_item = db.Column(
        db.Enum(
            "checkbox",
            "upload",
            "approval",
            name="tipe_item_enum"
        ),
        nullable=False,
        default="checkbox"
    )

    is_required = db.Column(db.Boolean, default=True)

    checklists = db.relationship("Checklist", backref="persyaratan", lazy=True)
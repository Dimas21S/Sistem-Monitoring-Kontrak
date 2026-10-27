from models.Kontrak import Kontrak
from models.Dokumen import Dokumen
from models.Checklist import Checklist
from models.Persyaratan import Persyaratan
from models.StatusTahapan import StatusTahapan
from models.extension import db

from flask_login import current_user
from flask import render_template


def get_checklist_kontrak():
    if current_user.role == "PIC":
        kontrak_list = (
            Kontrak.query
            .filter_by(pic=current_user.id)
            .order_by(Kontrak.id.desc())
            .all()
        )
    else:
        kontrak_list = (
            Kontrak.query
            .order_by(Kontrak.id.desc())
            .all()
        )

    # kontrak_list = (Kontrak.query.order_by(Kontrak.id.desc()).all())

    dokumen_list = (Dokumen.query.order_by(Dokumen.nomor_thp.asc()).all())

    kontrak_data = []
    for kontrak in kontrak_list:
        print("\nKONTRAK:", kontrak.id, kontrak.judul_kontrak)

        tahapan_data = []
        for dokumen in dokumen_list:
            status = StatusTahapan.query.filter_by(id_kontrak=kontrak.id, id_document=dokumen.id).first()

            checklist_items = (
                db.session.query(Checklist, Persyaratan)
                .join(
                    Persyaratan,
                    Checklist.id_item == Persyaratan.id
                )
                .filter(
                    Checklist.id_kontrak == kontrak.id,
                    Persyaratan.nomor_doc == dokumen.id
                )
                .order_by(
                    Persyaratan.nomor_item.asc()
                )
                .all()
            )

            items_data = []

            for checklist, persyaratan in checklist_items:
                items_data.append({
                    "id_checklist": checklist.id,
                    "id_item": persyaratan.id,
                    "nomor_item": persyaratan.nomor_item,
                    "label": persyaratan.label,
                    "tipe_item": persyaratan.tipe_item,
                    "is_required": persyaratan.is_required,
                    "is_done": checklist.is_done,
                    "tanggal_mulai": (
                        checklist.tanggal_mulai.isoformat()
                        if checklist.tanggal_mulai
                        else None
                    ),

                    "target_hari": checklist.target_hari,

                    "tanggal_target": (
                        checklist.tanggal_target.isoformat()
                        if checklist.tanggal_target
                        else None
                    ),

                    "tanggal_selesai": (
                        checklist.tanggal_selesai.isoformat()
                        if checklist.tanggal_selesai
                        else None
                    )
                })

            tahapan_data.append({
                "dokumen": {
                    "id": dokumen.id,
                    "nomor_thp": dokumen.nomor_thp,
                    "judul_dokumen": dokumen.judul_dokumen,
                    "subjudul": dokumen.subjudul
                },
                "status": {
                    "id": status.id if status else None,

                    "is_marked_done":
                        status.is_marked_done if status else False,

                    "marked_by":
                        status.marked_by if status else None,

                    "marked_at":
                        status.marked_at.isoformat()
                        if status and status.marked_at
                        else None,

                    "tanggal_mulai":
                        status.tanggal_mulai.isoformat()
                        if status and status.tanggal_mulai
                        else None,

                    "target_hari":
                        status.target_hari
                        if status else None,

                    "tanggal_target":
                        status.tanggal_target.isoformat()
                        if status and status.tanggal_target
                        else None,

                    "tanggal_selesai":
                        status.tanggal_selesai.isoformat()
                        if status and status.tanggal_selesai
                        else None
                } if status else None,
                "checklist_items": items_data
                        })

        kontrak_data.append({
            "kontrak": {
                "id": kontrak.id,
                "judul_kontrak": kontrak.judul_kontrak,
                "lokasi_kontrak": kontrak.lokasi_kontrak,
                "anggaran": kontrak.anggaran,
                "tahun_wpb": kontrak.tahun_wpb,
                "nilai": kontrak.nilai,
                "target_realisasi": kontrak.target_realisasi.isoformat(),
                "pic": kontrak.pic,
                "status": kontrak.status
            },
            "tahapan_data": tahapan_data
        })

    persyaratan_list = (Persyaratan.query.order_by(Persyaratan.nomor_doc.asc(), Persyaratan.nomor_item.asc()).all())

    checklist_items = Checklist.query.all()

    status_tahapan_list = StatusTahapan.query.all()

    return kontrak_data
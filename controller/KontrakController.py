from models.Kontrak import Kontrak
from models.Dokumen import Dokumen
from models.Checklist import Checklist
from models.Persyaratan import Persyaratan
from models.StatusTahapan import StatusTahapan
from models.extension import db
from models.User import User

from flask import flash, redirect, request, url_for
from datetime import date, timedelta, datetime

def hitung_tanggal_target(tanggal_mulai, target_hari):
    return tanggal_mulai + timedelta(days=target_hari)

def hitung_prioritas(tanggal_target):

    hari_ini = date.today()
    sisa_hari = (tanggal_target - hari_ini).days

    if sisa_hari < 0:
        prioritas = "Terlambat"
    elif sisa_hari <= 3:
        prioritas = "Mendesak"
    elif sisa_hari <= 7:
        prioritas = "Segera"
    else:
        prioritas = "Normal"

    return {
        "sisa_hari": sisa_hari,
        "prioritas": prioritas
    }

def create_new_contract():

    if request.method == "POST":

        try:

            judul_kontrak = request.form.get("judul_kontrak")
            lokasi_kontrak = request.form.get("lokasi_kontrak")
            anggaran = request.form.get("anggaran")
            tahun_wpb = request.form.get("tahun_wpb")
            nilai = request.form.get("nilai")
            target_realisasi = request.form.get("target_realisasi")
            pic = request.form.get("pic")
            status = request.form.get("status")

            if not all([
                judul_kontrak,
                lokasi_kontrak,
                anggaran,
                tahun_wpb,
                nilai,
                target_realisasi,
                pic,
                status
            ]):
                flash("Semua field harus diisi.", "error")
                return redirect(url_for("tambah_kontrak"))

            anggaran = float(anggaran)
            nilai = float(nilai)
            tahun_wpb = int(tahun_wpb)
            target_realisasi_date = date.fromisoformat(target_realisasi)
            pic = int(pic)

            pic_user = User.query.filter_by(
                id=pic,
                role="PIC"
            ).first()

            if not pic_user:
                flash(
                    "PIC yang dipilih tidak valid.",
                    "error"
                )
                return redirect(url_for("tambah_kontrak"))

            kontrak_baru = Kontrak(
                judul_kontrak=judul_kontrak,
                lokasi_kontrak=lokasi_kontrak,
                anggaran=anggaran,
                tahun_wpb=tahun_wpb,
                nilai=nilai,
                target_realisasi=target_realisasi_date,
                pic=pic_user.id,
                status=status
            )

            db.session.add(kontrak_baru)
            db.session.flush()

            list_dokument = (
                Dokumen.query
                .filter_by(is_active=True)
                .order_by(Dokumen.nomor_thp.asc())
                .all()
            )
            for dokumen in list_dokument:
                status_tahapan = StatusTahapan(
                    id_kontrak=kontrak_baru.id,
                    id_document=dokumen.id,
                    is_marked_done=False
                )

                db.session.add(status_tahapan)

            persyaratan_list = (
                Persyaratan.query
                .order_by(
                    Persyaratan.nomor_doc.asc(),
                    Persyaratan.nomor_item.asc()
                )
                .all()
            )

            for persyaratan in persyaratan_list:
                checklist_item = Checklist(
                    id_kontrak=kontrak_baru.id,
                    id_item=persyaratan.id,
                    is_done=False,
                    catatan=None,
                    updated_at=db.func.current_timestamp()
                )

                db.session.add(checklist_item)

            db.session.commit()

            flash(
                "Data kontrak berhasil disimpan.",
                "success"
            )

            return redirect(url_for("data_kontrak"))

        except ValueError as e:

            db.session.rollback()

            flash(
                "Format data tidak valid. "
                "Periksa kembali angka, tahun, dan tanggal.",
                "danger"
            )

            return redirect(url_for("tambah_kontrak"))

        except Exception as e:

            db.session.rollback()
            flash(
                f"Terjadi kesalahan saat menyimpan data: {str(e)}",
                "danger"
            )

            return redirect(url_for("tambah_kontrak"))

def get_startitem_checklist(id_checklist):

    checklist = db.session.get(Checklist, id_checklist)

    if not checklist:
        return {
            "success": False,
            "message": "Checklist tidak ditemukan"
        }, 404

    data = request.get_json() or {}

    target_hari = data.get("target_hari")

    if target_hari is None:
        return {
            "success": False,
            "message": "Target hari harus diisi"
        }, 400

    try:
        target_hari = int(target_hari)
    except (ValueError, TypeError):
        return {
            "success": False,
            "message": "Target hari harus berupa angka"
        }, 400

    if target_hari <= 0:
        return {
            "success": False,
            "message": "Target hari harus lebih dari 0"
        }, 400

    tanggal_mulai = date.today()

    tanggal_target = hitung_tanggal_target(
        tanggal_mulai,
        target_hari
    )

    checklist.tanggal_mulai = tanggal_mulai
    checklist.target_hari = target_hari
    checklist.tanggal_target = tanggal_target
    checklist.tanggal_selesai = None

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    informasi = hitung_prioritas(tanggal_target)

    return {
        "success": True,
        "message": "Target persyaratan berhasil disimpan",

        "id_checklist": checklist.id,
        "tanggal_mulai": tanggal_mulai.isoformat(),
        "target_hari": target_hari,
        "tanggal_target": tanggal_target.isoformat(),
        "tanggal_selesai": None,

        "sisa_hari": informasi["sisa_hari"],
        "prioritas": informasi["prioritas"]
    }, 200

def update_progres_tahapan(data):

    kontrak_id = data.get("id_kontrak")
    dokumen_id = data.get("id_document")
    is_marked_done = data.get("is_marked_done")

    print("kontrak_id:", kontrak_id)
    print("dokumen_id:", dokumen_id)
    print("is_marked_done:", is_marked_done)

    status = StatusTahapan.query.filter_by(
        id_kontrak=kontrak_id,
        id_document=dokumen_id
    ).first()

    print("STATUS DITEMUKAN:", status)

    if not status:
        return {
            "success": False,
            "message": "Status tahapan tidak ditemukan"
        }, 404

    status.is_marked_done = bool(is_marked_done)

    if status.is_marked_done:
        status.marked_at = datetime.now()
        status.marked_by = "User"
    else:
        status.marked_at = None
        status.marked_by = None

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return {
        "success": True,
        "message": "Status tahapan berhasil diperbarui"
    }, 200

def aktifkan_tahap_berikutnya(id_kontrak, id_document):

    tahap_sekarang = Dokumen.query.get(id_document)

    if not tahap_sekarang:
        return

    # Cari tahap berikutnya berdasarkan nomor tahapan
    tahap_berikutnya = (
        Dokumen.query
        .filter(
            Dokumen.nomor_thp > tahap_sekarang.nomor_thp,
            Dokumen.is_active == True
        )
        .order_by(Dokumen.nomor_thp.asc())
        .first()
    )

    # Tidak ada tahap berikutnya
    if not tahap_berikutnya:
        return

    # Status tahap sekarang
    status_sekarang = StatusTahapan.query.filter_by(
        id_kontrak=id_kontrak,
        id_document=id_document
    ).first()

    # Status tahap berikutnya
    status_berikutnya = StatusTahapan.query.filter_by(
        id_kontrak=id_kontrak,
        id_document=tahap_berikutnya.id
    ).first()

    if not status_sekarang or not status_berikutnya:
        return

    # Jangan aktifkan lagi jika sudah pernah dimulai
    if status_berikutnya.tanggal_mulai:
        return

    # Tahap berikutnya mulai setelah tahap sekarang selesai
    if not status_sekarang.tanggal_selesai:
        return

    status_berikutnya.tanggal_mulai = (
        status_sekarang.tanggal_selesai
    )

    # Kalau target hari sudah ditentukan
    if status_berikutnya.target_hari:

        status_berikutnya.tanggal_target = (
            status_berikutnya.tanggal_mulai
            + timedelta(days=status_berikutnya.target_hari)
        )

def complete_tahapan(data):

    kontrak_id = data.get("id_kontrak")
    dokumen_id = data.get("id_document")

    if kontrak_id is None or dokumen_id is None:
        return {
            "success": False,
            "message": "ID kontrak atau dokumen tidak ditemukan"
        }, 400

    # =========================
    # AMBIL SEMUA CHECKLIST
    # =========================

    checklist_items = (
        db.session.query(Checklist)
        .join(
            Persyaratan,
            Checklist.id_item == Persyaratan.id
        )
        .filter(
            Checklist.id_kontrak == kontrak_id,
            Persyaratan.nomor_doc == dokumen_id
        )
        .all()
    )

    # =========================
    # CARI STATUS TAHAPAN
    # =========================

    status_tahapan = StatusTahapan.query.filter_by(
        id_kontrak=kontrak_id,
        id_document=dokumen_id
    ).first()

    if not status_tahapan:
        return {
            "success": False,
            "message": "Status tahapan tidak ditemukan"
        }, 404

    # =========================
    # SELESAIKAN CHECKLIST
    # =========================

    tanggal_selesai = date.today()

    for checklist in checklist_items:

        checklist.is_done = True
        checklist.tanggal_selesai = tanggal_selesai

    # =========================
    # SELESAIKAN TAHAPAN
    # =========================

    status_tahapan.status = True
    status_tahapan.is_marked_done = True
    status_tahapan.tanggal_selesai = tanggal_selesai
    status_tahapan.marked_at = datetime.now()
    status_tahapan.marked_by = "User"

    # =========================
    # AKTIFKAN TAHAP BERIKUTNYA
    # =========================

    aktifkan_tahap_berikutnya(
        kontrak_id,
        dokumen_id
    )

    # =========================
    # SIMPAN
    # =========================

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return {
        "success": True,
        "message": "Tahapan berhasil diselesaikan",
        "updated": len(checklist_items)
    }, 200
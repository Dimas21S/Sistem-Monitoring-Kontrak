import os
from dotenv import load_dotenv
from datetime import date, datetime

from flask_login import LoginManager, current_user, login_required as flask_login_required
from models import User
from models.extension import db
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from sqlalchemy import func, or_
from datetime import date, timedelta, datetime

from utils.auth import login_required

from controller.SistemController import (get_dashboard_data, get_contract_progress)
from controller.KontrakController import (create_new_contract, get_startitem_checklist, update_progres_tahapan)
from controller.ChecklistController import (get_checklist_kontrak)
from controller.AuthController import auth_routes
from controller.AdminController import user_bp
from controller.UserController import user_api

from models.Kontrak import Kontrak
from models.Dokumen import Dokumen
from models.Checklist import Checklist
from models.Persyaratan import Persyaratan
from models.StatusTahapan import StatusTahapan
from models.User import User

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contracts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Silakan login terlebih dahulu."

db.init_app(app)

auth_routes(app)
app.register_blueprint(user_bp)
app.register_blueprint(user_api)

def format_currency(value):
    if value >= 1_000_000_000:
        return f"Rp {value / 1_000_000_000:.1f} M"
    return f"Rp {value / 1_000_000:.0f} jt"

def hitung_tanggal_target(tanggal_mulai, target_hari):
    if not tanggal_mulai or not target_hari:
        return None

    return tanggal_mulai + timedelta(days=target_hari)

def hitung_prioritas(tanggal_target):
    if not tanggal_target:
        return {
            "sisa_hari": None,
            "prioritas": "Normal"
        }

    sisa_hari = (tanggal_target - date.today()).days

    if sisa_hari <= 3:
        prioritas = "Tinggi"
    elif sisa_hari <= 7:
        prioritas = "Sedang"
    else:
        prioritas = "Normal"

    return {
        "sisa_hari": sisa_hari,
        "prioritas": prioritas
    }

@app.template_filter("currency")
def currency_filter(value):
    return format_currency(value)

@app.route("/")
@flask_login_required
def index():
    role = str(current_user.role).strip().upper()

    if role == "ADMIN":
        return redirect(url_for("index_pengguna"))

    elif role == "PIC":
        return redirect(url_for("form_inputan"))

    elif role == "USER":
        return redirect(url_for("dashboard"))

    return redirect(url_for("logout"))

# Tampilan dashboard utama
@app.get("/dashboard")
def dashboard():
    data = get_dashboard_data()
    daftar_pic = (
        User.query
        .filter_by(role="PIC")
        .order_by(User.nama_lengkap.asc())
        .all()
    )

    return render_template("index.html", **data, daftar_pic=daftar_pic)

# Tampilan form input data kontrak baru
@app.route("/form-inputan")
def form_inputan():
    return render_template("form-inputan.html")

# Tampilan chekclist tahapan dokumen dan persyaratan kontrak
@app.route("/checklist_kontrak")
def checklist_kontrak():
    kontrak_data = get_checklist_kontrak()

    return render_template(
        "checklist-kontrak.html", 
        kontrak_data=kontrak_data
    )

# Tampilan flowchart tahapan dokumen dan persyaratan kontrak
@app.route("/flowchart")
def flowchart():
    return render_template("flowchart.html")

# Route untuk menambahkan kontrak baru
@app.route("/tambah-kontrak", methods=["GET", "POST"])
def tambah_kontrak():
    if request.method == "POST":
        return create_new_contract()

    daftar_pic = User.query.filter_by(role="PIC").all()

    print("================================")
    print("JUMLAH PIC:", len(daftar_pic))

    for user in daftar_pic:
        print(
            "PIC:",
            user.id,
            user.nama_lengkap,
            user.username,
            user.role,
            user.is_active
        )

    return render_template("form-inputan.html", daftar_pic=daftar_pic)


@app.route("/api/tahapan/update", methods=["POST"])
def update_tahapan():
    try:
        data = request.get_json() or {}

        result, status_code = update_progres_tahapan(data)

        return jsonify(result), status_code

    except Exception as e:
        db.session.rollback()

        print("ERROR UPDATE TAHAPAN:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


def cek_tahapan_selesai(id_kontrak, id_document):

    checklist_items = (
        db.session.query(Checklist)
        .join(
            Persyaratan,
            Checklist.id_item == Persyaratan.id
        )
        .filter(
            Checklist.id_kontrak == id_kontrak,
            Persyaratan.nomor_doc == id_document,
            Persyaratan.is_required == True
        )
        .all()
    )

    # Kalau tidak ada item wajib,
    # jangan dianggap selesai otomatis
    if not checklist_items:
        return False

    return all(
        checklist.is_done
        for checklist in checklist_items
    )


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


@app.route("/api/checklist/update", methods=["POST"])
def update_checklist():
    try:
        data = request.get_json()

        id_checklist = data.get("id_checklist")
        is_done = data.get("is_done")

        if id_checklist is None or is_done is None:
            return jsonify({
                "success": False,
                "message": "Data checklist tidak lengkap"
            }), 400

        checklist = Checklist.query.get(id_checklist)

        if not checklist:
            return jsonify({
                "success": False,
                "message": "Checklist tidak ditemukan"
            }), 404

        checklist.is_done = bool(is_done)

        if checklist.is_done:
            checklist.tanggal_selesai = date.today()
        else:
            checklist.tanggal_selesai = None

        persyaratan = Persyaratan.query.get(
            checklist.id_item
        )

        if not persyaratan:
            return jsonify({
                "success": False,
                "message": "Persyaratan tidak ditemukan"
            }), 404

        id_document = persyaratan.nomor_doc

        status_tahapan = StatusTahapan.query.filter_by(
            id_kontrak=checklist.id_kontrak,
            id_document=id_document
        ).first()

        if not status_tahapan:
            return jsonify({
                "success": False,
                "message": "Status tahapan tidak ditemukan"
            }), 404

        # =========================
        # CEK SEMUA REQUIRED ITEM
        # =========================

        selesai = cek_tahapan_selesai(
            checklist.id_kontrak,
            id_document
        )

        if selesai:

            status_tahapan.status = True
            status_tahapan.tanggal_selesai = date.today()

        else:

            status_tahapan.status = False
            status_tahapan.tanggal_selesai = None

        db.session.commit()

        print("========== UPDATE CHECKLIST ==========")
        print("id_checklist:", checklist.id)
        print("is_done:", checklist.is_done)
        print("id_document:", id_document)
        print("tahapan_selesai:", selesai)
        print("COMMIT CHECKLIST BERHASIL")

        return jsonify({
            "success": True,
            "message": "Checklist berhasil diperbarui",
            "id_checklist": checklist.id,
            "is_done": checklist.is_done,
            "tahapan_selesai": selesai
        })

    except Exception as e:
        db.session.rollback()

        print("ERROR UPDATE CHECKLIST:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route("/api/tahapan/complete", methods=["POST"])
def complete_tahapan():

    try:

        data = request.get_json()

        kontrak_id = data.get("id_kontrak")
        dokumen_id = data.get("id_document")

        if kontrak_id is None or dokumen_id is None:
            return jsonify({
                "success": False,
                "message": "ID kontrak atau dokumen tidak ditemukan"
            }), 400

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
        # SELESAIKAN CHECKLIST
        # =========================

        for checklist in checklist_items:

            checklist.is_done = True
            checklist.tanggal_selesai = date.today()

        # =========================
        # CARI STATUS TAHAPAN
        # =========================

        status_tahapan = StatusTahapan.query.filter_by(
            id_kontrak=kontrak_id,
            id_document=dokumen_id
        ).first()

        if not status_tahapan:
            return jsonify({
                "success": False,
                "message": "Status tahapan tidak ditemukan"
            }), 404

        # =========================
        # SELESAIKAN TAHAPAN
        # =========================

        status_tahapan.status = True
        status_tahapan.is_marked_done = True
        status_tahapan.tanggal_selesai = date.today()
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
        # COMMIT
        # =========================

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Tahapan berhasil diselesaikan",
            "updated": len(checklist_items)
        })

    except Exception as e:

        db.session.rollback()

        print("ERROR COMPLETE TAHAPAN:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route("/update-status/<int:kontrak_id>", methods=["POST"])
def update_status(kontrak_id):

    kontrak = Kontrak.query.get_or_404(kontrak_id)

    data = request.get_json()
    status_baru = data.get("status")

    status_valid = [
        "Aktif",
        "Menunggu perpanjangan",
        "Draft"
    ]

    if status_baru not in status_valid:
        return jsonify({
            "success": False,
            "message": "Status tidak valid"
        }), 400

    kontrak.status = status_baru

    db.session.commit()

    return jsonify({
        "success": True,
        "status": kontrak.status
    })


@app.route("/status-tahapan/<int:id_status>/mulai", methods=["POST"])
def mulai_tahapan(id_status):
    try:
        status_tahapan = db.session.get(StatusTahapan, id_status)

        if not status_tahapan:
            return jsonify({
                "success": False,
                "message": "Status tahapan tidak ditemukan"
            }), 404

        data = request.get_json() or {}

        target_hari = data.get("target_hari")

        if target_hari is None:
            return jsonify({
                "success": False,
                "message": "Target hari harus diisi"
            }), 400

        try:
            target_hari = int(target_hari)
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "message": "Target hari harus berupa angka"
            }), 400

        if target_hari <= 0:
            return jsonify({
                "success": False,
                "message": "Target hari harus lebih dari 0"
            }), 400

        # Tanggal mulai = hari ini
        tanggal_mulai = date.today()

        # Hitung tanggal target
        tanggal_target = tanggal_mulai + timedelta(days=target_hari)

        # Simpan
        status_tahapan.tanggal_mulai = tanggal_mulai
        status_tahapan.target_hari = target_hari
        status_tahapan.tanggal_target = tanggal_target

        # Belum selesai
        status_tahapan.tanggal_selesai = None
        status_tahapan.status = False
        status_tahapan.is_marked_done = False

        db.session.commit()

        informasi = hitung_prioritas(tanggal_target)

        return jsonify({
            "success": True,
            "message": "Target tahapan berhasil disimpan",
            "tanggal_mulai": tanggal_mulai.isoformat(),
            "target_hari": target_hari,
            "tanggal_target": tanggal_target.isoformat(),
            "tanggal_selesai": None,
            "sisa_hari": informasi["sisa_hari"],
            "prioritas": informasi["prioritas"]
        })

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    try:

        status_tahapan = StatusTahapan.query.get(id_status)

        if not status_tahapan:
            return jsonify({
                "success": False,
                "message": "Status tahapan tidak ditemukan"
            }), 404

        data = request.get_json() or {}

        target_hari = data.get("target_hari")

        # =========================
        # VALIDASI TARGET
        # =========================

        if target_hari is None:
            return jsonify({
                "success": False,
                "message": "Target hari harus diisi"
            }), 400

        try:
            target_hari = int(target_hari)
        except (ValueError, TypeError):

            return jsonify({
                "success": False,
                "message": "Target hari harus berupa angka"
            }), 400

        if target_hari <= 0:

            return jsonify({
                "success": False,
                "message": "Target hari harus lebih dari 0"
            }), 400

        # =========================
        # TANGGAL MULAI
        # =========================

        tanggal_mulai = date.today()

        # =========================
        # TANGGAL TARGET
        # =========================

        tanggal_target = hitung_tanggal_target(
            tanggal_mulai,
            target_hari
        )

        # =========================
        # SIMPAN
        # =========================

        status_tahapan.tanggal_mulai = tanggal_mulai
        status_tahapan.target_hari = target_hari
        status_tahapan.tanggal_target = tanggal_target

        # Tahapan belum selesai
        status_tahapan.status = False
        status_tahapan.is_marked_done = False

        db.session.commit()

        # =========================
        # HITUNG PRIORITAS
        # =========================

        informasi = hitung_prioritas(
            tanggal_target
        )

        return jsonify({
            "success": True,
            "message": "Tahapan berhasil dimulai",

            "id_status": status_tahapan.id,

            "tanggal_mulai":
                tanggal_mulai.isoformat(),

            "target_hari":
                target_hari,

            "tanggal_target":
                tanggal_target.isoformat(),

            "sisa_hari":
                informasi["sisa_hari"],

            "prioritas":
                informasi["prioritas"]
        })

    except Exception as e:

        db.session.rollback()

        print("ERROR MULAI TAHAPAN:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/item-checklist/<int:id_checklist>/mulai", methods=["POST"])
def mulai_item_checklist(id_checklist):

    result, status_code = get_startitem_checklist(id_checklist)

    return jsonify(result), status_code

@app.route("/api/kontrak", methods=["GET"])
def api_kontrak():
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "all").strip()

    query = Kontrak.query

    # Pencarian hanya berdasarkan nama/judul kontrak
    if search:
        keyword = f"%{search}%"
        query = query.filter(
            Kontrak.judul_kontrak.ilike(keyword)
        )

    # Filter berdasarkan status
    if status and status != "all":
        query = query.filter(
            Kontrak.status == status
        )

    kontrak_list = query.all()

    contracts, avg_progress = get_contract_progress(kontrak_list)

    return jsonify({
        "data": contracts,
        "total": len(contracts),
        "avg_progress": avg_progress
    })

@app.route("/api/kontrak/<int:id>", methods=["DELETE"])
def delete_kontrak(id):
    kontrak = db.session.get(Kontrak, id)

    if not kontrak:
        return jsonify({
            "success": False,
            "message": "Kontrak tidak ditemukan"
        }), 404

    try:
        # Hapus checklist
        Checklist.query.filter_by(
            id_kontrak=id
        ).delete()

        # Hapus status tahapan
        StatusTahapan.query.filter_by(
            id_kontrak=id
        ).delete()

        # Hapus kontrak
        db.session.delete(kontrak)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Kontrak berhasil dihapus"
        })

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "success": False,
            "message": "Gagal menghapus kontrak"
        }), 500

@app.route("/api/kontrak/<int:id>", methods=["PUT"])
def update_kontrak(id):
    kontrak = db.session.get(Kontrak, id)

    if not kontrak:
        return jsonify({
            "success": False,
            "message": "Kontrak tidak ditemukan"
        }), 404

    try:
        data = request.get_json()

        kontrak.judul_kontrak = data.get(
            "judul_kontrak",
            kontrak.judul_kontrak
        )

        kontrak.lokasi_kontrak = data.get(
            "lokasi_kontrak",
            kontrak.lokasi_kontrak
        )

        kontrak.anggaran = data.get(
            "anggaran",
            kontrak.anggaran
        )

        kontrak.tahun_wpb = data.get(
            "tahun_wpb",
            kontrak.tahun_wpb
        )

        kontrak.nilai = data.get(
            "nilai",
            kontrak.nilai
        )

        if data.get("pic") is not None:

            try:
                pic_id = int(data["pic"])
            except (ValueError, TypeError):

                return jsonify({
                    "success": False,
                    "message": "ID PIC tidak valid"
                }), 400

            pic_user = User.query.filter_by(
                id=pic_id,
                role="PIC"
            ).first()

            if not pic_user:
                return jsonify({
                    "success": False,
                    "message": "PIC yang dipilih tidak valid"
                }), 400

            kontrak.pic = pic_user.id

        kontrak.status = data.get(
            "status",
            kontrak.status
        )

        if data.get("target_realisasi"):
            kontrak.target_realisasi = datetime.strptime(
                data["target_realisasi"],
                "%Y-%m-%d"
            ).date()

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Kontrak berhasil diperbarui"
        })

    except Exception as e:
        db.session.rollback()

        print(e)

        return jsonify({
            "success": False,
            "message": "Gagal memperbarui kontrak"
        }), 500

@app.route("/api/dashboard")
def dashboard_api():
    tahun = request.args.get("tahun")
    lokasi = request.args.get("lokasi")
    status = request.args.get("status")
    pic = request.args.get("pic")

    data = get_dashboard_data(
        tahun=tahun,
        lokasi=lokasi,
        status=status,
        pic=pic
    )

    return jsonify(data)

@app.get("/api/kontrak/check-name")
@login_required
def check_contract_name():

    nama = request.args.get("nama", "").strip()

    if not nama:
        return jsonify({
            "exists": False,
            "contracts": []
        })

    kontrak = Kontrak.query.filter(
        db.func.lower(Kontrak.judul_kontrak) == nama.lower()
    ).all()

    return jsonify({
        "exists": len(kontrak) > 0,
        "contracts": [
            {
                "id": k.id,
                "judul_kontrak": k.judul_kontrak,
                "tahun_wpb": k.tahun_wpb,
                "lokasi_kontrak": k.lokasi_kontrak,
                "status": k.status,
                "pic": k.pic
            }
            for k in kontrak
        ]
    })

@app.route("/manajemen-pengguna")
def index_pengguna():
    return render_template("manajemen-pengguna.html")

@app.route("/data-kontrak")
def data_kontrak():
    query = Kontrak.query

    # PIC hanya dapat melihat kontrak yang ditugaskan kepadanya.
    if current_user.role.upper() == "PIC":
        query = query.filter(Kontrak.pic == current_user.id)

    # Ambil data kontrak sesuai hak akses pengguna.
    kontrak_data = query.order_by(
        Kontrak.id.desc()
    ).all()


    notifikasi_deadline = []

    for kontrak in kontrak_data:
        checklist = kontrak.checklists or []

        for item in checklist:
            # Persyaratan yang sudah selesai tidak perlu dinotifikasikan.
            if item.is_done:
                continue

            # Gunakan kolom tanggal_target dari model Checklist.
            deadline = item.tanggal_target

            # Abaikan persyaratan yang belum memiliki target tanggal.
            if not deadline:
                continue

            hari_ini = date.today()
            sisa_hari = (deadline - hari_ini).days

            # Tampilkan deadline yang sudah terlewat atau maksimal 3 hari lagi.
            if sisa_hari <= 3:
                notifikasi_deadline.append({
                    "kontrak_id": kontrak.id,
                    "judul_kontrak": kontrak.judul_kontrak,
                    "checklist_id": item.id,
                    "deadline": deadline,
                    "sisa_hari": sisa_hari,
                    "status": (
                        "Terlambat" if sisa_hari < 0
                        else "Hari ini" if sisa_hari == 0
                        else "Mendekati deadline"
                    )
                })

            # Urutkan dari deadline yang paling mendesak.
            notifikasi_deadline.sort(
                key=lambda x: x["sisa_hari"]
            )

            jumlah_notifikasi = len(notifikasi_deadline)


    # Mengubah ID PIC menjadi nama pengguna.
    users = User.query.all()
    pic_names = {
        user.id: user.nama_lengkap
        for user in users
    }

    # Hitung progres checklist setiap kontrak.
    progress_data = {}

    for kontrak in kontrak_data:
        checklist = kontrak.checklists or []
        total = len(checklist)
        selesai = sum(
            1 for item in checklist if item.is_done
        )

        progress_data[kontrak.id] = (
            round(selesai / total * 100) if total else 0
        )

    # Hitung KPI berdasarkan kontrak yang dapat dilihat.
    total_kontrak = len(kontrak_data)

    persiapan_dokumen = sum(
        1 for kontrak in kontrak_data
        if kontrak.status == "Persiapan Dokumen"
    )

    dalam_proses = sum(
        1 for kontrak in kontrak_data
        if kontrak.status in [
            "Routing & Persetujuan",
            "Submit SmartGEP"
        ]
    )

    siap_proses_tender = sum(
        1 for kontrak in kontrak_data
        if kontrak.status == "Siap Proses Tender"
    )

    # Gabungkan seluruh nilai KPI.
    kpi = {
        "total_kontrak": total_kontrak,
        "persiapan_dokumen": persiapan_dokumen,
        "dalam_proses": dalam_proses,
        "siap_proses_tender": siap_proses_tender
    }

    return render_template(
        "data-kontrak.html",
        kontrak_data=kontrak_data,
        pic_names=pic_names,
        progress_data=progress_data,
        kpi=kpi,
        notifikasi_deadline=notifikasi_deadline,
        jumlah_notifikasi=len(notifikasi_deadline)
    )

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (ValueError, TypeError):
        return None

@login_manager.unauthorized_handler
def unauthorized():
    if request.path.startswith("/api/"):
        return jsonify({
            "error": "Sesi login tidak valid. Silakan login kembali."
        }), 401

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

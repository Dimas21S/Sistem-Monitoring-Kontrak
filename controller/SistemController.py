from models.Kontrak import Kontrak
from models.Dokumen import Dokumen
from models.Checklist import Checklist
from models.Persyaratan import Persyaratan
from models.StatusTahapan import StatusTahapan
from models.extension import db

from datetime import date, datetime
from sqlalchemy import func

def get_summary(kontrak_list):
    tahun_sekarang = date.today().year

    # A. Total seluruh kontrak
    total = len(kontrak_list)

    # B. Total kontrak yang dibuat pada tahun ini
    kontrak_tahun_ini = Kontrak.query.filter(
        db.extract("year", Kontrak.created_at) == tahun_sekarang
    ).count()

    # D. Jumlah persyaratan yang perlu ditindaklanjuti
    follow_up_count = get_follow_up(kontrak_list, limit=None)

    # E. Total anggaran seluruh kontrak
    total_value = sum(
        float(kontrak.anggaran or 0)
        for kontrak in kontrak_list
    )

    # C. Jumlah kontrak dengan progres di bawah 60%
    contracts, _ = get_contract_progress(kontrak_list)

    kontrak_progress_rendah = sum(
        1 for kontrak in contracts
        if kontrak["progress"] < 60
    )

    return {
        "total": total,
        "kontrak_tahun_ini": kontrak_tahun_ini,
        "kontrak_progress_rendah": kontrak_progress_rendah,
        "follow_up_count": follow_up_count,
        "value": total_value
    }

def get_lokasi_data(kontrak_list):
    lokasi_data = {}

    for kontrak in kontrak_list:

        lokasi = kontrak.lokasi_kontrak

        if lokasi not in lokasi_data:
            lokasi_data[lokasi] = 0

        lokasi_data[lokasi] += 1

    lokasi_labels = list(lokasi_data.keys())
    lokasi_counts = list(lokasi_data.values())

    return lokasi_labels, lokasi_counts

def get_contract_progress(kontrak_list):
    contracts = []
    total_progress = 0
    jumlah_kontrak_terhitung = 0

    for kontrak in kontrak_list:
        checklist_items = Checklist.query.filter_by(
            id_kontrak=kontrak.id
        ).all()

        total_checklist = len(checklist_items)
        selesai_checklist = sum(
            1 for item in checklist_items
            if item.is_done is True
        )

        if total_checklist > 0:
            progress = (
                selesai_checklist / total_checklist
            ) * 100

            total_progress += progress
            jumlah_kontrak_terhitung += 1
            progress_display = round(progress)
        else:
            # Belum ada checklist, progres belum dapat dihitung
            progress = None
            progress_display = 0

        pic_nama = (
            kontrak.pic_user.nama_lengkap
            if kontrak.pic_user else "-"
        )

        contracts.append({
            "id": kontrak.id,
            "judul": kontrak.judul_kontrak,
            "lokasi": kontrak.lokasi_kontrak,
            "anggaran": float(kontrak.anggaran or 0),
            "tahun_wpb": kontrak.tahun_wpb,
            "nilai": float(kontrak.nilai or 0),
            "target_realisasi": (
                kontrak.target_realisasi.isoformat()
                if kontrak.target_realisasi else None
            ),
            "pic": pic_nama,
            "status": kontrak.status,
            "progress": progress_display,
            "progress_tersedia": progress is not None
        })

    avg_progress = (
        round(total_progress / jumlah_kontrak_terhitung)
        if jumlah_kontrak_terhitung > 0 else 0
    )

    return contracts, avg_progress


def get_portfolio(kontrak_list):
    # Semua status kesiapan kontrak yang ingin ditampilkan
    status_order = [
        "Persiapan Dokumen",
        "Routing & Persetujuan",
        "Submit SmartGEP",
        "Siap Proses Tender"
    ]

    # Siapkan semua status sejak awal agar tetap tampil
    portfolio_data = {
        status: {
            "status": status,
            "progress_list": []
        }
        for status in status_order
    }

    # Hitung progres masing-masing kontrak
    for kontrak in kontrak_list:
        checklist_items = (
            Checklist.query
            .filter_by(id_kontrak=kontrak.id)
            .all()
        )

        total_item = len(checklist_items)

        selesai_item = sum(
            1 for item in checklist_items
            if item.is_done
        )

        progress = (
            round((selesai_item / total_item) * 100)
            if total_item > 0 else 0
        )

        status = kontrak.status or "Tanpa Status"

        # Jika ditemukan status baru di database,
        # tambahkan juga agar tidak hilang dari dashboard.
        if status not in portfolio_data:
            portfolio_data[status] = {
                "status": status,
                "progress_list": []
            }

        portfolio_data[status]["progress_list"].append(
            progress
        )

    portfolio = []

    for status, data in portfolio_data.items():
        progress_list = data["progress_list"]

        jumlah_kontrak = len(progress_list)

        rata_rata_progress = (
            round(sum(progress_list) / jumlah_kontrak)
            if jumlah_kontrak > 0 else 0
        )

        portfolio.append({
            "status": status,
            "jumlah_kontrak": jumlah_kontrak,
            "progress": rata_rata_progress
        })

    # Urutkan status utama sesuai tahapan kesiapan
    status_priority = {
        status: index
        for index, status in enumerate(status_order)
    }

    portfolio.sort(
        key=lambda item: (
            status_priority.get(item["status"], 999),
            item["status"]
        )
    )

    return portfolio


def get_contracts_needing_attention(kontrak_list):
    result = []

    for kontrak in kontrak_list:
        checklist_items = (
            Checklist.query
            .filter_by(id_kontrak=kontrak.id)
            .all()
        )

        total_item = len(checklist_items)

        selesai_item = sum(
            1 for item in checklist_items
            if item.is_done
        )

        progress = (
            round((selesai_item / total_item) * 100)
            if total_item > 0 else 0
        )

        # Ambil hanya kontrak dengan progres di bawah 60%
        if progress < 60:
            result.append({
                "id": kontrak.id,
                "judul_kontrak": kontrak.judul_kontrak,
                "lokasi_kontrak": kontrak.lokasi_kontrak,
                "status": kontrak.status or "Tanpa Status",
                "progress": progress
            })

    # Urutkan dari progres terendah
    result.sort(key=lambda item: item["progress"])

    return result


def get_follow_up(kontrak_list, limit=5):
    today = date.today()
    follow_up = []

    for kontrak in kontrak_list:
        status_tahapan_list = (
            StatusTahapan.query
            .filter_by(id_kontrak=kontrak.id)
            .all()
        )

        for status_tahapan in status_tahapan_list:
            if not status_tahapan.tanggal_target:
                continue

            dokumen = db.session.get(
                Dokumen,
                status_tahapan.id_document
            )

            if not dokumen:
                continue

            checklist_items = (
                db.session.query(Checklist)
                .join(
                    Persyaratan,
                    Checklist.id_item == Persyaratan.id
                )
                .filter(
                    Checklist.id_kontrak == kontrak.id,
                    Persyaratan.nomor_doc
                    == status_tahapan.id_document
                )
                .all()
            )

            for checklist in checklist_items:
                if checklist.is_done:
                    continue

                persyaratan = db.session.get(
                    Persyaratan,
                    checklist.id_item
                )

                if not persyaratan:
                    continue

                sisa_hari = (
                    status_tahapan.tanggal_target - today
                ).days

                if sisa_hari < 0:
                    status_target = "Terlambat"
                elif sisa_hari == 0:
                    status_target = "Hari ini"
                elif sisa_hari == 1:
                    status_target = "Besok"
                else:
                    status_target = f"{sisa_hari} hari lagi"

                follow_up.append({
                    "kontrak_id": kontrak.id,
                    "kontrak": kontrak.judul_kontrak,
                    "stage_id": dokumen.id,
                    "stage": dokumen.judul_dokumen,
                    "stage_number": dokumen.nomor_thp,
                    "persyaratan": persyaratan.label,
                    "tanggal_target": status_tahapan.tanggal_target,
                    "sisa_hari": sisa_hari,
                    "status_target": status_target
                })

    # Deadline terdekat ditampilkan lebih dahulu
    follow_up.sort(key=lambda x: x["tanggal_target"])

    # None berarti tampilkan seluruh data
    if limit is None:
        return follow_up

    return follow_up[:limit]


def get_oe_chart(kontrak_list):
    oe_data = []

    for kontrak in kontrak_list:
        oe_data.append({
            "judul": kontrak.judul_kontrak,
            "nilai_oe": float(kontrak.nilai or 0)
        })

    oe_data.sort(
        key=lambda x: x["nilai_oe"],
        reverse=True
    )

    return oe_data[:10]

def get_target_realisasi_chart(kontrak_list):
    target_data = {}

    for kontrak in kontrak_list:
        if not kontrak.target_realisasi:
            continue

        tahun = kontrak.target_realisasi.year

        if tahun not in target_data:
            target_data[tahun] = 0

        target_data[tahun] += 1

    return [
        {
            "tahun": tahun,
            "jumlah": jumlah
        }
        for tahun, jumlah in sorted(target_data.items())
    ]

def get_dashboard_data( tahun=None, lokasi=None, status=None, pic=None):

    query = Kontrak.query

    if tahun:
        query = query.filter(Kontrak.tahun_wpb == tahun)

    if lokasi:
        query = query.filter(Kontrak.lokasi_kontrak == lokasi)

    if status:
        query = query.filter(Kontrak.status == status)

    if pic:
        query = query.filter(Kontrak.pic == pic)

    kontrak_list = (query.order_by(Kontrak.id.desc()).all())

    summary = get_summary(kontrak_list)
    lokasi_labels, lokasi_counts = get_lokasi_data(kontrak_list)
    contracts, avg_progress = (get_contract_progress(kontrak_list))
    portfolio = get_portfolio(kontrak_list)
    follow_up = get_follow_up(kontrak_list, limit=5)
    follow_up_all = get_follow_up(kontrak_list, limit=None)
    chart_oe = get_oe_chart(kontrak_list)
    chart_target_realisasi = get_target_realisasi_chart(kontrak_list)
    contracts_needing_attention = get_contracts_needing_attention(kontrak_list)
    tahun_sekarang = date.today().year

    kontrak_tahun_berjalan = [
        kontrak
        for kontrak in kontrak_list
        if kontrak.created_at
        and kontrak.created_at.year == tahun_sekarang
    ]

    return {
        "contracts": contracts,
        "summary": summary,
        "kontrak_list": kontrak_list,
        "avg_progress": avg_progress,
        "lokasi_labels": lokasi_labels,
        "lokasi_counts": lokasi_counts,
        "portfolio": portfolio,
        "follow_up": follow_up,
        "follow_up_all": follow_up_all,
        "target_realisasi": chart_target_realisasi,
        "chart_oe": chart_oe,
        "contracts_needing_attention": contracts_needing_attention,
        "kontrak_tahun_berjalan": kontrak_tahun_berjalan
    }


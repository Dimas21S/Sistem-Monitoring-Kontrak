# Sistem Monitoring Kontrak — PHR Zona 1 Jambi

Sistem Monitoring Kontrak merupakan aplikasi berbasis web yang dikembangkan untuk membantu proses pemantauan dan pengelolaan data kontrak, progres pemenuhan persyaratan, serta tindak lanjut pekerjaan kontrak pada PT Pertamina Hulu Rokan (PHR) Zona 1 Jambi.

Aplikasi ini menyediakan informasi progres kontrak secara terpusat sehingga pengguna dapat memantau kesiapan dokumen, status tahapan pekerjaan, batas waktu persyaratan, dan ringkasan data kontrak dengan lebih terstruktur.

> **Catatan:** Proyek ini dikembangkan sebagai bagian dari kegiatan magang. Data yang digunakan untuk demonstrasi atau pengujian sebaiknya berupa data dummy yang tidak memuat informasi internal perusahaan.

## 📌 Daftar Isi

- [Tentang Proyek](#-tentang-proyek)
- [Fitur Utama](#-fitur-utama)
- [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
- [Arsitektur Aplikasi](#-arsitektur-aplikasi)
- [Struktur Direktori](#-struktur-direktori)
- [Persyaratan Sistem](#-persyaratan-sistem)
- [Instalasi dan Konfigurasi](#-instalasi-dan-konfigurasi)
- [Menjalankan Aplikasi](#-menjalankan-aplikasi)
- [Hak Akses Pengguna](#-hak-akses-pengguna)
- [Pengembangan Selanjutnya](#-pengembangan-selanjutnya)
- [Kontributor](#-kontributor)
- [Lisensi](#-lisensi)

## 🎯 Tentang Proyek

Pengelolaan kontrak membutuhkan pemantauan terhadap berbagai informasi, mulai dari data kontrak, tahapan proses, kelengkapan dokumen, hingga target penyelesaian. Sistem ini dikembangkan untuk membantu menyajikan informasi tersebut dalam satu aplikasi berbasis web.

Tujuan pengembangan:

- Memusatkan pengelolaan data kontrak.
- Mempermudah pemantauan progres persyaratan kontrak.
- Membantu mengidentifikasi kontrak yang memerlukan perhatian.
- Menyediakan informasi batas waktu dan tindak lanjut.
- Menampilkan ringkasan data melalui dashboard interaktif.
- Membantu pengelolaan pengguna berdasarkan peran dan hak akses.

## ✨ Fitur Utama

### 1. Dashboard Monitoring

Menyajikan ringkasan informasi kontrak melalui indikator dan visualisasi, meliputi:

- Total kontrak.
- Kontrak yang dibuat pada tahun berjalan.
- Kontrak dengan progres di bawah 60%.
- Informasi tindak lanjut.
- Total anggaran kontrak.
- Visualisasi progres portofolio kontrak.

### 2. Manajemen Data Kontrak

Mendukung pengelolaan data kontrak, termasuk:

- Menambahkan data kontrak.
- Menampilkan daftar kontrak.
- Memperbarui informasi kontrak.
- Menghapus data kontrak.
- Mencari kontrak berdasarkan kata kunci.
- Memantau status dan progres kontrak.
- Mengelola informasi PIC (*Person in Charge*).

### 3. Checklist Persyaratan Kontrak

Menyediakan checklist untuk membantu pemantauan pemenuhan persyaratan pada setiap kontrak.

Fitur ini mencakup:

- Menampilkan daftar persyaratan berdasarkan tahapan.
- Menandai persyaratan yang telah selesai.
- Memantau jumlah persyaratan yang selesai dan belum selesai.
- Menghitung persentase progres berdasarkan checklist.
- Memantau kelengkapan dokumen kontrak.

### 4. Batas Waktu Persyaratan

Membantu pengguna memantau target penyelesaian persyaratan melalui informasi tenggat waktu dan kebutuhan tindak lanjut.

### 5. Monitoring Tahapan Kontrak

Mendukung pemantauan tahapan proses kontrak, antara lain:

1. Persiapan Dokumen.
2. Routing & Persetujuan.
3. Submit SmartGEP.
4. Siap Proses Tender.

### 6. Manajemen Pengguna

Menyediakan pengelolaan akun pengguna sesuai dengan peran yang ditetapkan, termasuk penambahan, pembaruan, dan penghapusan pengguna oleh administrator.

### 7. Autentikasi dan Hak Akses

Menggunakan mekanisme login untuk membatasi akses aplikasi berdasarkan peran pengguna.

### 8. Visualisasi Data

Menggunakan grafik dan indikator dashboard untuk membantu pengguna memahami kondisi portofolio serta progres kontrak secara ringkas.

## 🛠 Teknologi yang Digunakan

| Teknologi | Kegunaan |
|---|---|
| Python | Bahasa pemrograman backend |
| Flask | Framework aplikasi web |
| MySQL | Basis data relasional |
| Flask-SQLAlchemy / SQLAlchemy | ORM dan pengelolaan basis data |
| PyMySQL | Koneksi Python ke MySQL |
| Flask-Login | Autentikasi dan sesi pengguna |
| Jinja2 | Template halaman web |
| HTML5 | Struktur halaman |
| Tailwind CSS | Styling antarmuka |
| JavaScript | Interaksi pada sisi frontend |
| Chart.js | Visualisasi data dashboard |
| Lucide Icons | Ikon antarmuka |
| Git & GitHub | Version control dan penyimpanan kode |

## 🏗 Arsitektur Aplikasi

Aplikasi menggunakan Flask sebagai backend dengan pemisahan tanggung jawab ke dalam modul controller, model, dan template.

Gambaran alur aplikasi:

```text
Pengguna
   |
   v
Antarmuka Web
(HTML, Tailwind CSS, JavaScript)
   |
   v
Flask Application
   |
   v
Controller
   |
   +--------------------+
   |                    |
   v                    v
Model / ORM         Logika Bisnis
   |
   v
Database MySQL
```

Pembagian komponen:

- **Frontend:** Menampilkan dashboard, formulir, tabel kontrak, checklist, dan informasi pengguna.
- **Controller:** Menangani request, validasi input, autentikasi, dan proses bisnis.
- **Model:** Merepresentasikan data dan relasi antartabel.
- **Database:** Menyimpan data kontrak, pengguna, checklist, dokumen, dan tahapan kontrak.

## 📂 Struktur Direktori

Berikut gambaran struktur direktori yang dapat disesuaikan dengan struktur proyek aktual.

```text
MonitoringKontrak/
├── app.py
├── controller/
│   ├── AuthController.py
│   ├── AdminController.py
│   ├── UserController.py
│   ├── SistemController.py
│   ├── KontrakController.py
│   └── ChecklistController.py
├── models/
│   └── ...
├── templates/
│   ├── dashboard.html
│   ├── data_kontrak.html
│   └── ...
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

**Catatan:** Nama dan lokasi folder di atas merupakan gambaran struktur. Sesuaikan dengan direktori yang benar-benar tersedia pada repositori proyek.

## 💻 Persyaratan Sistem

Sebelum menjalankan aplikasi, pastikan perangkat telah memiliki:

- Python 3.10 atau versi yang kompatibel dengan dependensi proyek.
- MySQL Server.
- pip untuk instalasi paket Python.
- Git (opsional, untuk mengkloning repositori).
- Browser modern seperti Google Chrome atau Microsoft Edge.

## ⚙️ Instalasi dan Konfigurasi

### 1. Clone repositori

Ganti URL berikut dengan alamat repositori GitHub milikmu.

```bash
git clone https://github.com/USERNAME/MonitoringKontrak.git
cd MonitoringKontrak
```

### 2. Buat virtual environment

Windows:

```bash
python -m venv venv
```

Aktifkan virtual environment:

```bash
venv\Scripts\activate
```

### 3. Instal dependensi

Jika file `requirements.txt` sudah tersedia:

```bash
pip install -r requirements.txt
```

Pastikan seluruh dependensi yang diperlukan aplikasi telah tercantum dalam file tersebut.

### 4. Siapkan database MySQL

Buat database dengan nama:

```sql
CREATE DATABASE monitoring_kontrak;
```

Sesuaikan nama database jika konfigurasi proyek menggunakan nama yang berbeda. Impor skema atau jalankan proses inisialisasi database sesuai implementasi aplikasi.

### 5. Konfigurasi environment

Buat file `.env` pada direktori utama proyek.

Contoh konfigurasi:

```env
SECRET_KEY=ganti_dengan_secret_key_yang_aman

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=monitoring_kontrak
```

Sesuaikan variabel tersebut dengan konfigurasi yang dibaca oleh `app.py` dan modul koneksi database. Jangan mengunggah kredensial asli ke repositori publik.

## ▶️ Menjalankan Aplikasi

Setelah dependensi dan database siap, jalankan:

```bash
python app.py
```

Jika aplikasi menggunakan konfigurasi Flask standar pada port 5000, akses melalui browser:

```text
http://127.0.0.1:5000
```

Pastikan server MySQL berjalan dan konfigurasi database sudah benar sebelum membuka aplikasi.

## 👥 Hak Akses Pengguna

Aplikasi dirancang dengan tiga peran pengguna.

| Peran | Hak Akses |
|---|---|
| Admin | Mengelola pengguna dan mengakses fitur administrasi sesuai implementasi |
| PIC | Mengelola serta memantau kontrak yang menjadi tanggung jawabnya |
| User | Melihat dashboard dan informasi kontrak sesuai hak akses |

Pembatasan akses dilakukan pada sisi backend untuk membantu memastikan pengguna hanya dapat menjalankan tindakan yang diizinkan bagi perannya.

## 🔒 Keamanan

Beberapa hal yang perlu diperhatikan ketika menjalankan atau mendistribusikan aplikasi:

- Simpan kredensial database dan `SECRET_KEY` di environment variable.
- Jangan mengunggah file `.env` ke GitHub.
- Gunakan password yang telah di-hash.
- Terapkan pemeriksaan autentikasi dan otorisasi pada endpoint backend.
- Gunakan data dummy untuk demonstrasi publik.
- Hindari memublikasikan informasi kontrak, dokumen, atau data internal perusahaan tanpa izin.

## 🚀 Pengembangan Selanjutnya

Beberapa pengembangan yang dapat dipertimbangkan:

- Notifikasi otomatis untuk persyaratan yang mendekati tenggat waktu.
- Penyempurnaan filter dashboard secara menyeluruh.
- Ekspor laporan monitoring ke Excel atau PDF.
- Penyempurnaan pencatatan aktivitas pengguna.
- Penguatan validasi input dan pengujian keamanan.
- Deployment pada server yang dapat diakses oleh pengguna berwenang.

## 👨‍💻 Kontributor

Dikembangkan sebagai proyek sistem informasi berbasis web dalam kegiatan magang di PT Pertamina Hulu Rokan Zona 1 Jambi.

**Fokus kontribusi:** Backend Development

Tanggung jawab pengembangan backend meliputi:

- Pengembangan endpoint dan logika bisnis menggunakan Flask.
- Pengelolaan koneksi dan operasi basis data.
- Implementasi proses CRUD data kontrak.
- Pengembangan logika checklist dan perhitungan progres.
- Implementasi autentikasi serta hak akses pengguna.
- Penyediaan data untuk kebutuhan dashboard monitoring.

## 📄 Lisensi

Lisensi proyek belum ditentukan. Jika repositori akan dipublikasikan, tentukan lisensi yang sesuai dengan kepemilikan kode dan izin distribusi proyek.

---

**Sistem Monitoring Kontrak — PHR Zona 1 Jambi**

*Web-based Contract Monitoring and Management System*

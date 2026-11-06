# ASM TRANSPORT KEBUMEN V2 (PO ALULA SADIDA MARYAM)
> **Corporate Transportation Website & Online Booking Management System**

Selamat datang di repositori resmi **ASM Transport Kebumen V2**. Proyek ini adalah platform web korporat modern untuk perusahaan otobus pariwisata **ASM Transport (PO Alula Sadida Maryam)** yang berbasis di Kabupaten Kebumen, Jawa Tengah.

Situs web ini dirancang dengan gaya **Premium Corporate & Modern Minimalist** menggunakan palet warna identitas perusahaan:
- **Navy Blue**: `#101D38`
- **Pure White**: `#FFFFFF`
- **Accent Orange**: `#F28C28`
- **Light Gray**: `#F4F6F9`

---

## 🚌 Fitur Utama Website

### 1. Halaman Publik (Customer-Facing)
1. **Beranda (Home)**:
   - Topbar informasi layanan & hotline 24 jam.
   - Hero section dengan slogan resmi: *"Perjalanan Nyaman, Kenangan Berkesan"*.
   - Kartu pencarian & cek ketersediaan bus interaktif.
   - Pengenalan profil PO Alula Sadida Maryam.
   - Katalog armada unggulan dengan kartu spesifikasi dinamis.
   - Layanan transportasi bus terlengkap (Wisata, Study Tour, Ziarah Wali, Kunjungan Kerja, Antar Jemput Bandara).
   - 4 Pilar keunggulan ASM Transport (Keselamatan, Kebersihan Armada, Kru Sopir Ramah, Harga Transparan).
   - Pratinjau galeri dokumentasi perjalanan.
   - Ulasan testimoni pelanggan dengan rating bintang.
   - Floating WhatsApp button interaktif.
   - Footer informatif dengan legalitas demo, kontak kantor Kebumen, dan tautan sosial media.
2. **Profil Perusahaan (`/profil`)**:
   - Sejarah & filosofi PO Alula Sadida Maryam.
   - Visi & Misi perusahaan.
   - Nilai-nilai utama (*Safety First, Comfort & Cleanliness, Punctuality, Fair Pricing*).
   - Standar legalitas, uji KIR berkala, dan kesiapan darurat.
3. **Katalog Armada (`/armada`)**:
   - Filter armada berdasarkan kategori: *Big Bus*, *Medium Bus*, *Executive Bus*, *HiAce / Minibus*.
   - Kartu bus dengan indikator kapasitas kursi, transmisi, sasis mesin, daftar fasilitas, dan status kesiapan.
4. **Detail Armada (`/armada/<slug>`)**:
   - Foto resolusi tinggi dan spesifikasi teknis lengkap.
   - Rincian fasilitas kenyamanan (AC Denso, Karaoke Android, Reclining Seat, USB Charger, Toilet, dll.).
   - Tombol langsung *"Pesan Bus Ini"* yang otomatis memilihkan armada pada formulir reservasi.
5. **Layanan Transportasi (`/layanan`)**:
   - Rincian lengkap 6 paket layanan transportasi pariwisata dan kedinasan.
   - 4 Langkah alur mudah pemesanan bus pariwisata.
6. **Galeri Dokumentasi (`/galeri`)**:
   - Filter kategori foto: *Armada*, *Perjalanan*, *Fasilitas*, *Kru*.
   - Lightbox modal interaktif untuk melihat gambar ukuran penuh beserta keterangannya.
7. **Kontak & Lokasi (`/kontak`)**:
   - Alamat kantor operasional & pool bus di Kebumen.
   - Nomor WhatsApp 24 jam, telepon kantor, email resmi.
   - Formulir kirim pesan cepat dengan validasi.
   - Peta interaktif Google Maps Kebumen.
8. **Formulir Permintaan Pemesanan (`/pemesanan`)**:
   - Validasi nama, nomor WhatsApp, email, pilihan bus, tanggal berangkat dan pulang.
   - Perhitungan otomatis durasi hari sewa melalui JavaScript ES6.
   - Input titik penjemputan, kota tujuan, jumlah rombongan, dan permintaan khusus.
9. **Konfirmasi Pemesanan & Integrasi WhatsApp (`/pemesanan/sukses/<kode>`)**:
   - Penerbitan Kode Booking unik (format: `ASM-YYYYMMDD-XXXX`).
   - Tombol konfirmasi satu-klik ke WhatsApp Admin dengan pesan otomatis terformat rapi.
   - Tombol cetak / simpan rincian reservasi.

---

### 2. Panel Dashboard Administrator (`/admin`)
- **Autentikasi Aman**: Dilindungi sistem login Flask-Login, Session Management, dan proteksi CSRF Flask-WTF.
- **Ringkasan KPI Dashboard**:
  - Total Pemesanan & Penghitung Status (*Menunggu Konfirmasi*, *Dikonfirmasi*, *Selesai*, *Dibatalkan*).
  - Total Armada Bus & Status Aktif.
  - Total Layanan, Galeri, dan Testimoni.
  - Tabel interaktif pemesanan terbaru dengan akses cepat.
- **CRUD Armada Bus (`/admin/fleets`)**:
  - Tambah, Edit, Hapus unit bus.
  - Pengunggahan foto armada dengan validasi format (JPG, PNG, WEBP) & pratinjau live.
  - Pengaturan status kesiapan (Tersedia, Beroperasi, Perawatan) dan penanda Unggulan di Beranda.
- **Manajemen Pemesanan (`/admin/bookings`)**:
  - Filter pemesanan berdasarkan status.
  - Lihat detail lengkap pemesan, tanggal, rute, catatan khusus.
  - Pembaruan status pemesanan (*Menunggu Konfirmasi*, *Dikonfirmasi*, *Selesai*, *Dibatalkan*).
  - Kolom catatan internal admin (riwayat DP, nomor bus, nama supir yang ditugaskan).
  - Tombol langsung untuk menghubungi WhatsApp pemesan.
- **CRUD Layanan (`/admin/services`)**:
  - Tambah, Edit, Hapus layanan dengan pemilihan ikon Font Awesome.
- **CRUD Galeri Dokumentasi (`/admin/galleries`)**:
  - Pengunggahan foto dengan kategori dan keterangan.
- **CRUD Testimoni Pelanggan (`/admin/testimonials`)**:
  - Kelola ulasan pelanggan, rating bintang (1-5), instansi, dan opsi tampil di beranda.
- **Pengaturan Website (`/admin/settings`)**:
  - Perbarui nomor WhatsApp pemesanan, telepon, email, alamat kantor di Kebumen, jam operasional, slogan, dan tautan sosial media tanpa mengubah kode program.
- **Profil & Ganti Kata Sandi (`/admin/profile`)**:
  - Form penggantian kata sandi dengan verifikasi kata sandi lama dan password hashing terenkripsi aman.

---

## 🛠️ Arsitektur & Teknologi

- **Backend**: Python 3.11, Flask Framework, Application Factory Pattern (`create_app`), Flask Blueprints (`main`, `auth`, `admin`).
- **Database & ORM**: SQLite (`instance/asm_transport.db`), Flask-SQLAlchemy, Flask-Migrate (Alembic).
- **Keamanan & Autentikasi**: Flask-Login, Werkzeug Security (`generate_password_hash`, `check_password_hash`), Flask-WTF CSRF Protection.
- **Frontend**: HTML5, Modern CSS3, JavaScript ES6, Bootstrap 5.3, Font Awesome 6 Icons, Google Fonts (Plus Jakarta Sans).
- **Pengolahan Gambar**: Pillow (PIL), Secure Filename Handling dengan UUID.

---

## 📁 Struktur Folder Proyek

```
ASM 2.0/
├── app/
│   ├── __init__.py            # Application Factory (create_app)
│   ├── extensions.py          # Inisialisasi db, migrate, login_manager, csrf
│   ├── models.py              # Skema database SQLite (User, Fleet, Booking, dll.)
│   ├── forms.py               # Formulir Flask-WTF dengan validasi
│   ├── utils.py               # Helper fungsi (upload, format tanggal ID, slugify)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py            # Rute halaman publik (Beranda, Profil, Armada, Booking)
│   │   ├── auth.py            # Rute otentikasi admin (Login, Logout)
│   │   └── admin.py           # Rute CRUD dashboard admin
│   ├── templates/
│   │   ├── base.html          # Layout utama halaman publik
│   │   ├── pages/             # 8 Halaman publik
│   │   │   ├── index.html
│   │   │   ├── about.html
│   │   │   ├── fleets.html
│   │   │   ├── fleet_detail.html
│   │   │   ├── services.html
│   │   │   ├── gallery.html
│   │   │   ├── contact.html
│   │   │   ├── booking.html
│   │   │   └── booking_success.html
│   │   ├── admin/             # Seluruh tampilan dashboard admin
│   │   │   ├── base_admin.html
│   │   │   ├── login.html
│   │   │   ├── dashboard.html
│   │   │   ├── fleets/        # CRUD Armada
│   │   │   ├── bookings/      # Manajemen Pemesanan
│   │   │   ├── services/      # CRUD Layanan
│   │   │   ├── galleries/     # CRUD Galeri
│   │   │   ├── testimonials/  # CRUD Testimoni
│   │   │   ├── settings.html  # Pengaturan Web
│   │   │   └── profile.html   # Ganti Password
│   │   └── errors/
│   │       ├── 404.html
│   │       └── 500.html
│   └── static/
│       ├── css/
│       │   ├── style.css      # CSS publik modern corporate
│       │   └── admin.css      # CSS admin dashboard
│       ├── js/
│       │   ├── main.js        # JavaScript publik interaktif
│       │   └── admin.js       # JavaScript admin
│       ├── images/            # Logo & foto asli bus ASM Transport
│       └── uploads/           # Folder penyimpanan upload dinamis
├── migrations/                # Database migrations (Flask-Migrate/Alembic)
├── config.py                  # Konfigurasi aplikasi
├── seed.py                    # Script pengisian data awal demonstrasi
├── run.py                     # Entry point server Flask
├── test_suite.py              # Suite pengujian unit & integrasi otomatis
├── requirements.txt           # Daftar dependensi Python
├── .env                       # Variabel lingkungan aktif
├── .env.example               # Contoh konfigurasi environment
├── .gitignore
└── README.md
```

---

## 🚀 Panduan Menjalankan Aplikasi Secara Lokal

### 1. Prasyarat Sistem
- Python 3.9 atau yang lebih baru (Disarankan Python 3.11).
- Terminal PowerShell / Command Prompt / VS Code Terminal.

### 2. Membuat dan Mengaktifkan Virtual Environment
Buka folder ruang kerja di terminal VS Code:

```powershell
# Membuat virtual environment
python -m venv venv

# Mengaktifkan virtual environment di Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Atau jika menggunakan Command Prompt (cmd)
venv\Scripts\activate.bat
```

### 3. Menginstal Seluruh Dependensi
```powershell
pip install -r requirements.txt
```

### 4. Menjalankan Aplikasi
Aplikasi dilengkapi dengan fitur **Auto-Initialize Database**. Saat pertama kali dijalankan, aplikasi akan otomatis membuat basis data SQLite `instance/asm_transport.db` dan mengisinya dengan data demonstrasi lengkap (Armada, Layanan, Galeri, Testimoni, Pengaturan, dan Akun Admin).

Jalankan perintah berikut:
```powershell
python run.py
```

Buka peramban (browser) Anda dan akses:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🔐 Akun Administrator Awal

Untuk mengakses Dashboard Administrator:
1. Buka tautan: **[http://127.0.0.1:5000/admin/login](http://127.0.0.1:5000/admin/login)**
2. Masukkan kredensial awal:
   - **Username**: `admin` (atau email `admin@asmtransport.com`)
   - **Password**: `adminasm2026`

### Cara Mengganti Kata Sandi Administrator:
1. Masuk ke Dashboard Admin.
2. Di sidebar kiri, klik menu **Profil & Keamanan** (atau klik nama admin di pojok kanan atas lalu pilih **Ganti Password**).
3. Masukkan kata sandi saat ini (`adminasm2026`).
4. Masukkan kata sandi baru (minimal 6 karakter).
5. Konfirmasi kata sandi baru dan klik **Perbarui Kata Sandi**.
6. Kata sandi akan langsung terenkripsi menggunakan algoritma hashing modern Werkzeug.

---

## 🧪 Menjalankan Pengujian Otomatis (Automated Tests)

Aplikasi memiliki pengujian komprehensif yang mencakup rute publik, validasi formulir pemesanan, proteksi autentikasi, serta seluruh fungsi CRUD admin.

Jalankan pengujian menggunakan:
```powershell
python test_suite.py
```
Hasil pengujian: **14 tests passed (OK)**.

---

## 💬 Konfigurasi WhatsApp

Nomor WhatsApp terkonfigurasi secara terpusat dan dapat disesuaikan kapan saja:
1. Masuk ke Dashboard Admin &rarr; **Pengaturan Website**.
2. Ubah kolom **Nomor WhatsApp** (gunakan format internasional tanpa spasi, contoh: `62882005363151`).
3. Klik **Simpan Seluruh Pengaturan**. Seluruh tombol WhatsApp pada halaman publik dan floating chat akan otomatis tersinkronisasi.

---

## 📄 Catatan Hak Cipta & Demonstrasi
Data foto armada bus dan logo PO Alula Sadida Maryam dilestarikan dari aset asli perusahaan. Seluruh data historis atau narasi yang bersifat contoh diberi tanda demonstrasi dan dapat diperbarui sewaktu-waktu melalui Dashboard Admin resmi.


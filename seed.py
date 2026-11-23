import os
from datetime import date, datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import User, Fleet, Booking, Service, Gallery, Testimonial, SiteSetting
from app.utils import slugify, generate_booking_code

def _run_seed_process():
    # Create database tables if they do not exist
    db.create_all()

    try:
        print("[1/7] Inisialisasi Akun Administrator...")
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@asmtransport.com',
                full_name='Administrator ASM Transport',
                role='admin',
                is_active=True
            )
            admin.set_password('adminasm2026')
            db.session.add(admin)
            print("  -> Akun admin dibuat: Username 'admin', Password 'adminasm2026'")
        else:
            print("  -> Akun admin sudah ada.")

        print("[2/7] Inisialisasi Pengaturan Website (Site Settings)...")
        settings_defaults = [
            ('company_name', 'ASM Transport Kebumen', 'Nama Perusahaan', 'general'),
            ('tagline', 'Perjalanan Nyaman, Kenangan Berkesan', 'Slogan Perusahaan', 'general'),
            ('whatsapp_number', '62882005363151', 'Nomor WhatsApp Pemesanan', 'contact'),
            ('office_phone', '(0287) 381-000', 'Nomor Telepon Kantor', 'contact'),
            ('office_email', 'info@asmtransport.id', 'Email Resmi Perusahaan', 'contact'),
            ('address', 'Jl. Raya Kebumen - Purworejo KM. 5, Kebumen, Jawa Tengah 54311 (Data Sampel Demonstrasi)', 'Alamat Kantor', 'contact'),
            ('operating_hours', 'Senin - Minggu: 24 Jam Pelayanan Reservasi & Informasi Bus', 'Jam Operasional', 'contact'),
            ('about_summary', 'ASM Transport Kebumen (PO Alula Sadida Maryam) adalah penyedia layanan transportasi bus pariwisata profesional terpercaya yang melayani perjalanan wisata, study tour, ziarah, dan perjalanan dinas se-Indonesia dengan mengutamakan keselamatan dan kepuasan pelanggan.', 'Ringkasan Tentang Kami', 'general'),
            ('instagram_url', 'https://instagram.com/asmtransport_kebumen', 'Link Instagram', 'social'),
            ('facebook_url', 'https://facebook.com/asmtransportkebumen', 'Link Facebook', 'social'),
            ('tiktok_url', 'https://tiktok.com/@asmtransport', 'Link TikTok', 'social'),
            ('youtube_url', 'https://youtube.com/@asmtransportkebumen', 'Link YouTube', 'social')
        ]
        for key, value, label, group in settings_defaults:
            if not SiteSetting.query.filter_by(key=key).first():
                SiteSetting.set(key, value, label, group)
        print("  -> Pengaturan website berhasil disimpan.")

        print("[3/7] Inisialisasi Katalog Armada Bus ASM Transport...")
        fleets_data = [
            {
                'name': 'Jetbus 5 SHD Dream Coach - Alula 01 (Executive)',
                'category': 'Executive Bus',
                'seat_capacity': 30,
                'seat_configuration': '2-1',
                'facilities': 'AC Dingin Denso, Android Karaoke & Wireless Mic, Legrest Reclining Seat, USB Fast Charging, Toilet Bersih, Dispenser Air, Bantal & Selimut, Bagasi Luas Tembus, APAR & Palu Darurat',
                'description': '[DEMO DATA] Unit flagship kelas eksekutif ASM Transport dengan kenyamanan paripurna. Sangat cocok untuk perjalanan wisata VIP, kunjungan kedinasan instansi, dan rombongan keluarga besar yang mengutamakan privasi dan kelegaan tempat duduk.',
                'transmission': 'Manual 6-Speed',
                'chassis_engine': 'Mercedes-Benz OH 1626 Air Suspension',
                'price_estimate': 'Mulai Rp 3.500.000 / Hari (Nego Hubungi Admin)',
                'main_image': 'images/bus-executive.jpg',
                'status': 'Tersedia',
                'is_featured': True
            },
            {
                'name': 'Legacy SR3 HD Prime - Alula 02 (Big Bus Pariwisata)',
                'category': 'Big Bus',
                'seat_capacity': 50,
                'seat_configuration': '2-2',
                'facilities': 'AC Central Ducting, 2 Unit TV LED 32 & 24 Inch, Audio Karaoke Full Bass, Kursi Reclining Ergonomis, Port Charger Tiap Baris, Bagasi Luas, Lampu Baca, Bantal & Selimut',
                'description': '[DEMO DATA] Big Bus berkapasitas 50 kursi yang menjadi pilihan favorit untuk rombongan Study Tour sekolah, ziarah wali, family gathering perusahaan, atau rombongan hajatan. Kabin senyap dan ruang kaki lega menjamin kenyamanan maksimal.',
                'transmission': 'Manual 6-Speed',
                'chassis_engine': 'Hino RK8 R260 Euro 4',
                'price_estimate': 'Mulai Rp 3.200.000 / Hari (Nego Hubungi Admin)',
                'main_image': 'images/bus-big.jpg',
                'status': 'Tersedia',
                'is_featured': True
            },
            {
                'name': 'Jetbus 3+ HDD Voyager - Salman Alula 03',
                'category': 'Big Bus',
                'seat_capacity': 48,
                'seat_configuration': '2-2',
                'facilities': 'Full AC Dingin Merata, Audio Subwoofer & Wireless Mic Karaoke, TV Monitor HD, Reclining Seat, USB Charging Port, Tirai Privasi, Bagasi Bawah & Kompartemen Atas',
                'description': '[DEMO DATA] Unit Big Bus tangguh dengan tampilan Voyager yang gagah dan elegan. Siap menemani perjalanan antar-provinsi ke Yogyakarta, Jawa Timur, Bali, Bandung, hingga Jakarta dengan kestabilan berkendara yang teruji.',
                'transmission': 'Manual 6-Speed',
                'chassis_engine': 'Hino RK8 R260 Leaf Spring',
                'price_estimate': 'Mulai Rp 3.000.000 / Hari (Nego Hubungi Admin)',
                'main_image': 'images/Salman Voyager.jpeg',
                'status': 'Tersedia',
                'is_featured': True
            },
            {
                'name': 'Medium Bus Jetbus MD - Alula Junior 05',
                'category': 'Medium Bus',
                'seat_capacity': 33,
                'seat_configuration': '2-2',
                'facilities': 'AC Dingin Terawat, TV LED & Karaoke Musik, Reclining Seat Empuk, USB Charging, Bagasi Luas, Desain Lincah untuk Rute Pegunungan & Desa Wisata',
                'description': '[DEMO DATA] Solusi transportasi tepat untuk rombongan dengan destinasi jalan menanjak atau berkelok seperti Dataran Tinggi Dieng Wonosobo, Telaga Sarangan, atau Guci Tegal. Lincah, bertenaga, dan tetap sangat nyaman.',
                'transmission': 'Manual 5-Speed',
                'chassis_engine': 'Mitsubishi Canter FE 84 BC 136 PS',
                'price_estimate': 'Mulai Rp 2.000.000 / Hari (Nego Hubungi Admin)',
                'main_image': 'images/bus-medium.jpg',
                'status': 'Tersedia',
                'is_featured': True
            },
            {
                'name': 'Toyota HiAce Commuter VIP - Alula Shuttle',
                'category': 'HiAce / Minibus',
                'seat_capacity': 15,
                'seat_configuration': '1-2',
                'facilities': 'AC Dual Blower Nyaman, Audio Bluetooth, Kursi Reclining Mewah, USB Fast Charging Tiap Baris, Suspensi Lembut, Privasi Tinggi',
                'description': '[DEMO DATA] Kendaraan minibus berkelas untuk rombongan keluarga inti, penjemputan tamu VIP bandara YIA Kulon Progo / Solo / Semarang, atau rombongan dinas instansi yang membutuhkan mobilitas cepat dan gesit.',
                'transmission': 'Manual 5-Speed',
                'chassis_engine': 'Toyota 2KD-FTV D-4D 2.5L Turbo',
                'price_estimate': 'Mulai Rp 1.200.000 / Hari (Nego Hubungi Admin)',
                'main_image': 'images/bus-luxury.jpg',
                'status': 'Tersedia',
                'is_featured': False
            }
        ]

        for item in fleets_data:
            slug = slugify(item['name'])
            existing = Fleet.query.filter_by(slug=slug).first()
            if not existing:
                fleet = Fleet(
                    name=item['name'],
                    slug=slug,
                    category=item['category'],
                    seat_capacity=item['seat_capacity'],
                    seat_configuration=item['seat_configuration'],
                    facilities=item['facilities'],
                    description=item['description'],
                    transmission=item['transmission'],
                    chassis_engine=item['chassis_engine'],
                    price_estimate=item['price_estimate'],
                    main_image=item['main_image'],
                    status=item['status'],
                    is_featured=item['is_featured'],
                    is_active=True
                )
                db.session.add(fleet)
        print("  -> Katalog armada berhasil diinisialisasi.")

        print("[4/7] Inisialisasi Layanan Transportasi...")
        services_data = [
            {
                'title': 'Pariwisata & Study Tour',
                'short_description': 'Perjalanan wisata sekolah, kampus, dan rombongan umum dengan rute wisata populer Jawa, Bali, hingga Lombok.',
                'full_description': '[DEMO DATA] Kami menyediakan paket penyewaan bus pariwisata lengkap untuk kegiatan Study Tour, KKL mahasiswa, dan wisata komunitas. Dilengkapi kru yang ramah, sopir berpengalaman, serta unit bus ber-AC dingin dengan fasilitas karaoke untuk menghidupkan suasana perjalanan.',
                'icon': 'fa-solid fa-graduation-cap',
                'image': 'images/Yogya.png',
                'display_order': 1
            },
            {
                'title': 'Ziarah Wali & Wisata Religi',
                'short_description': 'Perjalanan ibadah ziarah Wali Songo, ziarah ulama Jawa Tengah, Jawa Timur, dan Madura dengan kenyamanan optimal.',
                'full_description': '[DEMO DATA] Layanan khusus ziarah religi dengan jadwal yang dapat disesuaikan secara fleksibel. Pengemudi kami sangat memahami rute tempat ziarah, kantong parkir bus, dan rest area yang nyaman untuk rombongan.',
                'icon': 'fa-solid fa-mosque',
                'image': 'images/Wonosobo.png',
                'display_order': 2
            },
            {
                'title': 'Kunjungan Kerja & Instansi',
                'short_description': 'Transportasi resmi untuk keperluan kedinasan, rapat kerja, kunjungan industri, dan gathering perusahaan.',
                'full_description': '[DEMO DATA] Solusi profesional bagi instansi pemerintah dan perusahaan swasta di wilayah Kebumen dan sekitarnya yang memerlukan transportasi terpercaya dengan standar keselamatan dan ketepatan waktu tinggi.',
                'icon': 'fa-solid fa-briefcase',
                'image': 'images/Bandung.png',
                'display_order': 3
            },
            {
                'title': 'Antar Jemput Bandara & Stasiun',
                'short_description': 'Layanan antar jemput tepat waktu menuju Bandara YIA Kulon Progo, Solo, Semarang, maupun stasiun kereta api.',
                'full_description': '[DEMO DATA] Memastikan rombongan Anda tiba tepat waktu di bandara atau stasiun dengan armada bersih dan bagasi yang luas untuk barang bawaan penumpang.',
                'icon': 'fa-solid fa-plane-departure',
                'image': 'images/bus-luxury.jpg',
                'display_order': 4
            },
            {
                'title': 'Acara Keluarga & Hajatan',
                'short_description': 'Transportasi nyaman untuk rombongan resepsi pernikahan antar-kota, lamaran, dan silaturahmi keluarga besar.',
                'full_description': '[DEMO DATA] Momen bahagia keluarga semakin berkesan saat seluruh rombongan dapat berangkat bersama dalam satu bus yang sejuk, nyaman, dan bersih.',
                'icon': 'fa-solid fa-people-group',
                'image': 'images/Bali.png',
                'display_order': 5
            },
            {
                'title': 'Sewa Khusus / Charter Fleksibel',
                'short_description': 'Penyewaan bus harian, mingguan, atau kontrak operasional jangka panjang dengan tarif penawaran spesial.',
                'full_description': '[DEMO DATA] Kami membuka kerja sama sewa fleksibel untuk event organizer, biro perjalanan wisata (tour leader), dan korporasi dengan unit yang selalu prima.',
                'icon': 'fa-solid fa-route',
                'image': 'images/hero-bus.jpg',
                'display_order': 6
            }
        ]

        for item in services_data:
            slug = slugify(item['title'])
            existing = Service.query.filter_by(slug=slug).first()
            if not existing:
                serv = Service(
                    title=item['title'],
                    slug=slug,
                    short_description=item['short_description'],
                    full_description=item['full_description'],
                    icon=item['icon'],
                    image=item['image'],
                    display_order=item['display_order'],
                    is_active=True
                )
                db.session.add(serv)
        print("  -> Data layanan transportasi berhasil diinisialisasi.")

        print("[5/7] Inisialisasi Galeri Foto...")
        galleries_data = [
            ('Armada Kebanggaan ASM Transport Kebumen', 'Armada', 'images/hero-bus.jpg', 'Unit Big Bus ASM Transport siap memberikan pelayanan terbaik di jalan raya.', True),
            ('Momen Seru Study Tour Rombongan di Yogyakarta', 'Perjalanan', 'images/Yogya.png', 'Dokumentasi perjalanan rombongan wisata di Kota Pelajar Yogyakarta.', True),
            ('Wisata Alam Sejuk Dataran Tinggi Wonosobo', 'Perjalanan', 'images/Wonosobo.png', 'Perjalanan wisata alam yang menyegarkan bersama rombongan pelanggan.', True),
            ('Eksplorasi Pesona Keindahan Pulau Dewata Bali', 'Perjalanan', 'images/Bali.png', 'Melintasi rute Jawa-Bali dengan armada bus eksekutif berfasilitas lengkap.', True),
            ('Tour Wisata dan Kuliner Rombongan di Bandung', 'Perjalanan', 'images/Bandung.png', 'Kenyamanan perjalanan jauh bersama kru yang berpengalaman.', True),
            ('Unit Big Bus Pariwisata Siap Meluncur', 'Armada', 'images/bus-big.jpg', 'Tampilan eksterior bus yang elegan dan terawat secara berkala.', True),
            ('Kenyamanan Kabin Eksekutif Kursi Empuk', 'Fasilitas', 'images/bus-executive.jpg', 'Interior bersih dengan ruang kaki luas dan pendingin udara sejuk.', True),
            ('Kru Ramah dan Pengemudi Profesional', 'Kru', 'images/bus-medium.jpg', 'Kru bertugas siap melayani kebutuhan penumpang sepanjang perjalanan.', True)
        ]

        for title, category, img, caption, feat in galleries_data:
            existing = Gallery.query.filter_by(title=title).first()
            if not existing:
                gal = Gallery(
                    title=title,
                    category=category,
                    image_file=img,
                    caption=f"[DEMO DATA] {caption}",
                    is_featured=feat
                )
                db.session.add(gal)
        print("  -> Data galeri foto berhasil diinisialisasi.")

        print("[6/7] Inisialisasi Testimoni Pelanggan...")
        testimonials_data = [
            (
                'Bpk. H. Rahmat Hidayat',
                'Ketua Rombongan Ziarah Wali - Kebumen',
                5,
                '[DEMO DATA] Alhamdulillah perjalanan ziarah kami 4 hari 3 malam bersama ASM Transport berjalan sangat lancar. Busnya dingin, kursinya empuk buat istirahat, dan bapak supirnya sangat sabar serta paham rute jalan.',
                'images/bus-executive.jpg'
            ),
            (
                'Ibu Dra. Hj. Siti Nurhaliza',
                'Waka Kesiswaan SMA di Kebumen',
                5,
                '[DEMO DATA] Kami menyewa 3 unit Big Bus ASM Transport untuk acara Study Tour siswa ke Yogyakarta dan Malang. Pelayanannya sangat profesional, tepat waktu, dan fasilitas karaoke di dalam bus membuat anak-anak senang.',
                'images/bus-big.jpg'
            ),
            (
                'Mas Danang Prasetyo',
                'Panitia Family Gathering Komunitas',
                5,
                '[DEMO DATA] Rekomendasi sewa bus pariwisata terbaik di Kebumen. Komunikasi dengan admin lewat WhatsApp responsif dan harga sewanya sangat bersaing dengan kualitas bus yang mewah.',
                'images/hero-bus.jpg'
            ),
            (
                'Bpk. Wahyu Nugroho, S.T.',
                'HR Manager PT Cemerlang Logistik',
                5,
                '[DEMO DATA] Perjalanan dinas dan gathering kantor ke Bandung sangat berkesan. Unit busnya prima, suspensinya halus, dan semua fasilitas berfungsi dengan baik.',
                'images/bus-medium.jpg'
            )
        ]

        for name, role, rating, content, avatar in testimonials_data:
            existing = Testimonial.query.filter_by(customer_name=name).first()
            if not existing:
                testi = Testimonial(
                    customer_name=name,
                    customer_role_or_org=role,
                    rating=rating,
                    content=content,
                    avatar_image=avatar,
                    is_active=True,
                    is_featured=True
                )
                db.session.add(testi)
        print("  -> Data testimoni pelanggan berhasil diinisialisasi.")

        print("[7/7] Inisialisasi Contoh Data Pemesanan (Demo)...")
        first_fleet = Fleet.query.first()
        sample_bookings = [
            {
                'code': 'ASM-20261106-DEMO1',
                'name': 'Bpk. Ahmad Fauzi (Data Demo)',
                'phone': '081234567890',
                'email': 'ahmad.fauzi@example.com',
                'dep': date.today() + timedelta(days=7),
                'ret': date.today() + timedelta(days=9),
                'days': 3,
                'pickup': 'Alun-Alun Kebumen',
                'dest': 'Yogyakarta - Gunungkidul',
                'passengers': 45,
                'requests': '[DEMO DATA] Mohon siapkan bantal dan selimut lengkap untuk rombongan.',
                'status': 'Menunggu Konfirmasi',
                'notes': 'Belum diverifikasi, menunggu konfirmasi customer.'
            },
            {
                'code': 'ASM-20261106-DEMO2',
                'name': 'Ibu Ratna Dewi (Data Demo)',
                'phone': '081987654321',
                'email': 'ratna.dewi@example.com',
                'dep': date.today() + timedelta(days=14),
                'ret': date.today() + timedelta(days=18),
                'days': 5,
                'pickup': 'Kecamatan Gombong, Kebumen',
                'dest': 'Denpasar & Nusa Dua, Bali',
                'passengers': 48,
                'requests': '[DEMO DATA] Perjalanan rombongan PKK, butuh supir yang terbiasa rute penyeberangan Ketapang-Gilimanuk.',
                'status': 'Dikonfirmasi',
                'notes': 'DP 30% telah diterima, armada unit 01 telah dialokasikan.'
            }
        ]

        for sb in sample_bookings:
            existing = Booking.query.filter_by(booking_code=sb['code']).first()
            if not existing:
                book = Booking(
                    booking_code=sb['code'],
                    customer_name=sb['name'],
                    customer_phone=sb['phone'],
                    customer_email=sb['email'],
                    fleet_id=first_fleet.id if first_fleet else None,
                    departure_date=sb['dep'],
                    return_date=sb['ret'],
                    duration_days=sb['days'],
                    pickup_location=sb['pickup'],
                    destination=sb['dest'],
                    bus_count=sb.get('bus_count', 1),
                    passenger_count=sb['passengers'],
                    special_requests=sb['requests'],
                    status=sb['status'],
                    admin_notes=sb['notes']
                )
                db.session.add(book)
        print("  -> Data pemesanan demo berhasil diinisialisasi.")

        db.session.commit()
        print("\n=== SEMUA DATA AWAL (SEED) BERHASIL DIINISIALISASI DENGAN SUKSES! ===")
    except Exception as e:
        db.session.rollback()
        print(f"[SEED ERROR] {e}")


def seed_data(target_app=None):
    """Seed data entrypoint that safely accepts an optional Flask app instance."""
    if target_app:
        with target_app.app_context():
            _run_seed_process()
    else:
        _run_seed_process()


if __name__ == '__main__':
    _cli_app = create_app()
    seed_data(_cli_app)


import unittest
from datetime import date, timedelta
from app import create_app
from app.extensions import db
from app.models import User, Fleet, Booking, Service, Gallery, Testimonial, SiteSetting


class ASMTransportTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('development')
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def login_admin(self):
        return self.client.post('/admin/login', data={
            'username': 'admin',
            'password': 'adminasm2026'
        }, follow_redirects=True)

    # 1. Public Routes
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('ASM', response.get_data(as_text=True))
        self.assertIn('Perjalanan Nyaman, Kenangan Berkesan', response.get_data(as_text=True))

    def test_about_page(self):
        response = self.client.get('/profil')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Profil Perusahaan', response.get_data(as_text=True))
        self.assertIn('Visi Kami', response.get_data(as_text=True))

    def test_fleets_catalog(self):
        response = self.client.get('/armada')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Katalog Armada Bus', response.get_data(as_text=True))

        response_filtered = self.client.get('/armada?kategori=Big+Bus')
        self.assertEqual(response_filtered.status_code, 200)

    def test_fleet_detail(self):
        fleet = Fleet.query.first()
        self.assertIsNotNone(fleet)
        response = self.client.get(f'/armada/{fleet.slug}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(fleet.name, response.get_data(as_text=True))
        self.assertIn('Spesifikasi Kendaraan', response.get_data(as_text=True))

    def test_services_page(self):
        response = self.client.get('/layanan')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Layanan Transportasi Kami', response.get_data(as_text=True))

    def test_gallery_page(self):
        response = self.client.get('/galeri')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Galeri Dokumentasi', response.get_data(as_text=True))

    def test_contact_page(self):
        response = self.client.get('/kontak')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Kantor Operasional & Reservasi', response.get_data(as_text=True))

    def test_booking_submission(self):
        fleet = Fleet.query.first()
        dep = (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')
        ret = (date.today() + timedelta(days=12)).strftime('%Y-%m-%d')

        post_data = {
            'customer_name': 'Bpk. Testing Otomatis',
            'customer_phone': '081299988899',
            'customer_email': 'testing@example.com',
            'fleet_id': fleet.id if fleet else 0,
            'departure_date': dep,
            'return_date': ret,
            'pickup_location': 'Kebumen Kota',
            'destination': 'Semarang - Solo',
            'bus_count': 2,
            'passenger_count': 70,
            'special_requests': 'Butuh unit dengan pendingin AC ekstra dingin.'
        }

        response = self.client.post('/pemesanan', data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Permintaan Pemesanan Berhasil Dikirim', response.get_data(as_text=True))

        booking = Booking.query.filter_by(customer_phone='081299988899').first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.duration_days, 3)
        self.assertEqual(booking.bus_count, 2)
        self.assertEqual(booking.passenger_count, 70)
        self.assertEqual(booking.status, 'Menunggu Konfirmasi')
        self.assertTrue(booking.booking_code.startswith('ASM-'))

    # 2. Authentication & Protected Routes
    def test_admin_requires_login(self):
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login', response.headers['Location'])

    def test_admin_login_logout(self):
        res_fail = self.client.post('/admin/login', data={'username': 'admin', 'password': 'wrong'}, follow_redirects=True)
        self.assertIn('Kredensial login tidak cocok', res_fail.get_data(as_text=True))

        res_success = self.login_admin()
        self.assertEqual(res_success.status_code, 200)
        self.assertIn('Ringkasan Operasional & Dashboard', res_success.get_data(as_text=True))

        res_logout = self.client.get('/admin/logout', follow_redirects=True)
        self.assertIn('berhasil keluar', res_logout.get_data(as_text=True))

    # 3. Fleet CRUD in Admin
    def test_fleet_crud(self):
        self.login_admin()

        # Create
        res_create = self.client.post('/admin/fleets/new', data={
            'name': 'Unit Test Bus 99',
            'category': 'Big Bus',
            'seat_capacity': 50,
            'seat_configuration': '2-2',
            'facilities': 'AC, TV, Audio Karaoke',
            'description': 'Deskripsi unit test bus',
            'transmission': 'Manual 6-Speed',
            'chassis_engine': 'Hino RK8',
            'price_estimate': 'Rp 3.000.000 / Hari',
            'status': 'Tersedia',
            'is_featured': True,
            'is_active': True
        }, follow_redirects=True)
        self.assertEqual(res_create.status_code, 200)
        created_fleet = Fleet.query.filter_by(name='Unit Test Bus 99').first()
        self.assertIsNotNone(created_fleet)

        # Edit
        res_edit = self.client.post(f'/admin/fleets/{created_fleet.id}/edit', data={
            'name': 'Unit Test Bus 99 Edited',
            'category': 'Big Bus',
            'seat_capacity': 52,
            'seat_configuration': '2-2',
            'facilities': 'AC, TV, Audio Karaoke, WiFi',
            'description': 'Deskripsi diedit',
            'transmission': 'Manual 6-Speed',
            'chassis_engine': 'Hino RK8',
            'price_estimate': 'Rp 3.200.000 / Hari',
            'status': 'Beroperasi',
            'is_featured': False,
            'is_active': True
        }, follow_redirects=True)
        self.assertEqual(res_edit.status_code, 200)
        self.assertEqual(created_fleet.seat_capacity, 52)
        self.assertEqual(created_fleet.status, 'Beroperasi')

        # Delete
        res_del = self.client.post(f'/admin/fleets/{created_fleet.id}/delete', follow_redirects=True)
        self.assertEqual(res_del.status_code, 200)
        self.assertIsNone(Fleet.query.filter_by(name='Unit Test Bus 99 Edited').first())

    # 4. Booking Update in Admin
    def test_booking_status_update(self):
        self.login_admin()
        booking = Booking.query.first()
        self.assertIsNotNone(booking)

        res_update = self.client.post(f'/admin/bookings/{booking.id}', data={
            'status': 'Dikonfirmasi',
            'admin_notes': 'DP 30% diterima via transfer BCA'
        }, follow_redirects=True)
        self.assertEqual(res_update.status_code, 200)
        self.assertEqual(booking.status, 'Dikonfirmasi')
        self.assertEqual(booking.admin_notes, 'DP 30% diterima via transfer BCA')

    # 5. Service, Gallery, Testimonial CRUD
    def test_service_crud(self):
        self.login_admin()
        res = self.client.post('/admin/services/new', data={
            'title': 'Layanan Uji Coba',
            'short_description': 'Ringkasan layanan uji coba',
            'full_description': 'Deskripsi lengkap',
            'icon': 'fa-solid fa-star',
            'display_order': 99,
            'is_active': True
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        serv = Service.query.filter_by(title='Layanan Uji Coba').first()
        self.assertIsNotNone(serv)

        # Delete
        res_del = self.client.post(f'/admin/services/{serv.id}/delete', follow_redirects=True)
        self.assertEqual(res_del.status_code, 200)
        self.assertIsNone(Service.query.filter_by(title='Layanan Uji Coba').first())

    # 6. Site Settings Update
    def test_site_settings_update(self):
        self.login_admin()
        res = self.client.post('/admin/settings', data={
            'company_name': 'ASM Transport Kebumen V2',
            'tagline': 'Perjalanan Nyaman, Kenangan Berkesan',
            'whatsapp_number': '62882005363151',
            'office_phone': '(0287) 381-000',
            'office_email': 'kontak@asmtransport.id',
            'address': 'Jl. Raya Kebumen KM 5, Kebumen',
            'operating_hours': '24 Jam Reservasi',
            'about_summary': 'Tentang ASM Transport',
            'instagram_url': 'https://instagram.com',
            'facebook_url': 'https://facebook.com',
            'tiktok_url': 'https://tiktok.com',
            'youtube_url': 'https://youtube.com'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(SiteSetting.get('company_name'), 'ASM Transport Kebumen V2')


if __name__ == '__main__':
    unittest.main()

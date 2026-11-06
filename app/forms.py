from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField,
    TextAreaField, IntegerField, SelectField, DateField
)
from wtforms.validators import (
    DataRequired, Email, Length, Optional, NumberRange, ValidationError
)
from datetime import date


class LoginForm(FlaskForm):
    username = StringField('Username / Email', validators=[DataRequired(message='Username wajib diisi.')])
    password = PasswordField('Kata Sandi', validators=[DataRequired(message='Kata sandi wajib diisi.')])
    remember_me = BooleanField('Ingat saya')
    submit = SubmitField('Masuk ke Dashboard')


class BookingForm(FlaskForm):
    customer_name = StringField('Nama Lengkap', validators=[
        DataRequired(message='Nama lengkap wajib diisi.'),
        Length(min=3, max=100, message='Nama minimal 3 karakter.')
    ])
    customer_phone = StringField('Nomor WhatsApp / HP', validators=[
        DataRequired(message='Nomor WhatsApp wajib diisi.'),
        Length(min=9, max=20, message='Nomor telepon tidak valid.')
    ])
    customer_email = StringField('Alamat Email (Opsional)', validators=[
        Optional(),
        Email(message='Format email tidak valid.')
    ])
    fleet_id = SelectField('Pilihan Armada Bus', coerce=int, validators=[Optional()])
    departure_date = DateField('Tanggal Berangkat', format='%Y-%m-%d', validators=[
        DataRequired(message='Tanggal keberangkatan wajib dipilih.')
    ])
    return_date = DateField('Tanggal Pulang', format='%Y-%m-%d', validators=[
        DataRequired(message='Tanggal kepulangan wajib dipilih.')
    ])
    pickup_location = StringField('Lokasi Penjemputan', validators=[
        DataRequired(message='Lokasi penjemputan wajib diisi.'),
        Length(max=200)
    ])
    destination = StringField('Kota / Destinasi Tujuan', validators=[
        DataRequired(message='Kota / destinasi tujuan wajib diisi.'),
        Length(max=200)
    ])
    bus_count = IntegerField('Jumlah Unit Bus yang Mau Disewa', default=1, validators=[
        DataRequired(message='Jumlah unit bus wajib diisi.'),
        NumberRange(min=1, max=50, message='Jumlah unit bus minimal 1.')
    ])
    passenger_count = IntegerField('Estimasi Jumlah Penumpang', validators=[
        DataRequired(message='Jumlah penumpang wajib diisi.'),
        NumberRange(min=1, max=500, message='Jumlah penumpang minimal 1.')
    ])
    special_requests = TextAreaField('Permintaan Khusus / Catatan Perjalanan (Opsional)')
    submit = SubmitField('Kirim Permintaan Pemesanan')

    def validate_departure_date(self, field):
        if field.data and field.data < date.today():
            raise ValidationError('Tanggal keberangkatan tidak boleh di masa lalu.')

    def validate_return_date(self, field):
        if self.departure_date.data and field.data and field.data < self.departure_date.data:
            raise ValidationError('Tanggal kepulangan harus sama atau setelah tanggal keberangkatan.')


class FleetForm(FlaskForm):
    name = StringField('Nama Armada', validators=[
        DataRequired(message='Nama armada wajib diisi.'),
        Length(max=120)
    ])
    category = SelectField('Kategori Bus', choices=[
        ('Big Bus', 'Big Bus (45 - 59 Seats)'),
        ('Medium Bus', 'Medium Bus (30 - 35 Seats)'),
        ('Executive Bus', 'Executive Bus (28 - 32 Seats)'),
        ('HiAce / Minibus', 'HiAce / Minibus (14 - 19 Seats)')
    ], validators=[DataRequired()])
    seat_capacity = IntegerField('Kapasitas Kursi', validators=[
        DataRequired(message='Kapasitas kursi wajib diisi.'),
        NumberRange(min=1, max=100)
    ])
    seat_configuration = StringField('Konfigurasi Kursi', default='2-2', validators=[Optional(), Length(max=20)])
    facilities = TextAreaField('Fasilitas (Pisahkan dengan koma)', validators=[Optional()],
                               description='Contoh: AC Dingin, Full Audio & Karaoke, TV LED, Reclining Seat, USB Charger, Bantal & Selimut, Toilet')
    description = TextAreaField('Deskripsi Armada', validators=[Optional()])
    transmission = StringField('Transmisi', default='Manual 6-Speed', validators=[Optional(), Length(max=50)])
    chassis_engine = StringField('Sasis & Mesin', default='Mercedes-Benz / Hino', validators=[Optional(), Length(max=100)])
    price_estimate = StringField('Estimasi Harga / Catatan Tarif', default='Hubungi Admin untuk Penawaran', validators=[Optional(), Length(max=100)])
    main_image = FileField('Foto Utama Bus', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Hanya file gambar yang diizinkan (JPG, PNG, WEBP).')
    ])
    status = SelectField('Status Kesiapan', choices=[
        ('Tersedia', 'Tersedia'),
        ('Beroperasi', 'Sedang Beroperasi'),
        ('Perawatan', 'Dalam Perawatan / Maintenance')
    ], default='Tersedia', validators=[DataRequired()])
    is_featured = BooleanField('Tampilkan sebagai Armada Unggulan di Beranda')
    is_active = BooleanField('Status Aktif / Ditampilkan', default=True)
    submit = SubmitField('Simpan Armada')


class BookingAdminUpdateForm(FlaskForm):
    status = SelectField('Status Pemesanan', choices=[
        ('Menunggu Konfirmasi', 'Menunggu Konfirmasi'),
        ('Dikonfirmasi', 'Dikonfirmasi (Disetujui)'),
        ('Selesai', 'Selesai / Terlaksana'),
        ('Dibatalkan', 'Dibatalkan')
    ], validators=[DataRequired()])
    admin_notes = TextAreaField('Catatan Internal Admin / Penawaran Harga')
    submit = SubmitField('Perbarui Status')


class ServiceForm(FlaskForm):
    title = StringField('Judul Layanan', validators=[
        DataRequired(message='Judul layanan wajib diisi.'),
        Length(max=120)
    ])
    short_description = TextAreaField('Ringkasan Layanan', validators=[
        DataRequired(message='Ringkasan wajib diisi.'),
        Length(max=255)
    ])
    full_description = TextAreaField('Deskripsi Lengkap', validators=[Optional()])
    icon = StringField('Ikon (Class FontAwesome)', default='fa-solid fa-bus', validators=[
        DataRequired(message='Ikon FontAwesome wajib diisi.')
    ], description='Contoh: fa-solid fa-bus, fa-solid fa-route, fa-solid fa-graduation-cap, fa-solid fa-mosque')
    image = FileField('Foto Pendukung Layanan', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Hanya file gambar yang diizinkan.')
    ])
    display_order = IntegerField('Urutan Tampil', default=0)
    is_active = BooleanField('Aktif / Tampilkan di Website', default=True)
    submit = SubmitField('Simpan Layanan')


class GalleryForm(FlaskForm):
    title = StringField('Judul / Keterangan Singkat', validators=[
        DataRequired(message='Judul foto wajib diisi.'),
        Length(max=120)
    ])
    category = SelectField('Kategori Galeri', choices=[
        ('Armada', 'Armada & Eksterior'),
        ('Perjalanan', 'Momen Perjalanan / Wisata'),
        ('Fasilitas', 'Interior & Fasilitas'),
        ('Kru', 'Kru & Layanan')
    ], validators=[DataRequired()])
    image_file = FileField('File Gambar', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Hanya file gambar yang diizinkan.')
    ])
    caption = TextAreaField('Keterangan Tambahan', validators=[Optional()])
    is_featured = BooleanField('Tampilkan di Beranda')
    submit = SubmitField('Simpan Foto Galeri')


class TestimonialForm(FlaskForm):
    customer_name = StringField('Nama Pelanggan', validators=[
        DataRequired(message='Nama pelanggan wajib diisi.'),
        Length(max=120)
    ])
    customer_role_or_org = StringField('Instansi / Rombongan / Asal', validators=[
        Optional(),
        Length(max=120)
    ], description='Contoh: Komite SMAN 1 Kebumen, PT Megah Abadi, Rombongan Keluarga Semarang')
    rating = SelectField('Rating Bintang', choices=[
        ('5', '5 Bintang (Sangat Puas)'),
        ('4', '4 Bintang (Puas)'),
        ('3', '3 Bintang (Cukup)'),
        ('2', '2 Bintang (Kurang)'),
        ('1', '1 Bintang (Kecewa)')
    ], default='5', coerce=int, validators=[DataRequired()])
    content = TextAreaField('Isi Ulasan / Testimoni', validators=[
        DataRequired(message='Isi testimoni wajib diisi.')
    ])
    avatar_image = FileField('Foto Pelanggan / Avatar', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Hanya file gambar yang diizinkan.')
    ])
    is_active = BooleanField('Tampilkan di Website', default=True)
    is_featured = BooleanField('Tampilkan di Beranda', default=True)
    submit = SubmitField('Simpan Testimoni')


class SettingsForm(FlaskForm):
    company_name = StringField('Nama Perusahaan', validators=[DataRequired()])
    tagline = StringField('Slogan Perusahaan', validators=[DataRequired()])
    whatsapp_number = StringField('Nomor WhatsApp', validators=[DataRequired()])
    office_phone = StringField('Telepon Kantor', validators=[Optional()])
    office_email = StringField('Email Resmi', validators=[Optional(), Email()])
    address = TextAreaField('Alamat Kantor', validators=[DataRequired()])
    operating_hours = StringField('Jam Operasional Layanan', validators=[Optional()])
    about_summary = TextAreaField('Ringkasan Tentang Kami', validators=[Optional()])
    instagram_url = StringField('Link Instagram', validators=[Optional()])
    facebook_url = StringField('Link Facebook', validators=[Optional()])
    tiktok_url = StringField('Link TikTok', validators=[Optional()])
    youtube_url = StringField('Link YouTube', validators=[Optional()])
    submit = SubmitField('Simpan Pengaturan Website')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Kata Sandi Saat Ini', validators=[
        DataRequired(message='Kata sandi saat ini wajib diisi.')
    ])
    new_password = PasswordField('Kata Sandi Baru', validators=[
        DataRequired(message='Kata sandi baru wajib diisi.'),
        Length(min=6, message='Kata sandi baru minimal 6 karakter.')
    ])
    confirm_password = PasswordField('Konfirmasi Kata Sandi Baru', validators=[
        DataRequired(message='Konfirmasi kata sandi wajib diisi.')
    ])
    submit = SubmitField('Perbarui Kata Sandi')

    def validate_confirm_password(self, field):
        if field.data != self.new_password.data:
            raise ValidationError('Konfirmasi kata sandi tidak cocok dengan kata sandi baru.')


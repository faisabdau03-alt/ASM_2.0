import urllib.parse
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='admin', nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Fleet(db.Model):
    __tablename__ = 'fleets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)  # Big Bus, Medium Bus, Minibus/Elf
    seat_capacity = db.Column(db.Integer, nullable=False)
    seat_configuration = db.Column(db.String(20), default='2-2')  # 2-2, 2-1, dsb
    facilities = db.Column(db.Text, nullable=True)  # Comma-separated list
    description = db.Column(db.Text, nullable=True)
    transmission = db.Column(db.String(50), default='Manual 6-Speed')
    chassis_engine = db.Column(db.String(100), default='Mercedes-Benz / Hino')
    price_estimate = db.Column(db.String(100), default='Hubungi Admin untuk Penawaran')
    main_image = db.Column(db.String(255), default='images/bus-big.jpg')
    status = db.Column(db.String(30), default='Tersedia')  # Tersedia, Beroperasi, Perawatan
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bookings = db.relationship('Booking', backref='fleet', lazy='dynamic')

    @property
    def facilities_list(self):
        if not self.facilities:
            return []
        return [item.strip() for item in self.facilities.split(',') if item.strip()]

    def __repr__(self):
        return f'<Fleet {self.name}>'


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    booking_code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(30), nullable=False)
    customer_email = db.Column(db.String(120), nullable=True)
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleets.id', ondelete='SET NULL'), nullable=True)
    departure_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    duration_days = db.Column(db.Integer, default=1)
    pickup_location = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    bus_count = db.Column(db.Integer, default=1, nullable=False)
    passenger_count = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='Menunggu Konfirmasi')  # Menunggu Konfirmasi, Dikonfirmasi, Dibatalkan, Selesai
    admin_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def generate_whatsapp_link(self, target_phone='62882005363151'):
        fleet_name = self.fleet.name if self.fleet else 'Pilihan Fleksibel'
        msg = (
            f"Halo Admin ASM Transport Kebumen,\n\n"
            f"Saya ingin mengonfirmasi permintaan pemesanan sewa bus:\n"
            f"📌 *Kode Booking*: {self.booking_code}\n"
            f"👤 *Nama*: {self.customer_name}\n"
            f"📞 *No HP/WA*: {self.customer_phone}\n"
            f"🚌 *Pilihan Armada*: {fleet_name} ({self.bus_count} Unit Bus)\n"
            f"👥 *Jumlah Penumpang*: {self.passenger_count} orang\n"
            f"📍 *Titik Jemput*: {self.pickup_location}\n"
            f"🎯 *Tujuan*: {self.destination}\n"
            f"🗓️ *Tanggal*: {self.departure_date.strftime('%d-%m-%Y')} s/d {self.return_date.strftime('%d-%m-%Y')} ({self.duration_days} Hari)\n"
        )
        if self.special_requests:
            msg += f"📝 *Catatan Khusus*: {self.special_requests}\n"
        msg += "\nMohon konfirmasi ketersediaan unit dan rincian penawaran harganya. Terima kasih!"
        
        encoded_msg = urllib.parse.quote(msg)
        cleaned_phone = ''.join(filter(str.isdigit, target_phone))
        return f"https://wa.me/{cleaned_phone}?text={encoded_msg}"

    def __repr__(self):
        return f'<Booking {self.booking_code}>'


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), unique=True, nullable=False, index=True)
    short_description = db.Column(db.String(255), nullable=False)
    full_description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(60), default='fa-solid fa-bus')
    image = db.Column(db.String(255), nullable=True)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Service {self.title}>'


class Gallery(db.Model):
    __tablename__ = 'galleries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), default='Armada')  # Armada, Perjalanan, Fasilitas, Kru
    image_file = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.Text, nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Gallery {self.title}>'


class Testimonial(db.Model):
    __tablename__ = 'testimonials'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_role_or_org = db.Column(db.String(120), nullable=True)
    rating = db.Column(db.Integer, default=5)
    content = db.Column(db.Text, nullable=False)
    avatar_image = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Testimonial {self.customer_name}>'


class SiteSetting(db.Model):
    __tablename__ = 'site_settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=True)
    label = db.Column(db.String(120), nullable=True)
    group = db.Column(db.String(50), default='general')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get(cls, key, default=None):
        setting = cls.query.filter_by(key=key).first()
        if setting and setting.value is not None:
            return setting.value
        return default

    @classmethod
    def set(cls, key, value, label=None, group='general'):
        setting = cls.query.filter_by(key=key).first()
        if not setting:
            setting = cls(key=key, value=value, label=label or key, group=group)
            db.session.add(setting)
        else:
            setting.value = value
            if label:
                setting.label = label
            if group:
                setting.group = group
        db.session.commit()
        return setting

    def __repr__(self):
        return f'<SiteSetting {self.key}>'

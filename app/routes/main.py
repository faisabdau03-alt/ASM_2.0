from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.extensions import db
from app.models import Fleet, Service, Gallery, Testimonial, Booking, SiteSetting
from app.forms import BookingForm
from app.utils import generate_booking_code, format_date_id
from datetime import datetime

main_bp = Blueprint('main', __name__)


@main_bp.app_context_processor
def inject_global_data():
    """Inject settings and helpers across all templates."""
    settings_dict = {
        'company_name': SiteSetting.get('company_name', 'ASM Transport Kebumen'),
        'tagline': SiteSetting.get('tagline', 'Perjalanan Nyaman, Kenangan Berkesan'),
        'whatsapp_number': SiteSetting.get('whatsapp_number', current_app.config.get('WHATSAPP_NUMBER', '62882005363151')),
        'office_phone': SiteSetting.get('office_phone', '(0287) 381-000'),
        'office_email': SiteSetting.get('office_email', 'info@asmtransport.id'),
        'address': SiteSetting.get('address', 'Jl. Raya Kebumen - Purworejo KM. 5, Kebumen, Jawa Tengah 54311'),
        'operating_hours': SiteSetting.get('operating_hours', 'Senin - Minggu: 24 Jam Pelayanan Reservasi'),
        'about_summary': SiteSetting.get('about_summary', 'ASM Transport (PO Alula Sadida Maryam) adalah penyedia jasa transportasi bus pariwisata terpercaya yang berbasis di Kebumen, Jawa Tengah.'),
        'instagram_url': SiteSetting.get('instagram_url', 'https://instagram.com/asmtransport_kebumen'),
        'facebook_url': SiteSetting.get('facebook_url', 'https://facebook.com'),
        'tiktok_url': SiteSetting.get('tiktok_url', 'https://tiktok.com'),
        'youtube_url': SiteSetting.get('youtube_url', 'https://youtube.com'),
    }
    return {
        'site_settings': settings_dict,
        'current_year': datetime.utcnow().year,
        'format_date_id': format_date_id
    }


@main_bp.route('/')
def index():
    """Homepage"""
    featured_fleets = Fleet.query.filter_by(is_active=True, is_featured=True).limit(4).all()
    if not featured_fleets:
        featured_fleets = Fleet.query.filter_by(is_active=True).limit(4).all()

    services = Service.query.filter_by(is_active=True).order_by(Service.display_order.asc()).limit(6).all()
    galleries = Gallery.query.filter_by(is_featured=True).limit(8).all()
    if not galleries:
        galleries = Gallery.query.order_by(Gallery.created_at.desc()).limit(8).all()

    testimonials = Testimonial.query.filter_by(is_active=True, is_featured=True).order_by(Testimonial.created_at.desc()).limit(6).all()
    fleets_count = Fleet.query.filter_by(is_active=True).count()
    completed_trips = Booking.query.filter_by(status='Selesai').count() + 150  # baseline demo count

    return render_template(
        'pages/index.html',
        featured_fleets=featured_fleets,
        services=services,
        galleries=galleries,
        testimonials=testimonials,
        fleets_count=fleets_count,
        completed_trips=completed_trips
    )


@main_bp.route('/profil')
def about():
    """Company Profile page"""
    testimonials = Testimonial.query.filter_by(is_active=True).limit(3).all()
    fleets_count = Fleet.query.filter_by(is_active=True).count()
    return render_template('pages/about.html', testimonials=testimonials, fleets_count=fleets_count)


@main_bp.route('/armada')
def fleets():
    """Fleet Catalog page with optional category filter"""
    category_filter = request.args.get('kategori', '').strip()
    query = Fleet.query.filter_by(is_active=True)

    if category_filter:
        query = query.filter_by(category=category_filter)

    fleet_list = query.order_by(Fleet.is_featured.desc(), Fleet.seat_capacity.desc()).all()
    categories = ['Big Bus', 'Medium Bus', 'Executive Bus', 'HiAce / Minibus']

    return render_template(
        'pages/fleets.html',
        fleets=fleet_list,
        current_category=category_filter,
        categories=categories
    )


@main_bp.route('/armada/<slug>')
def fleet_detail(slug):
    """Fleet Detail page"""
    fleet = Fleet.query.filter_by(slug=slug, is_active=True).first_or_404()
    related_fleets = Fleet.query.filter(
        Fleet.id != fleet.id,
        Fleet.is_active == True,
        Fleet.category == fleet.category
    ).limit(3).all()
    if not related_fleets:
        related_fleets = Fleet.query.filter(Fleet.id != fleet.id, Fleet.is_active == True).limit(3).all()

    return render_template('pages/fleet_detail.html', fleet=fleet, related_fleets=related_fleets)


@main_bp.route('/layanan')
def services():
    """Services page"""
    all_services = Service.query.filter_by(is_active=True).order_by(Service.display_order.asc()).all()
    return render_template('pages/services.html', services=all_services)


@main_bp.route('/galeri')
def gallery():
    """Gallery page with category filter"""
    category_filter = request.args.get('kategori', '').strip()
    query = Gallery.query

    if category_filter and category_filter != 'Semua':
        query = query.filter_by(category=category_filter)

    items = query.order_by(Gallery.created_at.desc()).all()
    categories = ['Semua', 'Armada', 'Perjalanan', 'Fasilitas', 'Kru']

    return render_template(
        'pages/gallery.html',
        galleries=items,
        current_category=category_filter or 'Semua',
        categories=categories
    )


@main_bp.route('/kontak', methods=['GET', 'POST'])
def contact():
    """Contact page with quick message form"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        message = request.form.get('message', '').strip()
        subject = request.form.get('subject', 'Pertanyaan Umum')

        if not name or not phone or not message:
            flash('Harap lengkapi seluruh formulir kontak sebelum mengirim pesan.', 'danger')
        else:
            flash('Terima kasih! Pesan Anda telah kami terima. Tim ASM Transport Kebumen akan segera menghubungi Anda.', 'success')
            return redirect(url_for('main.contact'))

    return render_template('pages/contact.html')


@main_bp.route('/pemesanan', methods=['GET', 'POST'])
def booking():
    """Booking Request Form page"""
    form = BookingForm()

    # Populate fleet choices
    active_fleets = Fleet.query.filter_by(is_active=True).order_by(Fleet.name.asc()).all()
    form.fleet_id.choices = [(0, '-- Pilih Armada (Bisa Konsultasi Admin) --')] + [
        (f.id, f"{f.name} ({f.category} - {f.seat_capacity} Kursi)") for f in active_fleets
    ]

    # Pre-select fleet if passed via query params ?fleet_id=...
    preselect_fleet_id = request.args.get('fleet_id', type=int)
    if request.method == 'GET' and preselect_fleet_id:
        form.fleet_id.data = preselect_fleet_id

    if form.validate_on_submit():
        # Calculate duration
        days = (form.return_date.data - form.departure_date.data).days + 1
        if days < 1:
            days = 1

        selected_fleet_id = form.fleet_id.data if form.fleet_id.data != 0 else None

        new_booking = Booking(
            booking_code=generate_booking_code(),
            customer_name=form.customer_name.data.strip(),
            customer_phone=form.customer_phone.data.strip(),
            customer_email=form.customer_email.data.strip() if form.customer_email.data else None,
            fleet_id=selected_fleet_id,
            departure_date=form.departure_date.data,
            return_date=form.return_date.data,
            duration_days=days,
            pickup_location=form.pickup_location.data.strip(),
            destination=form.destination.data.strip(),
            bus_count=form.bus_count.data or 1,
            passenger_count=form.passenger_count.data,
            special_requests=form.special_requests.data.strip() if form.special_requests.data else None,
            status='Menunggu Konfirmasi'
        )

        db.session.add(new_booking)
        db.session.commit()

        flash('Permintaan pemesanan Anda berhasil dikirim! Silakan konfirmasi ke WhatsApp admin untuk respon instan.', 'success')
        return redirect(url_for('main.booking_success', booking_code=new_booking.booking_code))

    return render_template('pages/booking.html', form=form, active_fleets=active_fleets)


@main_bp.route('/pemesanan/sukses/<booking_code>')
def booking_success(booking_code):
    """Booking Success & WhatsApp Confirmation Page"""
    booking_item = Booking.query.filter_by(booking_code=booking_code).first_or_404()
    whatsapp_number = SiteSetting.get('whatsapp_number', current_app.config.get('WHATSAPP_NUMBER', '62882005363151'))
    wa_link = booking_item.generate_whatsapp_link(whatsapp_number)

    return render_template(
        'pages/booking_success.html',
        booking=booking_item,
        wa_link=wa_link,
        whatsapp_number=whatsapp_number
    )


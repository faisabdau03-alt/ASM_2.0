import os
from flask import (
    Blueprint, render_template, redirect, url_for, flash,
    request, current_app
)
from flask_login import login_required, current_user
from app.extensions import db
from app.models import (
    User, Fleet, Booking, Service, Gallery, Testimonial, SiteSetting
)
from app.forms import (
    FleetForm, BookingAdminUpdateForm, ServiceForm,
    GalleryForm, TestimonialForm, SettingsForm, ChangePasswordForm
)
from app.utils import save_uploaded_file, slugify

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.before_request
@login_required
def require_login():
    """Ensure all routes in admin_bp require authentication."""
    pass


# -------------------------------------------------------------
# DASHBOARD OVERVIEW
# -------------------------------------------------------------
@admin_bp.route('/')
@admin_bp.route('/dashboard')
def dashboard():
    total_bookings = Booking.query.count()
    pending_bookings = Booking.query.filter_by(status='Menunggu Konfirmasi').count()
    confirmed_bookings = Booking.query.filter_by(status='Dikonfirmasi').count()
    total_fleets = Fleet.query.count()
    active_fleets = Fleet.query.filter_by(is_active=True).count()
    total_services = Service.query.count()
    total_galleries = Gallery.query.count()
    total_testimonials = Testimonial.query.count()

    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(8).all()
    recent_fleets = Fleet.query.order_by(Fleet.created_at.desc()).limit(4).all()

    return render_template(
        'admin/dashboard.html',
        total_bookings=total_bookings,
        pending_bookings=pending_bookings,
        confirmed_bookings=confirmed_bookings,
        total_fleets=total_fleets,
        active_fleets=active_fleets,
        total_services=total_services,
        total_galleries=total_galleries,
        total_testimonials=total_testimonials,
        recent_bookings=recent_bookings,
        recent_fleets=recent_fleets
    )


# -------------------------------------------------------------
# FLEETS CRUD
# -------------------------------------------------------------
@admin_bp.route('/fleets')
def fleets_list():
    query = Fleet.query
    category = request.args.get('kategori', '').strip()
    status = request.args.get('status', '').strip()

    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)

    fleets = query.order_by(Fleet.created_at.desc()).all()
    return render_template('admin/fleets/index.html', fleets=fleets, current_category=category, current_status=status)


@admin_bp.route('/fleets/new', methods=['GET', 'POST'])
def fleet_create():
    form = FleetForm()
    if form.validate_on_submit():
        # Generate unique slug
        base_slug = slugify(form.name.data)
        slug = base_slug
        counter = 1
        while Fleet.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        image_path = 'images/bus-big.jpg'
        if form.main_image.data:
            uploaded = save_uploaded_file(form.main_image.data, subfolder='fleets')
            if uploaded:
                image_path = uploaded

        fleet = Fleet(
            name=form.name.data.strip(),
            slug=slug,
            category=form.category.data,
            seat_capacity=form.seat_capacity.data,
            seat_configuration=form.seat_configuration.data or '2-2',
            facilities=form.facilities.data.strip() if form.facilities.data else None,
            description=form.description.data.strip() if form.description.data else None,
            transmission=form.transmission.data.strip() if form.transmission.data else 'Manual 6-Speed',
            chassis_engine=form.chassis_engine.data.strip() if form.chassis_engine.data else 'Mercedes-Benz / Hino',
            price_estimate=form.price_estimate.data.strip() if form.price_estimate.data else 'Hubungi Admin untuk Penawaran',
            main_image=image_path,
            status=form.status.data,
            is_featured=form.is_featured.data,
            is_active=form.is_active.data
        )
        db.session.add(fleet)
        db.session.commit()
        flash(f'Armada "{fleet.name}" berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.fleets_list'))

    return render_template('admin/fleets/form.html', form=form, title='Tambah Armada Baru')


@admin_bp.route('/fleets/<int:id>/edit', methods=['GET', 'POST'])
def fleet_edit(id):
    fleet = db.get_or_404(Fleet, id)
    form = FleetForm(obj=fleet)

    if form.validate_on_submit():
        if form.name.data.strip() != fleet.name:
            base_slug = slugify(form.name.data)
            slug = base_slug
            counter = 1
            while Fleet.query.filter(Fleet.slug == slug, Fleet.id != fleet.id).first():
                slug = f"{base_slug}-{counter}"
                counter += 1
            fleet.slug = slug

        fleet.name = form.name.data.strip()
        fleet.category = form.category.data
        fleet.seat_capacity = form.seat_capacity.data
        fleet.seat_configuration = form.seat_configuration.data or '2-2'
        fleet.facilities = form.facilities.data.strip() if form.facilities.data else None
        fleet.description = form.description.data.strip() if form.description.data else None
        fleet.transmission = form.transmission.data.strip() if form.transmission.data else 'Manual 6-Speed'
        fleet.chassis_engine = form.chassis_engine.data.strip() if form.chassis_engine.data else 'Mercedes-Benz / Hino'
        fleet.price_estimate = form.price_estimate.data.strip() if form.price_estimate.data else 'Hubungi Admin untuk Penawaran'
        fleet.status = form.status.data
        fleet.is_featured = form.is_featured.data
        fleet.is_active = form.is_active.data

        if form.main_image.data and hasattr(form.main_image.data, 'filename') and form.main_image.data.filename:
            uploaded = save_uploaded_file(form.main_image.data, subfolder='fleets')
            if uploaded:
                fleet.main_image = uploaded

        db.session.commit()
        flash(f'Perubahan data armada "{fleet.name}" berhasil disimpan.', 'success')
        return redirect(url_for('admin.fleets_list'))

    return render_template('admin/fleets/form.html', form=form, fleet=fleet, title='Edit Data Armada')


@admin_bp.route('/fleets/<int:id>/delete', methods=['POST'])
def fleet_delete(id):
    fleet = db.get_or_404(Fleet, id)
    name = fleet.name
    db.session.delete(fleet)
    db.session.commit()
    flash(f'Armada "{name}" berhasil dihapus.', 'info')
    return redirect(url_for('admin.fleets_list'))


# -------------------------------------------------------------
# BOOKINGS MANAGEMENT
# -------------------------------------------------------------
@admin_bp.route('/bookings')
def bookings_list():
    status_filter = request.args.get('status', '').strip()
    query = Booking.query

    if status_filter:
        query = query.filter_by(status=status_filter)

    bookings = query.order_by(Booking.created_at.desc()).all()
    statuses = ['Menunggu Konfirmasi', 'Dikonfirmasi', 'Selesai', 'Dibatalkan']

    return render_template(
        'admin/bookings/index.html',
        bookings=bookings,
        current_status=status_filter,
        statuses=statuses
    )


@admin_bp.route('/bookings/<int:id>', methods=['GET', 'POST'])
def booking_detail(id):
    booking = db.get_or_404(Booking, id)
    form = BookingAdminUpdateForm(obj=booking)

    if form.validate_on_submit():
        booking.status = form.status.data
        booking.admin_notes = form.admin_notes.data.strip() if form.admin_notes.data else None
        db.session.commit()
        flash(f'Status pemesanan {booking.booking_code} berhasil diperbarui menjadi "{booking.status}".', 'success')
        return redirect(url_for('admin.booking_detail', id=booking.id))

    whatsapp_number = SiteSetting.get('whatsapp_number', current_app.config.get('WHATSAPP_NUMBER', '62882005363151'))
    customer_wa_link = booking.generate_whatsapp_link(booking.customer_phone)

    return render_template(
        'admin/bookings/detail.html',
        booking=booking,
        form=form,
        customer_wa_link=customer_wa_link
    )


@admin_bp.route('/bookings/<int:id>/delete', methods=['POST'])
def booking_delete(id):
    booking = db.get_or_404(Booking, id)
    code = booking.booking_code
    db.session.delete(booking)
    db.session.commit()
    flash(f'Data pemesanan {code} berhasil dihapus.', 'info')
    return redirect(url_for('admin.bookings_list'))


# -------------------------------------------------------------
# SERVICES CRUD
# -------------------------------------------------------------
@admin_bp.route('/services')
def services_list():
    services = Service.query.order_by(Service.display_order.asc(), Service.created_at.asc()).all()
    return render_template('admin/services/index.html', services=services)


@admin_bp.route('/services/new', methods=['GET', 'POST'])
def service_create():
    form = ServiceForm()
    if form.validate_on_submit():
        base_slug = slugify(form.title.data)
        slug = base_slug
        counter = 1
        while Service.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        image_path = None
        if form.image.data:
            uploaded = save_uploaded_file(form.image.data, subfolder='services')
            if uploaded:
                image_path = uploaded

        service = Service(
            title=form.title.data.strip(),
            slug=slug,
            short_description=form.short_description.data.strip(),
            full_description=form.full_description.data.strip() if form.full_description.data else None,
            icon=form.icon.data.strip() or 'fa-solid fa-bus',
            image=image_path,
            display_order=form.display_order.data or 0,
            is_active=form.is_active.data
        )
        db.session.add(service)
        db.session.commit()
        flash(f'Layanan "{service.title}" berhasil ditambahkan.', 'success')
        return redirect(url_for('admin.services_list'))

    return render_template('admin/services/form.html', form=form, title='Tambah Layanan Baru')


@admin_bp.route('/services/<int:id>/edit', methods=['GET', 'POST'])
def service_edit(id):
    service = db.get_or_404(Service, id)
    form = ServiceForm(obj=service)

    if form.validate_on_submit():
        if form.title.data.strip() != service.title:
            base_slug = slugify(form.title.data)
            slug = base_slug
            counter = 1
            while Service.query.filter(Service.slug == slug, Service.id != service.id).first():
                slug = f"{base_slug}-{counter}"
                counter += 1
            service.slug = slug

        service.title = form.title.data.strip()
        service.short_description = form.short_description.data.strip()
        service.full_description = form.full_description.data.strip() if form.full_description.data else None
        service.icon = form.icon.data.strip() or 'fa-solid fa-bus'
        service.display_order = form.display_order.data or 0
        service.is_active = form.is_active.data

        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            uploaded = save_uploaded_file(form.image.data, subfolder='services')
            if uploaded:
                service.image = uploaded

        db.session.commit()
        flash(f'Layanan "{service.title}" berhasil diperbarui.', 'success')
        return redirect(url_for('admin.services_list'))

    return render_template('admin/services/form.html', form=form, service=service, title='Edit Layanan')


@admin_bp.route('/services/<int:id>/delete', methods=['POST'])
def service_delete(id):
    service = db.get_or_404(Service, id)
    title = service.title
    db.session.delete(service)
    db.session.commit()
    flash(f'Layanan "{title}" berhasil dihapus.', 'info')
    return redirect(url_for('admin.services_list'))


# -------------------------------------------------------------
# GALLERIES CRUD
# -------------------------------------------------------------
@admin_bp.route('/galleries')
def galleries_list():
    category = request.args.get('kategori', '').strip()
    query = Gallery.query
    if category:
        query = query.filter_by(category=category)

    galleries = query.order_by(Gallery.created_at.desc()).all()
    categories = ['Armada', 'Perjalanan', 'Fasilitas', 'Kru']
    return render_template('admin/galleries/index.html', galleries=galleries, current_category=category, categories=categories)


@admin_bp.route('/galleries/new', methods=['GET', 'POST'])
def gallery_create():
    form = GalleryForm()
    if form.validate_on_submit():
        image_path = 'images/hero-bus.jpg'
        if form.image_file.data:
            uploaded = save_uploaded_file(form.image_file.data, subfolder='galleries')
            if uploaded:
                image_path = uploaded
        else:
            flash('Harap pilih file gambar untuk galeri.', 'danger')
            return render_template('admin/galleries/form.html', form=form, title='Tambah Foto Galeri')

        item = Gallery(
            title=form.title.data.strip(),
            category=form.category.data,
            image_file=image_path,
            caption=form.caption.data.strip() if form.caption.data else None,
            is_featured=form.is_featured.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Foto galeri berhasil ditambahkan.', 'success')
        return redirect(url_for('admin.galleries_list'))

    return render_template('admin/galleries/form.html', form=form, title='Tambah Foto Galeri')


@admin_bp.route('/galleries/<int:id>/edit', methods=['GET', 'POST'])
def gallery_edit(id):
    item = db.get_or_404(Gallery, id)
    form = GalleryForm(obj=item)

    if form.validate_on_submit():
        item.title = form.title.data.strip()
        item.category = form.category.data
        item.caption = form.caption.data.strip() if form.caption.data else None
        item.is_featured = form.is_featured.data

        if form.image_file.data and hasattr(form.image_file.data, 'filename') and form.image_file.data.filename:
            uploaded = save_uploaded_file(form.image_file.data, subfolder='galleries')
            if uploaded:
                item.image_file = uploaded

        db.session.commit()
        flash('Foto galeri berhasil diperbarui.', 'success')
        return redirect(url_for('admin.galleries_list'))

    return render_template('admin/galleries/form.html', form=form, gallery=item, title='Edit Foto Galeri')


@admin_bp.route('/galleries/<int:id>/delete', methods=['POST'])
def gallery_delete(id):
    item = db.get_or_404(Gallery, id)
    title = item.title
    db.session.delete(item)
    db.session.commit()
    flash(f'Foto galeri "{title}" berhasil dihapus.', 'info')
    return redirect(url_for('admin.galleries_list'))


# -------------------------------------------------------------
# TESTIMONIALS CRUD
# -------------------------------------------------------------
@admin_bp.route('/testimonials')
def testimonials_list():
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials/index.html', testimonials=testimonials)


@admin_bp.route('/testimonials/new', methods=['GET', 'POST'])
def testimonial_create():
    form = TestimonialForm()
    if form.validate_on_submit():
        avatar_path = None
        if form.avatar_image.data:
            uploaded = save_uploaded_file(form.avatar_image.data, subfolder='testimonials')
            if uploaded:
                avatar_path = uploaded

        testimonial = Testimonial(
            customer_name=form.customer_name.data.strip(),
            customer_role_or_org=form.customer_role_or_org.data.strip() if form.customer_role_or_org.data else None,
            rating=form.rating.data,
            content=form.content.data.strip(),
            avatar_image=avatar_path,
            is_active=form.is_active.data,
            is_featured=form.is_featured.data
        )
        db.session.add(testimonial)
        db.session.commit()
        flash('Testimoni pelanggan berhasil ditambahkan.', 'success')
        return redirect(url_for('admin.testimonials_list'))

    return render_template('admin/testimonials/form.html', form=form, title='Tambah Testimoni Baru')


@admin_bp.route('/testimonials/<int:id>/edit', methods=['GET', 'POST'])
def testimonial_edit(id):
    item = db.get_or_404(Testimonial, id)
    form = TestimonialForm(obj=item)

    if form.validate_on_submit():
        item.customer_name = form.customer_name.data.strip()
        item.customer_role_or_org = form.customer_role_or_org.data.strip() if form.customer_role_or_org.data else None
        item.rating = form.rating.data
        item.content = form.content.data.strip()
        item.is_active = form.is_active.data
        item.is_featured = form.is_featured.data

        if form.avatar_image.data and hasattr(form.avatar_image.data, 'filename') and form.avatar_image.data.filename:
            uploaded = save_uploaded_file(form.avatar_image.data, subfolder='testimonials')
            if uploaded:
                item.avatar_image = uploaded

        db.session.commit()
        flash('Testimoni berhasil diperbarui.', 'success')
        return redirect(url_for('admin.testimonials_list'))

    return render_template('admin/testimonials/form.html', form=form, testimonial=item, title='Edit Testimoni')


@admin_bp.route('/testimonials/<int:id>/delete', methods=['POST'])
def testimonial_delete(id):
    item = db.get_or_404(Testimonial, id)
    name = item.customer_name
    db.session.delete(item)
    db.session.commit()
    flash(f'Testimoni dari "{name}" berhasil dihapus.', 'info')
    return redirect(url_for('admin.testimonials_list'))


# -------------------------------------------------------------
# SETTINGS & PROFILE
# -------------------------------------------------------------
@admin_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()

    if form.validate_on_submit():
        SiteSetting.set('company_name', form.company_name.data.strip(), 'Nama Perusahaan')
        SiteSetting.set('tagline', form.tagline.data.strip(), 'Slogan Perusahaan')
        SiteSetting.set('whatsapp_number', form.whatsapp_number.data.strip(), 'Nomor WhatsApp')
        SiteSetting.set('office_phone', form.office_phone.data.strip(), 'Telepon Kantor')
        SiteSetting.set('office_email', form.office_email.data.strip(), 'Email Resmi')
        SiteSetting.set('address', form.address.data.strip(), 'Alamat Kantor')
        SiteSetting.set('operating_hours', form.operating_hours.data.strip(), 'Jam Operasional')
        SiteSetting.set('about_summary', form.about_summary.data.strip(), 'Ringkasan Tentang Kami')
        SiteSetting.set('instagram_url', form.instagram_url.data.strip(), 'Instagram')
        SiteSetting.set('facebook_url', form.facebook_url.data.strip(), 'Facebook')
        SiteSetting.set('tiktok_url', form.tiktok_url.data.strip(), 'TikTok')
        SiteSetting.set('youtube_url', form.youtube_url.data.strip(), 'YouTube')

        flash('Pengaturan website berhasil diperbarui.', 'success')
        return redirect(url_for('admin.settings'))

    if request.method == 'GET':
        form.company_name.data = SiteSetting.get('company_name', 'ASM Transport Kebumen')
        form.tagline.data = SiteSetting.get('tagline', 'Perjalanan Nyaman, Kenangan Berkesan')
        form.whatsapp_number.data = SiteSetting.get('whatsapp_number', '62882005363151')
        form.office_phone.data = SiteSetting.get('office_phone', '(0287) 381-000')
        form.office_email.data = SiteSetting.get('office_email', 'info@asmtransport.id')
        form.address.data = SiteSetting.get('address', 'Jl. Raya Kebumen - Purworejo KM. 5, Kebumen, Jawa Tengah 54311')
        form.operating_hours.data = SiteSetting.get('operating_hours', 'Senin - Minggu: 24 Jam Pelayanan Reservasi')
        form.about_summary.data = SiteSetting.get('about_summary', 'ASM Transport (PO Alula Sadida Maryam) adalah penyedia jasa transportasi bus pariwisata terpercaya yang berbasis di Kebumen, Jawa Tengah.')
        form.instagram_url.data = SiteSetting.get('instagram_url', 'https://instagram.com/asmtransport_kebumen')
        form.facebook_url.data = SiteSetting.get('facebook_url', 'https://facebook.com')
        form.tiktok_url.data = SiteSetting.get('tiktok_url', 'https://tiktok.com')
        form.youtube_url.data = SiteSetting.get('youtube_url', 'https://youtube.com')

    return render_template('admin/settings.html', form=form)


@admin_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Kata sandi saat ini salah.', 'danger')
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Kata sandi Anda berhasil diperbarui. Silakan gunakan kata sandi baru untuk login berikutnya.', 'success')
            return redirect(url_for('admin.profile'))

    return render_template('admin/profile.html', form=form)

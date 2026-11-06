from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app.forms import LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/admin')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
            (User.username == form.username.data.strip()) |
            (User.email == form.username.data.strip().lower())
        ).first()

        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Akun Anda dinonaktifkan. Silakan hubungi pengelola sistem.', 'danger')
                return render_template('admin/login.html', form=form)

            login_user(user, remember=form.remember_me.data)
            flash(f'Selamat datang kembali, {user.full_name}!', 'success')
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('admin.dashboard')
            return redirect(next_page)
        else:
            flash('Kredensial login tidak cocok. Periksa username dan kata sandi Anda.', 'danger')

    return render_template('admin/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah berhasil keluar dari sistem dashboard.', 'info')
    return redirect(url_for('auth.login'))


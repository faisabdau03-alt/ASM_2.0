import os
from flask import Flask, render_template
from config import config
from app.extensions import db, migrate, login_manager, csrf


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    # Ensure instance and upload folders exist safely
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        for sub in ['fleets', 'services', 'galleries', 'testimonials']:
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], sub), exist_ok=True)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/404.html', message='Akses Ditolak'), 403

    return app


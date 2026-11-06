import os
from app import create_app
from app.extensions import db
from app.models import User
from seed import seed_data

app = create_app(os.environ.get('FLASK_ENV', 'development'))


def auto_init_database():
    """Ensure database tables and initial seed data exist before first request."""
    with app.app_context():
        # Create instance dir
        os.makedirs(app.instance_path, exist_ok=True)
        # Create tables
        db.create_all()
        # Check if admin user exists; if not, run seed
        if not User.query.filter_by(username='admin').first():
            print("[AUTO-INIT] Menginisialisasi basis data dan data demonstrasi awal...")
            seed_data()
            print("[AUTO-INIT] Inisialisasi selesai!")


if __name__ == '__main__':
    auto_init_database()
    # Run locally on 127.0.0.1:5000
    app.run(host='127.0.0.1', port=5000, debug=True)


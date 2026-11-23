import os
import sys
import traceback
from app import create_app
from app.extensions import db

app = create_app(os.environ.get('FLASK_ENV', 'development'))

_db_initialized = False


def auto_init_database():
    """Ensure database tables and initial seed data exist safely."""
    global _db_initialized
    if _db_initialized:
        return
    try:
        with app.app_context():
            if hasattr(app, 'instance_path'):
                try:
                    os.makedirs(app.instance_path, exist_ok=True)
                except OSError:
                    pass
            db.create_all()
            from app.models import User
            try:
                if not User.query.filter_by(username='admin').first():
                    print("[AUTO-INIT] Menginisialisasi basis data dan data demonstrasi awal...")
                    from seed import seed_data
                    seed_data(app)
                    print("[AUTO-INIT] Inisialisasi selesai!")
                _db_initialized = True
            except Exception as e:
                print(f"[AUTO-INIT NOTICE] Gagal memverifikasi user admin: {e}", file=sys.stderr)
    except Exception as err:
        print(f"[AUTO-INIT ERROR] {err}\n{traceback.format_exc()}", file=sys.stderr)


# Run initialization on import so it works on both local and serverless (Vercel)
auto_init_database()


@app.before_request
def ensure_db_on_request():
    """Safety check for serverless environments where cold-start import might defer init."""
    global _db_initialized
    if not _db_initialized:
        auto_init_database()


if __name__ == '__main__':
    # Run locally on 127.0.0.1:5000
    app.run(host='127.0.0.1', port=5000, debug=True)


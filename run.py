import os
import sys
import traceback

_import_error = None
flask_app = None

try:
    from app import create_app
    from app.extensions import db

    env_name = 'production' if os.environ.get('VERCEL') else os.environ.get('FLASK_ENV', 'development')
    flask_app = create_app(env_name)

    _db_initialized = False

    def auto_init_database():
        """Ensure database tables and initial seed data exist safely."""
        global _db_initialized
        if _db_initialized:
            return
        try:
            with flask_app.app_context():
                if hasattr(flask_app, 'instance_path'):
                    try:
                        os.makedirs(flask_app.instance_path, exist_ok=True)
                    except OSError:
                        pass
                db.create_all()
                from app.models import User
                try:
                    if not User.query.filter_by(username='admin').first():
                        print("[AUTO-INIT] Menginisialisasi basis data dan data demonstrasi awal...")
                        from seed import seed_data
                        seed_data(flask_app)
                        print("[AUTO-INIT] Inisialisasi selesai!")
                    _db_initialized = True
                except Exception as e:
                    print(f"[AUTO-INIT NOTICE] Gagal memverifikasi user admin: {e}", file=sys.stderr)
        except Exception as err:
            print(f"[AUTO-INIT ERROR] {err}\n{traceback.format_exc()}", file=sys.stderr)

    auto_init_database()

    @flask_app.before_request
    def ensure_db_on_request():
        global _db_initialized
        if not _db_initialized:
            auto_init_database()

except Exception as e:
    _import_error = traceback.format_exc()
    print(f"[IMPORT EXCEPTION] {_import_error}", file=sys.stderr)


class WSGIWrapper:
    def __init__(self, app_instance, err):
        self.app_instance = app_instance
        self.err = err

    def __call__(self, environ, start_response):
        if self.err:
            start_response('200 OK', [('Content-Type', 'text/plain; charset=utf-8')])
            return [f"=== SERVERLESS STARTUP IMPORT ERROR ===\n\n{self.err}".encode('utf-8')]
        try:
            return self.app_instance(environ, start_response)
        except Exception:
            tb = traceback.format_exc()
            print(f"[RUNTIME EXCEPTION] {tb}", file=sys.stderr)
            start_response('200 OK', [('Content-Type', 'text/plain; charset=utf-8')])
            return [f"=== SERVERLESS RUNTIME ERROR ===\n\n{tb}".encode('utf-8')]


app = WSGIWrapper(flask_app, _import_error)


if __name__ == '__main__':
    if flask_app:
        flask_app.run(host='127.0.0.1', port=5000, debug=True)


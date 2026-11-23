import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def is_serverless_env():
    """Detect if the application is running in a serverless/read-only environment like Vercel."""
    if any(os.environ.get(k) for k in ['VERCEL', 'VERCEL_ENV', 'AWS_LAMBDA_FUNCTION_NAME', 'LAMBDA_TASK_ROOT']):
        return True
    # Test if basedir is writable
    test_file = os.path.join(basedir, '.write_test')
    try:
        with open(test_file, 'w') as f:
            f.write('1')
        os.remove(test_file)
        return False
    except (OSError, IOError, PermissionError):
        return True


class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asm-secret-super-secure-key-v2-kebumen-transport-2026'
    
    IS_SERVERLESS = is_serverless_env()

    # Database
    if IS_SERVERLESS and not os.environ.get('DATABASE_URL'):
        db_path = '/tmp/asm_transport.db'
    else:
        db_path = os.path.join(basedir, 'instance', 'asm_transport.db')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{db_path}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads
    if IS_SERVERLESS:
        UPLOAD_FOLDER = '/tmp/uploads'
    else:
        UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 Megabytes max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

    # Admin Defaults for Seed
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@asmtransport.com')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'adminasm2026')
    ADMIN_FULL_NAME = os.environ.get('ADMIN_FULL_NAME', 'Administrator ASM')

    # WhatsApp and Contact defaults
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '62882005363151')
    OFFICE_PHONE = os.environ.get('OFFICE_PHONE', '(0287) 381-000')
    OFFICE_EMAIL = os.environ.get('OFFICE_EMAIL', 'info@asmtransport.id')
    COMPANY_ADDRESS = os.environ.get('COMPANY_ADDRESS', 'Jl. Raya Kebumen - Purworejo KM. 5, Kebumen, Jawa Tengah 54311')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


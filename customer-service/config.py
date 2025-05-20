class DevelopmentConfig:
    DEBUG = True
    TESTING = True  # Enable testing mode for test runs
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Use in-memory DB for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "dev-secret"
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing APIs
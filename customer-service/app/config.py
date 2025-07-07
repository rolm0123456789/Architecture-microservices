# app/config.py
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "b7e2e2e1e7e6c1a2b3d4f5c6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
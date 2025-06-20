#!/bin/sh
# Entrypoint script to initialize the SQLite DB and run the Flask app

# Set up the database if it doesn't exist
python -c "from app import create_app, db; app = create_app('app.config.DevelopmentConfig'); ctx = app.app_context(); ctx.push(); db.create_all(); ctx.pop()"

# Start the Flask app
exec flask run --host=0.0.0.0 --port=5000

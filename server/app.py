from flask import Flask
from flask_migrate import Migrate

from models import db

# Create the Flask application
app = Flask(__name__)

# Configure the database (SQLite for this project)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Disable modification tracking (saves memory and avoids warnings)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with Flask app
db.init_app(app)

# Initialize Flask-Migrate for handling database migrations
migrate = Migrate(app, db)

# Simple test route to confirm the server is running
@app.route('/')
def home():
    return {'message': 'Workout API is running'}

# Run the application
if __name__ == '__main__':
    app.run(port=5555, debug=True)
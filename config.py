import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

# Create a Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app
app = connex_app.app

# Configure SQLAlchemy part of the app instance
app.config['SQLALCHEMY_ECHO'] = True    # This causes SQLAlchemy to echo SQL statements it executes to the console
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'people.db')  # This tells SQLAlchemy to
# use SQLite as the database, and a file named people.db in the current directory as the database file.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy database instance
db = SQLAlchemy(app)
# This initializes SQLAlchemy by passing the app configuration information just set. The db variable is what’s imported
# into the build_database.py program to give it access to SQLAlchemy and the database. It will serve the same purpose
# in the server.py program and people.py module.

# Initialize Marshmallow
ma = Marshmallow(app)
# This initializes Marshmallow and allows it to introspect the SQLAlchemy components attached to the app. This is why
# Marshmallow is initialized after SQLAlchemy.
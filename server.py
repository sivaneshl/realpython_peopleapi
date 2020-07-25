from flask import render_template
import config

# Create the application instance
# app = Flask(__name__, template_folder='templates')
# Create the application instance using Connexion rather than Flask. Internally, the
# Flask app is still created, but it now has additional functionality added to it.
# app = connexion.App(__name__, specification_dir='./')

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api('swagger.yml')

# Create a URL route in our application for "/"
@connex_app.route('/')
def home():
    """
    This function just responds to the browser URL
    localhost:5000
    :return:    the rendered template home.html
    """
    return render_template('home.html')


# If we are running in stand alone mode, run the application
if __name__ == '__main__':
    connex_app.run(debug=True)

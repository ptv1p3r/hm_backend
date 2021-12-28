from datetime import datetime
from flask import Flask
import datetime
from app.templates.consultas.consultas import consultas
from app.templates.utentes.utentes import utentes

app = Flask(__name__)

# Configurations
app.config.from_object('config')


@app.route("/")
def index():
    return "Welcome to Hospitality Manager API v1 - " + '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())


@app.route('/isalive', methods=['GET'])
def is_Alive():
    return "Success", 201


# regista endpoint de utentes
app.register_blueprint(utentes)

# regista endpoint de consultas
app.register_blueprint(consultas)

# # Sample HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404

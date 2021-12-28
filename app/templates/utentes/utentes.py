from flask import Blueprint, render_template

utentes = Blueprint('utentes', __name__, template_folder='templates')


# create new user account
@utentes.route("/v1/utente/account/create", methods=["POST"])
def createAccount():
    dbconnection = None


# list all users
@utentes.route("/v1/utentes/list", methods=["GET"])
def getUtentes():
    dbconnection = None


# get user from db from id
@utentes.route('/v1/utente/', defaults={'id': None})
@utentes.route("/v1/utente/<int:id>", methods=["GET"])
def getUser(id):
    dbconnection = None

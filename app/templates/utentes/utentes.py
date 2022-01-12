import psycopg2
from flask import Blueprint, render_template, jsonify

from config import DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT

utentes = Blueprint('utentes', __name__, template_folder='templates')


# create new consulta
@utentes.route("/v1/utentes/create", methods=["POST"])
def createUtentes():
    dbconnection = None


# delete consulta
@utentes.route('/v1/utentes/delete/', defaults={'id': None})
@utentes.route("/v1/utentes/delete/<int:id>", methods=["DELETE"])
def deleteUtentes(id):
    dbconnection = None


# list all consultas
@utentes.route("/v1/utentes/list", methods=["GET"])
def getUtentes():
    dbconnection = None

    dbconnection = psycopg2.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        database=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD)

    # create a cursor
    cur = dbconnection.cursor()

    # execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)

    # close the communication with the PostgreSQL
    cur.close()

    return jsonify({'ok': False, 'message': db_version}), 200


# get user from db from id
@utentes.route('/v1/utentes/', defaults={'id': None})
@utentes.route("/v1/utentes/<int:id>", methods=["GET"])
def getUtentesById(id):
    dbconnection = None

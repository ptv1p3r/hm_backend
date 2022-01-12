import psycopg2
from flask import Blueprint, render_template, jsonify

from config import DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT

consultas = Blueprint('consultas', __name__, template_folder='templates')


# create new consulta
@consultas.route("/v1/consultas/create", methods=["POST"])
def createConsulta():
    dbconnection = None


# delete consulta
@consultas.route('/v1/consultas/delete/', defaults={'id': None})
@consultas.route("/v1/consultas/delete/<int:id>", methods=["DELETE"])
def deleteConsulta(id):
    dbconnection = None


# list all consultas
@consultas.route("/v1/consultas/list", methods=["GET"])
def getConsultas():
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
@consultas.route('/v1/consultas/', defaults={'id': None})
@consultas.route("/v1/consultas/<int:id>", methods=["GET"])
def getConsultaById(id):
    dbconnection = None

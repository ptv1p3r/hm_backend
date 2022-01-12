import psycopg2
from flask import Blueprint, render_template, jsonify

from config import DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT

medicos = Blueprint('medicos', __name__, template_folder='templates')


# create new consulta
@medicos.route("/v1/medicos/create", methods=["POST"])
def createMedicos():
    dbconnection = None


# delete consulta
@medicos.route('/v1/medicos/delete/', defaults={'id': None})
@medicos.route("/v1/medicos/delete/<int:id>", methods=["DELETE"])
def deleteMedicos(id):
    dbconnection = None


# list all consultas
@medicos.route("/v1/medicos/list", methods=["GET"])
def getMedicos():
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
@medicos.route('/v1/medicos/', defaults={'id': None})
@medicos.route("/v1/medicos/<int:id>", methods=["GET"])
def getMedicosById(id):
    dbconnection = None

import psycopg2
from flask import Blueprint, render_template, jsonify

consultas = Blueprint('consultas', __name__, template_folder='templates')


# create new user account
@consultas.route("/v1/consultas/account/create", methods=["POST"])
def createAccount():
    dbconnection = None


# list all users
@consultas.route("/v1/consultas/list", methods=["GET"])
def getConsultas():
    dbconnection = None
    conn = psycopg2.connect(
        host="192.168.2.14",
        database="hm_data",
        user="postgres",
        password="admin")

    # create a cursor
    cur = conn.cursor()

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
def getUser(id):
    dbconnection = None

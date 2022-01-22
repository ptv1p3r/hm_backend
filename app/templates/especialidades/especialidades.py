import psycopg2
from flask import Blueprint, jsonify, request
from datetime import datetime
from config import DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT

especialidades = Blueprint('especialidades', __name__, template_folder='templates')


# create new especialidades
@especialidades.route("/v1/especialidades/create", methods=["POST"])
def createEspecialidades():
    dbconnection = None
    cursor = None
    userExists = False
    now = datetime.now()

    data = request.get_json()
    data_name = data.get('Nome')
    data_datecreate = now.strftime('%Y-%m-%d %H:%M:%S')

    if data_name is not None:
        try:
            dbconnection = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT,
                                            database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
            # dbconnection = psycopg2.connect(host="127.0.0.1", port=DATABASE_PORT,
            #                                 database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
            cursor = dbconnection.cursor()

            # check if user exists by nome
            cursor.execute("SELECT id, nome FROM especialidades WHERE nome = %s", (data_name,))
            cursor.fetchone()

            # if cursor.rowcount == -1:
            if cursor.rowcount == 0:
                # user not found
                sql = "INSERT INTO especialidades (nome, datecreate, datemodify) " \
                      "VALUES (%s, %s, %s)"
                val = [data_name, now, now]

                cursor.execute(sql, val)
                dbconnection.commit()
            else:
                userExists = True

        except psycopg2.Error as err:
            dbconnection.rollback()

        finally:
            cursor.close()
            dbconnection.close()

        if userExists:
            return jsonify({'ok': True, 'message': 'Especialidade exists, not added'}), 200
        else:
            return jsonify({'ok': True, 'message': 'Especialidade added successfully'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Missing especialidade data'}), 400


# delete especialidade by id
@especialidades.route('/v1/especialidades/delete/', defaults={'id': None})
@especialidades.route("/v1/especialidades/delete/<int:id>", methods=["DELETE"])
def deleteEspecialidadeById(id):
    dbconnection = None
    cursor = None
    rowcount = 0

    if id is not None:
        try:
            dbconnection = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT,
                                            database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)

            # dbconnection = psycopg2.connect(host="127.0.0.1", port=DATABASE_PORT,
            #                                 database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)

            cursor = dbconnection.cursor()
            cursor.execute("DELETE FROM especialidades WHERE ID = %s", (int(id),))
            rowcount = cursor.rowcount
            dbconnection.commit()

        except psycopg2.Error as err:
            dbconnection.rollback()

        finally:
            cursor.close()
            dbconnection.close()

        if rowcount > 0:
            return jsonify({'ok': True, 'message': 'Especialidade deleted successfully'}), 200
        else:
            return jsonify({'ok': True, 'message': 'Especialidade not deleted'}), 200

    else:
        return jsonify({'ok': False, 'message': 'Missing Especialidade data'}), 400


# list all especialidades
@especialidades.route("/v1/especialidades/list", methods=["GET"])
def getEspecialidades():
    dbconnection = None
    cursor = None
    serializedData = []
    rowcount = 0
    now = datetime.now()

    try:
        dbconnection = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT,
                                        database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)

        # dbconnection = psycopg2.connect(host="127.0.0.1", port=DATABASE_PORT,
        #                                 database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)

        cursor = dbconnection.cursor()
        cursor.execute("SELECT id, nome, "
                       "to_char(datecreate, 'YYYY-MM-DD HH24:MI:SS') AS DateCreate, "
                       "to_char(datemodify, 'YYYY-MM-DD HH24:MI:SS') AS DateModify "
                       "FROM especialidades")
        datareturn = cursor.fetchall()
        rowcount = cursor.rowcount

        serializedData = [dict(zip([key[0] for key in cursor.description], row)) for row in datareturn]

    except psycopg2.Error as err:
        print(err)
    finally:
        cursor.close()
        dbconnection.close()

    if rowcount > 0:
        return jsonify({'ok': True, 'data': serializedData, "count": rowcount}), 200
    else:
        return jsonify({'ok': True, 'message': 'No especialidades found'}), 404


# get especialidade by id
@especialidades.route('/v1/especialidades/', defaults={'id': None})
@especialidades.route("/v1/especialidades/<int:id>", methods=["GET"])
def getEspecialidadeById(id):
    dbconnection = None
    cursor = None
    serializedData = []
    rowcount = 0

    if id is not None:
        try:
            dbconnection = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT,
                                            database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)

            # dbconnection = psycopg2.connect(host="127.0.0.1", port=DATABASE_PORT,
            #                                 database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
            cursor = dbconnection.cursor()
            cursor.execute("SELECT id, nome, "
                           "to_char(datecreate, 'YYYY-MM-DD HH24:MI:SS') AS DateCreate, "
                           "to_char(datemodify, 'YYYY-MM-DD HH24:MI:SS') AS DateModify "
                           "FROM especialidades WHERE id = %s", (int(id),))
            datareturn = cursor.fetchall()
            rowcount = cursor.rowcount

            serializedData = [dict(zip([key[0] for key in cursor.description], row)) for row in datareturn]

        except psycopg2.Error as err:
            print(str(err))

        finally:
            cursor.close()
            dbconnection.close()

        if rowcount > 0:
            return jsonify({'ok': True, 'data': serializedData}), 200
        else:
            return jsonify({'ok': True, 'message': 'Especialidade not found'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Missing parameters'}), 400


# update especialidade by id
@especialidades.route('/v1/especialidades/update/', defaults={'id': None})
@especialidades.route("/v1/especialidades/update/<int:id>", methods=["POST"])
def updateEspecialidadeById(id):
    dbconnection = None
    cursor = None
    rowcount = 0
    now = datetime.now()

    data = request.get_json()
    data_name = data.get('Nome')

    if id is not None and data_name is not None:
        try:
            dbconnection = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT,
                                            database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)

            # dbconnection = psycopg2.connect(host="127.0.0.1", port=DATABASE_PORT,
            #                                 database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
            cursor = dbconnection.cursor()
            cursor.execute("UPDATE especialidades SET nome = %s, datemodify = %s "
                           "WHERE id = %s",
                           (data_name, now, int(id)))
            rowcount = cursor.rowcount
            dbconnection.commit()

        except psycopg2.Error as err:
            print(str(err))

        finally:
            cursor.close()
            dbconnection.close()

        if rowcount > 0:
            return jsonify({'ok': True, 'message': 'Especialidade updated successfully'}), 200
        else:
            return jsonify({'ok': True, 'message': 'Especialidade not updated'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Missing especialidade data'}), 400

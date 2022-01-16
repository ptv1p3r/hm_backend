import psycopg2
from flask import Blueprint, jsonify, request
from datetime import datetime
from config import DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT

consultas = Blueprint('consultas', __name__, template_folder='templates')


# create new consulta
@consultas.route("/v1/consultas/create", methods=["POST"])
def createConsulta():
    dbconnection = None
    cursor = None
    userExists = False
    now = datetime.now()

    data = request.get_json()
    data_descricao = data.get('Descricao')
    data_utenteId = data.get('IdUtente')
    data_medicoId = data.get('IdMedico')
    data_consulta = datetime.strptime(data.get('DataConsulta'), '%Y-%m-%d %H:%M:%S').date()
    # data_datecreate = now.strftime('%Y-%m-%d %H:%M:%S')
    # data_datecreate = now

    if data_descricao is not None and data_utenteId is not None and data_medicoId is not None and data_consulta is not None:
        try:
            dbconnection = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT,
                                            database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
            # dbconnection = psycopg2.connect(host="127.0.0.1", port=DATABASE_PORT,
            #                                 database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
            cursor = dbconnection.cursor()

            # check if consulta exists
            cursor.execute("SELECT id FROM consultas WHERE id_medico = %s AND id_utente = %s AND data = %s",
                           (int(data_medicoId), int(data_utenteId), data_consulta))
            cursor.fetchone()

            # if cursor.rowcount == -1:
            if cursor.rowcount == 0:
                # consulta not found
                sql = "INSERT INTO consultas (descricao, id_medico, id_utente, data, datecreate, datemodify) " \
                      "VALUES (%s, %s, %s, %s, %s, %s)"
                val = [data_descricao, int(data_medicoId), int(data_utenteId), data_consulta, now, now]

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
            return jsonify({'ok': True, 'message': 'Consulta exists, not added'}), 200
        else:
            return jsonify({'ok': True, 'message': 'Consulta added successfully'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Missing consulta data'}), 400


# delete consulta by id
@consultas.route('/v1/consultas/delete/', defaults={'id': None})
@consultas.route("/v1/consultas/delete/<int:id>", methods=["DELETE"])
def deleteConsultaById(id):
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
            cursor.execute("DELETE FROM consultas WHERE ID = %s", (int(id),))
            rowcount = cursor.rowcount
            dbconnection.commit()

        except psycopg2.Error as err:
            dbconnection.rollback()

        finally:
            cursor.close()
            dbconnection.close()

        if rowcount > 0:
            return jsonify({'ok': True, 'message': 'Consulta deleted successfully'}), 200
        else:
            return jsonify({'ok': True, 'message': 'Consulta not deleted'}), 200

    else:
        return jsonify({'ok': False, 'message': 'Missing consulta data'}), 400


# list all consultas
@consultas.route("/v1/consultas/list", methods=["GET"])
def getConsultas():
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
        cursor.execute("SELECT id, descricao, id_medico, id_utente, "
                       "to_char(data, 'YYYY-MM-DD HH24:MI:SS') AS DataConsulta, to_char(datecreate, 'YYYY-MM-DD HH24:MI:SS') AS DateCreate, "
                       "to_char(datemodify, 'YYYY-MM-DD HH24:MI:SS') AS DateModify "
                       "FROM consultas")
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
        return jsonify({'ok': True, 'message': 'No consultas found'}), 404


# get consulta by id
@consultas.route('/v1/consultas/', defaults={'id': None})
@consultas.route("/v1/consultas/<int:id>", methods=["GET"])
def getConsultaById(id):
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
            cursor.execute("SELECT id, descricao, id_medico, id_utente, "
                           "to_char(data, 'YYYY-MM-DD HH24:MI:SS') AS DataConsulta, to_char(datecreate, 'YYYY-MM-DD HH24:MI:SS') AS DateCreate, "
                           "to_char(datemodify, 'YYYY-MM-DD HH24:MI:SS') AS DateModify "
                           "FROM consultas WHERE id = %s", (int(id),))
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
            return jsonify({'ok': True, 'message': 'Consulta not found'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Missing parameters'}), 400


# update consulta by id
@consultas.route('/v1/consultas/update/', defaults={'id': None})
@consultas.route("/v1/consultas/update/<int:id>", methods=["POST"])
def updateConsultaById(id):
    dbconnection = None
    cursor = None
    rowcount = 0
    now = datetime.now()

    data = request.get_json()
    data_descricao = data.get('Descricao')
    data_utenteId = data.get('IdUtente')
    data_medicoId = data.get('IdMedico')
    data_consulta = datetime.strptime(data.get('DataConsulta'), '%Y-%m-%d %H:%M:%S').date()

    if id is not None and data_descricao is not None and data_utenteId is not None and data_medicoId is not None and data_consulta is not None:
        try:
            dbconnection = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT,
                                            database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)

            # dbconnection = psycopg2.connect(host="127.0.0.1", port=DATABASE_PORT,
            #                                 database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
            cursor = dbconnection.cursor()
            cursor.execute(
                "UPDATE consultas SET descricao = %s, id_medico = %s, id_utente = %s, data = %s, datemodify = %s "
                "WHERE id = %s",
                (data_descricao, int(data_medicoId), int(data_utenteId), data_consulta, now, int(id)))
            rowcount = cursor.rowcount
            dbconnection.commit()

        except psycopg2.Error as err:
            print(str(err))

        finally:
            cursor.close()
            dbconnection.close()

        if rowcount > 0:
            return jsonify({'ok': True, 'message': 'Consulta updated successfully'}), 200
        else:
            return jsonify({'ok': True, 'message': 'Consulta not updated'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Missing consulta data'}), 400

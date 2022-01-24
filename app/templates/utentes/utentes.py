import psycopg2
from flask import Blueprint, jsonify, request
from datetime import datetime
from config import DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT

utentes = Blueprint('utentes', __name__, template_folder='templates')


# create new utente
@utentes.route("/v1/utentes/create", methods=["POST"])
def createUtentes():
    dbconnection = None
    cursor = None
    userExists = False
    now = datetime.now()

    data = request.get_json()
    data_name = data.get('Nome')
    data_address = data.get('Morada')
    data_codpost = data.get('CodPostal')
    data_email = data.get('Email')
    data_nif = data.get('Nif')
    data_mobile = data.get('Telemovel')
    data_nmrutente = data.get('NrUtente')
    data_datebirth = datetime.strptime(data.get('DataNascimento'), '%Y-%m-%d').date()
    data_datecreate = now.strftime('%Y-%m-%d %H:%M:%S')
    # data_datecreate = now

    if data_name is not None and data_email is not None:
        try:
            dbconnection = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT,
                                            database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
            # dbconnection = psycopg2.connect(host="127.0.0.1", port=DATABASE_PORT,
            #                                 database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
            cursor = dbconnection.cursor()

            # check if user exists by email
            cursor.execute("SELECT id, email FROM medicos WHERE email = %s", (data_email,))
            cursor.fetchone()

            if cursor.rowcount == 0:
                # user not found
                sql = "INSERT INTO utentes (nome, morada, email, codpost, nif, nmr_utente, telemovel, data_nascimento, datecreate, datemodify) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = [data_name, data_address, data_email, data_codpost, data_nif, data_nmrutente, data_mobile,
                       data_datebirth, now, now]

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
            return jsonify({'ok': True, 'message': 'Utente exists, not added'}), 200
        else:
            return jsonify({'ok': True, 'message': 'Utente added successfully'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Missing utente data'}), 400


# delete utente by id
@utentes.route('/v1/utentes/delete/', defaults={'id': None})
@utentes.route("/v1/utentes/delete/<int:id>", methods=["DELETE"])
def deleteUtenteById(id):
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
            cursor.execute("DELETE FROM utentes WHERE ID = %s", (int(id),))
            rowcount = cursor.rowcount
            dbconnection.commit()

        except psycopg2.Error as err:
            dbconnection.rollback()

        finally:
            cursor.close()
            dbconnection.close()

        if rowcount > 0:
            return jsonify({'ok': True, 'message': 'Utente deleted successfully'}), 200
        else:
            return jsonify({'ok': True, 'message': 'Utente not deleted'}), 200

    else:
        return jsonify({'ok': False, 'message': 'Missing utente data'}), 400


# list all utentes
@utentes.route("/v1/utentes/list", methods=["GET"])
def getUtentes():
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
        cursor.execute("SELECT id, nome, morada, email, codpost, nif, nmr_utente, telemovel, "
                       "to_char(data_nascimento, 'YYYY-MM-DD') AS DataNascimento, to_char(datecreate, 'YYYY-MM-DD HH24:MI:SS') AS DateCreate, "
                       "to_char(datemodify, 'YYYY-MM-DD HH24:MI:SS') AS DateModify "
                       "FROM utentes")
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
        return jsonify({'ok': True, 'message': 'No utentes found'}), 404


# get utente by id
@utentes.route('/v1/utentes/', defaults={'id': None})
@utentes.route("/v1/utentes/<int:id>", methods=["GET"])
def getUtentesById(id):
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
            cursor.execute("SELECT id, nome, morada, email, codpost, nif, nmr_utente, telemovel, "
                           "to_char(data_nascimento, 'YYYY-MM-DD') AS DataNascimento, to_char(datecreate, 'YYYY-MM-DD HH24:MI:SS') AS DateCreate, "
                           "to_char(datemodify, 'YYYY-MM-DD HH24:MI:SS') AS DateModify "
                           "FROM utentes WHERE id = %s", (int(id),))
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
            return jsonify({'ok': True, 'message': 'Utente not found'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Missing parameters'}), 400


# update utente by id
@utentes.route('/v1/utentes/update/', defaults={'id': None})
@utentes.route("/v1/utentes/update/<int:id>", methods=["POST"])
def updateUtenteById(id):
    dbconnection = None
    cursor = None
    rowcount = 0
    now = datetime.now()

    data = request.get_json()
    data_name = data.get('Nome')
    data_address = data.get('Morada')
    data_codpost = data.get('CodPostal')
    data_email = data.get('Email')
    data_nif = data.get('Nif')
    data_mobile = data.get('Telemovel')
    data_nmrutente = data.get('NrUtente')
    data_datebirth = datetime.strptime(data.get('DataNascimento'), '%Y-%m-%d').date()
    data_datecreate = now.strftime('%Y-%m-%d %H:%M:%S')
    # data_datecreate = now

    if id is not None and data_name is not None and data_address is not None and data_codpost is not None and data_email is not None and data_nif is not None \
            and data_mobile is not None and data_nmrutente is not None and data_datebirth is not None:
        try:
            dbconnection = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT,
                                            database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)

            # dbconnection = psycopg2.connect(host="127.0.0.1", port=DATABASE_PORT,
            #                                 database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
            cursor = dbconnection.cursor()
            cursor.execute("UPDATE utentes SET nome = %s, morada = %s, email = %s, "
                           "codpost = %s, nif = %s, nmr_utente = %s, telemovel = %s, data_nascimento = %s, datemodify = %s "
                           "WHERE id = %s",
                           (data_name, data_address, data_email, data_codpost, data_nif, data_nmrutente, data_mobile,
                            data_datebirth, now, int(id)))
            rowcount = cursor.rowcount
            dbconnection.commit()

        except psycopg2.Error as err:
            print(str(err))

        finally:
            cursor.close()
            dbconnection.close()

        if rowcount > 0:
            return jsonify({'ok': True, 'message': 'Utente updated successfully'}), 200
        else:
            return jsonify({'ok': True, 'message': 'Utente not updated'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Missing user data'}), 400

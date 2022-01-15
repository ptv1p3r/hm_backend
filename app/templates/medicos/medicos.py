import psycopg2
from flask import Blueprint, jsonify, request
from datetime import datetime
from config import DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT

medicos = Blueprint('medicos', __name__, template_folder='templates')


# create new medico
@medicos.route("/v1/medicos/create", methods=["POST"])
def createMedicos():
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
    data_cedprof = data.get('C.Profissional')
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

            # if cursor.rowcount == -1:
            if cursor.rowcount == 0:
                # user not found
                sql = "INSERT INTO medicos (nome, morada, email, codpost, nif, ced_profissional, telemovel, data_nascimento, datecreate, datemodify) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = [data_name, data_address, data_email, data_codpost, data_nif, data_cedprof, data_mobile,
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
            return jsonify({'ok': True, 'message': 'Doctor exists, not added'}), 200
        else:
            return jsonify({'ok': True, 'message': 'Doctor added successfully'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Missing doctor data'}), 400


# delete medico by id
@medicos.route('/v1/medicos/delete/', defaults={'id': None})
@medicos.route("/v1/medicos/delete/<int:id>", methods=["DELETE"])
def deleteMedicoById(id):
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
            cursor.execute("DELETE FROM medicos WHERE ID = %s", (int(id),))
            rowcount = cursor.rowcount
            dbconnection.commit()

        except psycopg2.connector.Error as err:
            dbconnection.rollback()

        finally:
            cursor.close()
            dbconnection.close()

        if rowcount > 0:
            return jsonify({'ok': True, 'message': 'Doctor deleted successfully'}), 200
        else:
            return jsonify({'ok': True, 'message': 'Doctor not deleted'}), 200

    else:
        return jsonify({'ok': False, 'message': 'Missing doctor data'}), 400


# list all medicos
@medicos.route("/v1/medicos/list", methods=["GET"])
def getMedicos():
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
        cursor.execute("SELECT id, nome, morada, email, codpost, nif, "
                       "to_char(data_nascimento, 'YYYY-MM-DD') AS DataNascimento, to_char(datecreate, 'YYYY-MM-DD HH24:MI:SS') AS DateCreate, "
                       "to_char(datemodify, 'YYYY-MM-DD HH24:MI:SS') AS DateModify "
                       "FROM medicos")
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
        return jsonify({'ok': True, 'message': 'No doctors found'}), 404


# get medico by id
@medicos.route('/v1/medicos/', defaults={'id': None})
@medicos.route("/v1/medicos/<int:id>", methods=["GET"])
def getMedicosById(id):
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
            cursor.execute("SELECT id, nome, morada, email, codpost, nif, "
                           "to_char(data_nascimento, 'YYYY-MM-DD') AS DataNascimento, to_char(datecreate, 'YYYY-MM-DD HH24:MI:SS') AS DateCreate, "
                           "to_char(datemodify, 'YYYY-MM-DD HH24:MI:SS') AS DateModify "
                           "FROM medicos WHERE id = %s", (int(id),))
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
            return jsonify({'ok': True, 'message': 'Doctor not found'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Missing parameters'}), 400


# update medico by id
@medicos.route('/v1/medicos/update/', defaults={'id': None})
@medicos.route("/v1/medicos/update/<int:id>", methods=["POST"])
def updateMedicoById(id):
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
    data_cedprof = data.get('C.Profissional')
    data_datebirth = datetime.strptime(data.get('DataNascimento'), '%Y-%m-%d').date()
    data_datecreate = now.strftime('%Y-%m-%d %H:%M:%S')
    # data_datecreate = now

    if id is not None and data_name is not None and data_address is not None and data_codpost is not None and data_email is not None and data_nif is not None \
            and data_mobile is not None and data_cedprof is not None and data_datebirth is not None:
        try:
            dbconnection = psycopg2.connect(host=DATABASE_HOST, port=DATABASE_PORT,
                                            database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)

            # dbconnection = psycopg2.connect(host="127.0.0.1", port=DATABASE_PORT,
            #                                 database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD)
            cursor = dbconnection.cursor()
            cursor.execute("UPDATE medicos SET nome=%s, morada=%s, email=%s, "
                           "codpost=%s, nif=%s, ced_profissional=%s, telemovel=%s, data_nascimento=%s, datemodify=%s "
                           "WHERE id = %s",
                           (data_name, data_address, data_email, data_codpost, data_nif, data_cedprof, data_mobile,
                            data_datebirth, now, int(id)))
            rowcount = cursor.rowcount
            dbconnection.commit()

        except psycopg2.Error as err:
            print(str(err))

        finally:
            cursor.close()
            dbconnection.close()

        if rowcount > 0:
            return jsonify({'ok': True, 'message': 'Doctor updated successfully'}), 200
        else:
            return jsonify({'ok': True, 'message': 'Doctor not updated'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Missing user data'}), 400

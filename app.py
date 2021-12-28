from app import app
from gevent.pywsgi import WSGIServer
from config import SERVER_MODE_DEV, SERVER_PORT

# inicia api em modo dev/prod
if __name__ == '__main__':

    if SERVER_MODE_DEV:
        # Debug/Development
        # app.run(debug=True, host="127.0.0.1", port=SERVER_PORT, use_reloader=False)
        app.run(debug=True, host="0.0.0.0", port=SERVER_PORT)
    else:
        # Production
        http_server = WSGIServer(('0.0.0.0', SERVER_PORT), app)
        # http_server = WSGIServer(('', SERVER_PORT), app, certfile='/etc/letsencrypt/live/vipernet.ddns.net/fullchain.pem', keyfile='/etc/letsencrypt/live/vipernet.ddns.net/privkey.pem')
        http_server.serve_forever()

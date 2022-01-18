from flask import Flask,request, jsonify, make_response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import uuid
import jwt
from functools import wraps
from event import ScanEvent
from datetime import timedelta
from event import QRInvalid,PersonUnknown,DeadTime,UnknownState,UnableToWrite,UnknownError,DatabaseDisconnect
import logging

app = Flask(__name__)
app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_COOKIE_SECURE"] = True
jwt = JWTManager(app)

logger = logging.getLogger('ScanEvent')
logger.debug('Logger for ScanEvent was initialised')


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route('/booking', methods=['POST'])
@jwt_required()
def booking(): 
    if request.method == 'POST': 
         #Removing all special chars
         personalHash = ''.join(e for e in request.args.get('hash') if e.isalnum())
         try:
            logger.debug(f'Received the folloing hash: {personalHash}')
            currentEvent = ScanEvent(personalHash)
            currentEvent.check_validity()
            currentEvent.get_personal_number()
            currentEvent.check_dead_time()
            currentEvent.check_open_entries()
            if currentEvent.direction == "Dienstbeginn":
                     currentEvent.create_shift()
                     return jsonify({'type': 'Dienstbeginn', 'textMain':'KOMMEN', 'textSub': f'Hallo {currentEvent.vorname} {currentEvent.nachname}', 'mainLabel': 'Green', 'textColor': 'black'})
            elif currentEvent.direction == "Dienstende":
                     currentEvent.close_shift()
                     return jsonify({'type': 'Dienstende', 'textMain':'GEHEN', 'textSub': f'Danke {currentEvent.vorname} {currentEvent.nachname} - Dienstdauer: {currentEvent.shiftDurationHours}:{currentEvent.shiftDurationMinutes}', 'mainLabel': 'Yellow', 'textColor': 'black'})
            return jsonify({'message': 'Everything ok'})
         except QRInvalid as e:
            logger.warning(f'The following invalid QR Code was scanned: {personalHash}')
            logger.error('The following error occured: %s' % (e))
            return jsonify({'type': 'Error', 'textMain':'Ungültiger QR Code', 'textSub': '', 'mainLabel': 'Red', 'textColor': 'black'})
         except PersonUnknown as e:
            logger.warning(f'The scanned hash {personalHash} is not known in database')
            logger.error('The following error occured: %s' % (e))
            return jsonify({'type': 'Error', 'textMain':'Mitarbeiter Unbekannt', 'textSub': '', 'mainLabel': 'Red', 'textColor': 'black'})
         except DeadTime as e:
           logger.warning(f'Double scanning of {personalHash}')
           logger.error('The following error occured: %s' % (e))
           return jsonify({'type': 'Error', 'textMain':'Zeit bereits gebucht', 'textSub': '', 'mainLabel': 'Blue', 'textColor': 'black'})
         except UnknownError as e:
           logger.error('The following error occured: %s' % (e))
           return jsonify({'type': 'Error', 'textMain':'Unbekannter Fehler', 'textSub': '', 'mainLabel': 'Red', 'textColor': 'black'})
         except UnableToWrite as e:
           logger.error('The following error occured: %s' % (e))
           return jsonify({'type': 'Error', 'textMain':'Zeit konnte nicht verbucht werden', 'textSub': '', 'mainLabel': 'Red', 'textColor': 'black'})
         except DatabaseDisconnect as e:
           logger.error('The following error occured: %s' % (e))
           return jsonify({'type': 'Error', 'textMain':'Server offline, Scan gespeichert', 'textSub': '', 'mainLabel': 'Red', 'textColor': 'black'})
         except UnknownState as e:
           logger.error('The following error occured: %s' % (e))
           return jsonify({'type': 'Error', 'textMain':'Unbekannter Fehler', 'textSub': '', 'mainLabel': 'Red', 'textColor': 'black'})
         except Exception as e:
           logger.error('The following error occured: %s' % (e))
           return jsonify({'type': 'Error', 'textMain':'Unbekannter Fehler', 'textSub': '', 'mainLabel': 'Red', 'textColor': 'black'})


if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0", port=3000)
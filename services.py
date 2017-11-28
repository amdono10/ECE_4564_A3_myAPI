from flask import Flask, request, Response
import json
import pymongo
from bson import json_util
from bson.objectid import ObjectId
from functools import wraps
#from pymongo import Connection

### NEED TO UPDATE THIS FUNCTION FOR ACTUAL USERNAMES AND PASSWORDS
def check_auth(username, password):
    return username == 'admin' and password == 'secret'

def authenticate():
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate' : 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)

@app.route("/")
@requires_auth
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

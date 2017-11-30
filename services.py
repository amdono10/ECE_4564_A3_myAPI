from flask import Flask, request, Response, jsonify, abort
from flask_discoverer import Discoverer, advertise
import json
import pymongo
from bson import json_util
from bson.objectid import ObjectId
from functools import wraps
from pymongo import MongoClient

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

### TEMPORARY ARRAY OF DICTIONARIES FOR DB SIMULATION
### WILL NEED TO CHANGE THIS TO A MONGODB SOLUTION
grades = [
    {
        'id' : 1,
        'course' : u'Net Apps',
        'course number' : 4564,
        'grade percentage' : 100
    }
]

app = Flask(__name__)
discoverer = Discoverer(app)
mongoClient = MongoClient('localhost', 27017)
db = mongoClient.grades
collection = db.users

user_credentials = [{"username" : "Adam",
                     "password" : "secret"},
                    {"username" : "Brendan",
                     "password" : "secret"},
                    {"username" : "Brandon",
                     "password" : "secret"}]

userLib = db.libs
userLib.insert_many(user_credentials)

for i in userLib.find():
    user = i["username"]
    if user == "Adam" or user == "Brendan" or user == "Brandon":
        print(user)

def mongoToJson(data):
    """Convert Mongo objects to JSON"""
    return json.dumps(data,  default=json_util.default)


@app.route('/calculator/api/v1/grades', methods=['GET'])
@requires_auth
def get_grades():
    '''Route to get all grades for a student'''
    return jsonify({'grades': grades})

@app.route('/calculator/api/v1/grades/<int:class_id>', methods=['GET'])
@requires_auth
def get_grade(class_id):
    '''Route to get the grade for a single class'''
    grade = [grade for grade in grades if grade['id'] == class_id]
    if len(grade) == 0:
        abort(404)
    return jsonify({'grade' : grade[0]})

#@app.route('/canvas/api/v1/file_upload', methods=['POST'])
#@requires_auth
#def upload_file(file):

# @app.route('/canvas/api/v1/file_download', methods=['GET'])
# @requires_auth
# def download_file(file_name):


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

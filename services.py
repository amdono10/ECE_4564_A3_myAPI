from flask import Flask, request, Response, jsonify, abort
from flask_discoverer import Discoverer, advertise
import json
import pymongo
from bson import json_util
from bson.objectid import ObjectId
from functools import wraps
from pymongo import MongoClient
import requests


course_list = []

from six.moves import input
from zeroconf import ServiceBrowser, Zeroconf

address = '\xc0\xa8\x00\x0f'
ipv4 = ':'.join(str(ord(i)) for i in address)
print (ipv4)

class MyListener(object):
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        # print name, info.get_name(), info.server,
        print (name, info)


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()

header = {"Authorization": "Bearer 4511~hNgxEqiPIYBBsV6jwwogaa1Jit4cBsPhFKOzPFjRpzws7qhhZd2PP5MUlt2uPhLI"}

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

def check_auth(username, password):
    return username == "admin" and password == "secret"
    # for i in userLib.find():
    #     user = i["username"]
    #     passw = i["password"]
    #     if username == user and passw == password:
    #         return true
    # return false

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


# for i in userLib.find():
#     user = i["username"]
#     if user == "Adam" or user == "Brendan" or user == "Brandon":
#         print(user)

def mongoToJson(data):
    """Convert Mongo objects to JSON"""
    return json.dumps(data,  default=json_util.default)


@app.route('/calculator/api/v1/grades', methods=['GET'])
@requires_auth
def get_grades():
    '''Route to get all grades for a student'''
    course_list_obj = requests.get('https://canvas.vt.edu/api/v1/courses', headers = header)
    course_list = []
    print(course_list_obj)

    #defualt is 100 for each course
    for item in course_list_obj.json():
        course_list.append({"id": item["id"], 'name': item["name"], 'grade':100})

    return jsonify({'grades': course_list})

@app.route('/calculator/api/v1/grades/<int:class_id>', methods=['GET'])
@requires_auth
def get_grade(class_id):
    '''Route to get the grade for a single class'''
    url = 'https://canvas.vt.edu/api/v1/courses/' + class_id + '/assignments'
    r = request.get(url, headers=header)
    #grade = [grade for grade in grades if grade['id'] == class_id]
    if len(grade) == 0:
        abort(404)
    return jsonify({'grade' : grade[0]})

#@app.route('/canvas/api/v1/file_upload', methods=['POST'])
#@requires_auth
#def upload_file(file):

# @app.route('/canvas/api/v1/file_download', methods=['GET'])
# @requires_auth
# def download_file(file_name):

@app.route('/canvas/api/v1/send', methods=['POST'])
@requires_auth
def send_grade(grade, course_id):
    grade = request.json['grade']
    cid = request.json['id']
    for item in grades:
        if item['id'] == cid:
            item['id']['grade'] = grade

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

@app.route('/LED', methods=['POST'])
@requires_auth
def LED():
    #contact the LED pi
    payload = {"status":requst.args.get("status"), "color":requst.args.get("color"), "intensity":requst.args.get("intensity")}
    r = requests.post(ipv4, data=payload)

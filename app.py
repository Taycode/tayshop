from chalice import Chalice
from pymongo import MongoClient
import json
from bson import ObjectId
client = MongoClient('mongodb+srv://tay2druh:olawale.@tay-canvy.mongodb.net/test?retryWrites=true&w=majority')
db = client.get_database('products_db')
table = db.products_records


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Chalice(app_name='tayshop')


@app.route('/')
def index():
    return JSONEncoder().encode(list(table.find())[0])


@app.route('/all', methods=['GET'])
def all_products():
    return JSONEncoder().encode(list(table.find())[0])


@app.route('/{name}')
def product(name):
    data = table.find_one({'name': name})
    return JSONEncoder().encode(data)


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

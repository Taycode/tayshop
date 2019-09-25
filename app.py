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
    return JSONEncoder().encode(list(table.find()))


@app.route('/all', methods=['GET'])
def all_products():
    return JSONEncoder().encode(list(table.find()))


@app.route('/{id}')
def product(name):
    data = table.find_one({'id': id})
    return JSONEncoder().encode(data)


@app.route('/create', methods=['POST'])
def create_product():
    request = app.current_request
    body = request.json_body
    body['id'] = table.count() + 1
    table.insert_one(body)
    return {'message': 'Successful addition'}


@app.route('/{id}/delete', methods=['POST'])
def product_delete(id):
    data = table.find_one({'id': id})
    if data is not None:
        table.delete_one(data)
        return {'message': 'Successful Deleting'}
    else:
        return {'message': 'Product not Found'}


@app.route('/{id}/update', methods=['POST'])
def product_update(id):
    request = app.current_request
    data = table.find_one({'id': id})
    body = request.json_body
    new_data = {'$set': body}
    table.update_one(data, new_data)
    return {'message': 'Successful Updating'}
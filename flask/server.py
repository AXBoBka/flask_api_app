from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongo:27017')
db = client['service_data']
collection = db['data']

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api', methods=['POST'])
def add_data():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    
    existing_data = collection.find_one({'key': key})
    if existing_data:
        return 'Запись с указанным ключом уже существует'
    
    if key and value:
        collection.insert_one({'key': key, 'value': value})
        return 'Данные успешно добавлены в базу данных'
    else:
        return 'Ошибка: не удалось добавить данные в базу данных. Проверьте ключ и значение.'


@app.route('/api', methods=['PUT'])
def update_data():
    data = request.json
    key = data.get('key')
    new_value = data.get('value')
    if key and new_value:
        collection.update_one({'key': key}, {'$set': {'value': new_value}})
        return 'Значение успешно обновлено'
    else:
        return 'Ошибка: не удалось обновить значение. Проверьте ключ и новое значение.'


@app.route('/api', methods=['GET'])
def get_data():
    key = request.args.get('key')
    if key:
        document = collection.find_one({'key': key})
        if document:
            return jsonify(f"{document['key']}: {document['value']}")
        else:
            return 'Данные не найдены'
    else:
        return 'Ошибка: необходимо указать ключ для получения данных'


@app.route('/api/get_all', methods=['GET'])
def get_all_data():
    documents = collection.find()
    documents_list = list(documents)
    for document in documents_list:
        del document['_id']
    return jsonify(documents_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

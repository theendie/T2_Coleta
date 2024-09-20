import os
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import pandas as pd

from medals import Medals

app = Flask(__name__)
api = Api(app)

# Carrega o arquivo CSV
df = pd.read_csv("dataset/medals.csv", encoding='utf-8', keep_default_na=False)
# Inicializa a classe Medals
medals = Medals()

# http://127.0.0.1:5000/medals/{country_name}
@app.route('/medal/<string:country_name>', methods=['GET'])
def medals_by_country(country_name=None):
    medals_by_country = medals.get_by(country_name)
    if medals_by_country is not None and not medals_by_country.empty:
        return jsonify(medals_by_country.to_dict(orient='records')), 200
    return {'message': 'Medal not found'}, 404

# http://127.0.0.1:5000/medals
@app.route('/medal', methods=['POST'])
def save_new_medal():
    medal_body = request.json

    print('Saving new medal...', medal_body)

    saved_successfully, e = medals.save_new_medal(medal_body)

    if saved_successfully is True: 
        return {'message': 'Medal was successfully saved'}, 201
    return {f'message': 'Error saving medal', 'error': '{e}'}, 400

# http://127.0.0.1/medal?code={medal_code}
@app.route('/medal', methods=['PUT'])
def update_medal():
    medal_code = request.args.get('code')
    print('Updating medal, medal code ', medal_code)

    if medal_code is None:
        return {'message': 'Missing required parameter: code'}, 400

    medal_body = request.json

    updated_successfully = medals.update_medal(medal_code, medal_body)

    if updated_successfully is True:
        return {'message': 'Medal was successfully updated.'}, 200
    return {'message': 'Medal not found'}, 404

# http://127.0.0.1/medal?code={medal_code}
@app.route('/medal', methods=['DELETE'])
def delete_medal():
    medal_code = request.args.get('code')

    print('Deleting medal, medal code ', medal_code)

    if medal_code is None:
        return {'message': 'Missing required parameter: code'}, 400
    
    deleted_successfully = medals.delete_medal(medal_code)
    
    if deleted_successfully is True:
        return {'message': 'Medal deleted'}, 200
    return {'message': 'Medal not found'}, 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
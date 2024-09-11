from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd

app = Flask(__name__)
api = Api(app)

df = pd.read_csv("dataset/medals.csv", encoding='utf-8', keep_default_na=False)

json_data = df.to_json(orient='records')
print(df)
##print(json_data)

data = json_data

class Medalhas(Resource):
    def get(self, country=None):
        if country:
            dataset_country = df.loc[df[u'country_code'] == country.upper()]
            return dataset_country.to_json(orient='records')
        return data, 200

    def post(self, item_id):
        if item_id in data:
            return {'message': 'Item already exists'}, 400
        data[item_id] = request.json.get('value')
        
        return {item_id: data[item_id]}, 201

    def put(self, item_id):
        data[item_id] = request.json.get('value')
        return {item_id: data[item_id]}, 200

    def delete(self, item_id):
        if item_id in data:
            del data[item_id]
            return {'message': 'Item deleted'}, 200
        return {'message': 'Item not found'}, 404

api.add_resource(Medalhas, '/medalha', '/medalhas/<string:country>')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import pandas as pd

app = Flask(__name__)
api = Api(app)

data = []

class Medals(Resource):
    df = pd.read_csv("dataset/medals.csv", encoding='utf-8', keep_default_na=False)

    #  http://127.0.0.1:5000/medals/{country_name}
    def get(self, country_name=None):
        if country_name:
            dataset_country = self.df[self.df['country'].str.contains(country_name, case=False, na=False)]
            if not dataset_country.empty:
                return jsonify(dataset_country.to_dict(orient='records'))
            return {'message': 'Country not found'}, 400
        return {'message': 'Country not found'}, 400

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

api.add_resource(Medals, '/medals', '/medals/', '/medals/<string:country_name>')

if __name__ == '__main__':
    app.run(debug=True)
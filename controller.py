from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import pandas as pd
import uuid

app = Flask(__name__)
api = Api(app)

data = []

class Medals(Resource):
    df = pd.read_csv("dataset/medals.csv", encoding='utf-8', keep_default_na=False)

    #  http://127.0.0.1:5000/medals/{country_name}
    def get(self, country_name=None):
        if country_name:
            # Filtra o DataFrame para retornar as medalhas do país que contenha a string passada
            dataset_country = self.df[self.df['country'].str.contains(country_name, case=False, na=False)]
            # Verifica se o DataFrame não está vazio
            if not dataset_country.empty:
                # Retorna as medalhas do país
                return jsonify(dataset_country.to_dict(orient='records'))
            # Retorna uma mensagem de erro caso o país não seja encontrado
            return {'message': 'Country not found'}, 400
        return {'message': 'Country not found'}, 400

    def post(self):
        medal = request.json
        print('Adicionando nova medalha', medal)

        # Pega os dados da nova medalha
        code = str(uuid.uuid4())
        medal_type = medal['medal_type']
        medal_code = medal['medal_code']
        medal_date = medal['medal_date']
        name = medal['name']
        gender = medal['gender']
        discipline = medal['discipline']
        event = medal['event']
        event_type = medal['event_type']
        url_event = medal['url_event']
        country = medal['country']
        country_long = medal['country_long']
        country_code = medal['country_code']
        
        # Adiciona a nova medalha ao DataFrame
        new_country_df = pd.DataFrame({
        u'code': [code],
        'medal_type': [medal_type],
        'medal_code': [medal_code],
        'medal_date': [medal_date],
        'name': [name],
        'gender': [gender],
        'discipline': [discipline],
        'event': [event],
        'event_type': [event_type],
        'url_event': [url_event],
        'country': [country],
        'country_long': [country_long],
        'country_code': [country_code]
        })
        # Concatena o novo DataFrame com o DataFrame atual
        self.df = pd.concat([self.df, new_country_df], ignore_index=True)
        
        # Salva o DataFrame atualizado no arquivo CSV
        self.df.to_csv("dataset/medals.csv", index=False, encoding='utf-8')

        return {'message': 'Medal was successfully saved.'}, 201


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
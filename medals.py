import pandas as pd
import uuid

class Medals():
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv("dataset/medals.csv", encoding='utf-8', keep_default_na=False)
    
    def get_by(self, country_name):
        if country_name:
            # Filtra o DataFrame para retornar as medalhas do país que contenha a string passada
            dataset_medal = self.df[self.df['country'].str.contains(country_name, case=False, na=False)]
            # Verifica se o DataFrame não está vazio
            if not dataset_medal.empty:
                # Retorna as medalhas do país
                return dataset_medal
        return None

    def save_new_medal(self, medal_body):
        try:
            # Verificar se todas as chaves necessárias estão presentes
            required_keys = ['medal_type', 'medal_date', 'name', 'gender', 'discipline', 'event', 'event_type', 'url_event', 'country', 'country_long']
            for key in required_keys:
                if key not in medal_body:
                    return False, f"Missing required key: {key}"

            # Gerar UUID para a medalha
            code = str(uuid.uuid4())

            # Adiciona uma nova linha ao DataFrame
            new_row = pd.DataFrame({
                u'medal_type': [medal_body['medal_type']],
                'medal_code': [medal_body['medal_code']],
                'medal_date': [medal_body['medal_date']],
                'name': [medal_body['name']],
                'gender': [medal_body['gender']],
                'discipline': [medal_body['discipline']],
                'event': [medal_body['event']],
                'event_type': [medal_body['event_type']],
                'url_event': [medal_body['url_event']],
                'code':[code],
                'country_code':[medal_body['country_code']],
                'country':[medal_body['country']],
                'country_long':[medal_body['country_long']],
            })

            # Concatena o novo DataFrame com o DataFrame atual
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            
            # Salva o DataFrame atualizado no arquivo CSV
            self.df.to_csv("dataset/medals.csv", index=False, encoding='utf-8')

            return True, None
        except (IOError, OSError) as e:
            # Retorna False e a mensagem de erro caso ocorra uma exceção
            return False, str(e)
        
    def update_medal(self, medal_code, medal_body):
        # Filtra o DataFrame para retornar a medalha com o código passado
        medal = self.df[self.df['code'] == medal_code]

        # Verifica se a medalha não está vazia
        if medal is not None and not medal.empty:
            # Atualiza as informações da medalha
            for key, value in medal_body.items():
                self.df.loc[self.df['code'] == medal_code, key] = medal_body[key]
                print(f'Updating medal... [{key}] old: {value}, new:{medal_body[key]}')
            # Salva o DataFrame atualizado no arquivo CSV
            self.df.to_csv("dataset/medals.csv", index=False, encoding='utf-8')
            return True
        return False
import requests

URL = 'https://api.hh.ru/vacancies'


class HeadHunterAPI:

    def __init__(self):
        self.vacancies = None

    def get_vacancies(self, query: str) -> dict:
        print(f'Получаем данные с {URL}...')
        params = {
            'text': f'NAME:{query}',
            'page': 0,
            'per_page': 100,
            'only_with_salary': True
        }
        response = requests.get(URL, params)
        result_page = response.json()
        self.vacancies = result_page['items']
        while len(result_page['items']) == 100:
            print(f"Загружено страниц c вакансиями: {params['page']}")
            params['page'] += 1
            response = requests.get(URL, params)
            result_page = response.json()
            if result_page.get('items'):
                self.vacancies.extend(result_page['items'])
            else:
                break
        return self.vacancies

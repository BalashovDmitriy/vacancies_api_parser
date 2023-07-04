import json
import requests
from operator import itemgetter
from datetime import datetime

from classes.headhunter import HeadHunterAPI
from classes.superjob import SuperJobAPI
from src.utils import format_salary


def user_interaction():
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI()
    while True:
        user_input = input("С какого сайта взять вакансии?\n"
                           "1. HeadHunter\n"
                           "2. SuperJob\n"
                           "0. Выход\n"
                           "Ваш выбор: ")
        if user_input == "1" or user_input == "2":
            break
        elif user_input == "0":
            print("Выход из программы...")
            exit(0)
    print("\n" * 5)
    search_query = input("Поисковый запрос по вакансиям\n"
                         "В запросе к HeadHunter API по умолчанию включено "
                         "умное преобразование текста от пользователя.\n"
                         "Например, при запросе: 'разработчик москва 70000' Будут выведены вакансии разработчика, "
                         "в городе Москва, с зарплатой не менее 70000руб.\n"
                         "Введите ваш поисковый запрос: ")
    if user_input == "1":
        result = hh_api.get_vacancies(search_query)
    elif user_input == "2":
        result = superjob_api.get_vacancies(search_query)

    # top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()

    if len(result) == 0:
        print("Не найдено вакансий по вашему запросу.")
        user_interaction()
    with open("result.json", "w") as json_file:
        json_file.write(json.dumps(result, indent=2, ensure_ascii=False))

    counter = 0
    sorted_by_date = sorted(result, key=itemgetter('published_at'), reverse=True)
    print("id".ljust(8), "Вакансия".ljust(75), "Зарплата".ljust(30), "Город".ljust(20),
          "Размещено".ljust(25), "Ссылка".ljust(30))
    for element in sorted_by_date:
        time = datetime.fromisoformat(element['published_at'])
        f_time = time.strftime("%d.%m.%Y %H:%M")
        salary = element['salary']
        print(element['id'].ljust(8), element['name'][:75].ljust(75), format_salary(salary).ljust(30),
              element['area']['name'][:20].ljust(20), f_time.ljust(25), element['alternate_url'].ljust(30))
        counter += 1
    print(f"Всего {counter} вакансий загружено")


if __name__ == '__main__':
    user_interaction()
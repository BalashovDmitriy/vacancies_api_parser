import json
import requests
from operator import itemgetter
from datetime import datetime

from classes.headhunter import HeadHunterAPI
from classes.superjob import SuperJobAPI
from classes.vacancy import Vacancy
from src.utils import format_salary, create_instances_from_hh, print_tab, create_instances_from_sj


def user_interaction():
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI()
    while True:
        user_input = input("С какого сайта взять вакансии?\n"
                           "1. HeadHunter\n"
                           "2. SuperJob\n"
                           "3. HeadHunter & SuperJob\n"
                           "0. Выход\n"
                           "Ваш выбор: ")
        if user_input == "1" or user_input == "2" or user_input == "3":
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
        create_instances_from_hh(result)
        print_tab()
    elif user_input == "2":
        result = superjob_api.get_vacancies(search_query)
        create_instances_from_sj(result)
        print_tab()

    # top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()

    # if len(result) == 0:
    #     print("Не найдено вакансий по вашему запросу.")
    #     user_interaction()
    with open("database/database.json", "w") as json_file:
        json_file.write(json.dumps(result, indent=2, ensure_ascii=False))
    #
    # counter = 0
    # sorted_by_date = sorted(result, key=itemgetter('published_at'), reverse=True)



if __name__ == '__main__':
    user_interaction()
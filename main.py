import json

from classes.apiclasses import HeadHunterAPI, SuperJobAPI
from classes.savers import JSONSaver
from classes.vacancy import Vacancy
from src.utils import *


def user_interaction():
    hh_api = HeadHunterAPI()
    super_job_api = SuperJobAPI()

    search_query = input("Введите поисковый запрос вакансии: ")

    result = hh_api.get_vacancies(search_query)
    create_instances_from_hh(result)
    result = super_job_api.get_vacancies(search_query)
    create_instances_from_sj(result, search_query)

    total_vacancies = total()
    json_saver = JSONSaver()
    json_saver.save_vacancies()
    print(f"\nВсего вакансий загружено в файл: {total_vacancies}")

    vacancy = Vacancy("", "", 0, 0, "", "", "", "", "")
    Vacancy.all_vac = []

    data = json_saver.get_vacancies()

    filter_words = input("\nВведите ключевые слова для фильтрации вакансий "
                         "или enter для вывода всех: ").split()
    if len(filter_words) > 0:
        filtered = filter_vacancies(data, filter_words)
    else:
        filtered = data

    if len(filtered) == 0:
        print("Не найдено вакансий по вашему запросу.")

    print(f"Всего отфильтрованных вакансий: {len(filtered)}")

    sort_method = user_input_sort_method()
    if sort_method == 1:
        result = sort_by_date(filtered)
    elif sort_method == 2:
        result = sort_by_salary(filtered)
    elif sort_method == 3:
        result = sort_by_city(filtered)
    create_instances(result)

    top_n = user_input_top(len(vacancy))
    print_tab(top_n)


if __name__ == '__main__':
    user_interaction()

from datetime import datetime
from operator import itemgetter

from classes.vacancy import Vacancy


def format_salary(value_from, value_to):
    if value_from:
        if value_to:
            return f"от {value_from} до {value_to} руб."
        else:
            return f"от {value_from} руб."
    else:
        if value_to:
            return f"до {value_to} руб."


def create_instances_from_hh(database):
    for vacancy in database:
        if vacancy['salary']['currency'] != "RUR":
            continue
        Vacancy(vacancy_id=vacancy['id'],
                name=vacancy['name'],
                salary_from=vacancy['salary']['from'],
                salary_to=vacancy['salary']['to'],
                city=vacancy['area']['name'],
                published=datetime.fromisoformat(vacancy['published_at']).strftime("%d.%m.%Y %H:%M"),
                requirements=vacancy['snippet']['requirement'],
                responsibility=vacancy['snippet']['responsibility'],
                url=vacancy['alternate_url'])


def create_instances_from_sj(database, query):
    for vacancy in database:
        if vacancy['currency'] != "rub" or query not in vacancy['profession']:
            continue
        Vacancy(vacancy_id=str(vacancy['id']),
                name=vacancy['profession'],
                salary_from=vacancy['payment_from'],
                salary_to=vacancy['payment_to'],
                city=vacancy['town']['title'],
                published=datetime.fromtimestamp(vacancy['date_published']).strftime("%d.%m.%Y %H:%M"),
                requirements=vacancy['candidat'],
                responsibility=vacancy['vacancyRichText'],
                url=vacancy['link'])


def print_tab(top_n):
    counter = 0
    print("id".ljust(8), "Вакансия".ljust(75), "Зарплата".ljust(30), "Город".ljust(20),
          "Размещено".ljust(25), "Ссылка".ljust(30))
    for element in Vacancy.all_vac:
        print(element.vacancy_id.ljust(8), element.name[:75].ljust(75),
              format_salary(element.salary_from, element.salary_to).ljust(30),
              element.city[:20].ljust(20), element.published.ljust(25), element.url.ljust(30))
        counter += 1
        if counter == top_n:
            break


def total():
    if len(Vacancy.all_vac) == 0:
        quit("Неудачный запрос")
    return len(Vacancy.all_vac)


def user_input_top(total):
    while True:
        top_n = input(f"Введите количество вакансий для вывода в топ N(от 1 до {total}): ")
        if not top_n.isdigit():
            continue
        elif int(top_n) not in range(1, total):
            continue
        break
    return int(top_n)


def user_input_sort_method():
    while True:
        sort_method = input("\nВыберите способ сортировки: \n"
                            "1. По дате размещения вакансии\n"
                            "2. По зарплате\n"
                            "3. По городу в алфавитном порядке\n")
        if not sort_method.isdigit():
            continue
        elif int(sort_method) not in [1, 2, 3]:
            continue
        break
    return int(sort_method)


def create_instances(data):
    for vacancy in data:
        if isinstance(vacancy['published'], datetime):
            vacancy['published'] = vacancy['published'].strftime("%d.%m.%Y %H:%M")
        Vacancy(vacancy['vacancy_id'],
                vacancy['name'],
                vacancy['salary_from'],
                vacancy['salary_to'],
                vacancy['city'],
                vacancy['url'],
                vacancy['published'],
                vacancy['requirements'],
                vacancy['responsibility'])


def sort_by_date(data):
    for vacancy in data:
        vacancy['published'] = datetime.strptime(vacancy['published'], "%d.%m.%Y %H:%M")
    sorted_vacancy = sorted(data, key=itemgetter('published'), reverse=True)
    return sorted_vacancy


def sort_by_salary(data):
    for vacancy in data:
        if vacancy.get('salary_from') is None:
            vacancy['salary_from'] = 0
    sorted_vacancy = sorted(data, key=itemgetter('salary_from'), reverse=True)
    for vacancy in sorted_vacancy:
        if vacancy['salary_from'] == 0:
            vacancy['salary_from'] = None
    return sorted_vacancy


def sort_by_city(data):
    sorted_vacancy = sorted(data, key=itemgetter('city'))
    return sorted_vacancy


def filter_vacancies(data, query):
    result = []
    for vacancy in data:
        for element in query:
            if vacancy['requirements'] is None or vacancy['responsibility'] is None:
                continue
            elif element in vacancy['requirements'] or element in vacancy['responsibility']:
                result.append(vacancy)
    return result

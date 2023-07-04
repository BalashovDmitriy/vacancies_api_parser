from datetime import datetime
from datetime import time

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


def create_instances_from_sj(database):
    for vacancy in database:
        if vacancy['currency'] != "rub":
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


def print_tab():
    print("id".ljust(8), "Вакансия".ljust(75), "Зарплата".ljust(30), "Город".ljust(20),
          "Размещено".ljust(25), "Ссылка".ljust(30))
    for element in Vacancy.all_vac:
        print(element.vacancy_id.ljust(8), element.name[:75].ljust(75),
              format_salary(element.salary_from, element.salary_to).ljust(30),
              element.city[:20].ljust(20), element.published.ljust(25), element.url.ljust(30))
    print(f"Всего {len(Vacancy.all_vac)} вакансий загружено")

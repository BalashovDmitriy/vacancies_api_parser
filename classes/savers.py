from abc import ABC, abstractmethod
import json

from classes.vacancy import Vacancy


class Saver(ABC):

    @abstractmethod
    def save_vacancies(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class JSONSaver(Saver):

    def save_vacancies(self):
        json_dict = []
        for vacancy in Vacancy.all_vac:
            json_dict.append(vacancy.__dict__)
        with open("database/database.json", "w") as json_file:
            json_file.write(json.dumps(json_dict, indent=2, ensure_ascii=False))

    def get_vacancies(self):
        with open("database/database.json") as json_file:
            json_dict = json.load(json_file)
        return json_dict

from abc import ABC, abstractmethod
from os import path, remove
from classes import Vacancy
import json


class Connector(ABC):

    @abstractmethod
    def insert(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, query):
        pass

    @abstractmethod
    def select(self):
        pass


class JSONSaver:
    def __init__(self, search_query, vacancy_list):
        self.__file_to_save = f'{search_query.title()}.json'
        folder_path = path.abspath("Job_Parser/data")
        self.file_path = path.join(folder_path, self.__file_to_save)
        self.insert(vacancy_list)

    def insert(self, vacancy):
        with open(self.file_path, 'w') as f:
            json.dump(vacancy, f, indent=4, ensure_ascii=False)

    def select(self):
        with open(self.file_path, 'r') as f:
            file_data = json.load(f)
            vacancies = [Vacancy(i['api'], i['title'], i['url'],
                                 i['salary_from'], i['salary_to'],
                                 i['currency'], i['employer']) for i in file_data]
            return vacancies

    def get_vacancies_by_salary(self, salary_from, salary_to=None):
        filtered_list = []

        for vacancy in self.select():
            if salary_to is None:
                if vacancy.salary_from and vacancy.salary_to == 0:
                    continue
                elif vacancy.salary_to != 0:
                    if salary_from < vacancy.salary_to:
                        filtered_list.append(vacancy)
                else:
                    if salary_from < vacancy.salary_from:
                        filtered_list.append(vacancy)
                    continue
        if len(filtered_list) == 0:
            return 'К сожалению вакансий от такой суммы нет.'
        else:
            return filtered_list

    def delete_save_file(self):
        remove(self.file_path)

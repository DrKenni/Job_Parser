from abc import ABC, abstractmethod
from os import path, remove
from classes import Vacancy
import json


class Connector(ABC):

    @abstractmethod
    def insert(self, vacancy):
        pass

    @abstractmethod
    def select(self):
        pass

    @abstractmethod
    def delete_save_file(self):
        pass


class JSONSaver:
    def __init__(self, search_query, vacancy_list):
        self.__file_to_save = f'{search_query.title()}.json'
        self.file_path = path.join('data', self.__file_to_save)
        self.insert(vacancy_list)

    def insert(self, vacancy):
        """Создает фаил в котором будет храниться информация в json формате"""
        with open(self.file_path, 'w', encoding='windows-1251') as f:
            json.dump(vacancy, f, indent=4, ensure_ascii=False)

    def select(self):
        """Создает экземпляры класса Vacancy
        return: список экземпляров класса Vacancy"""
        with open(self.file_path, 'r') as f:
            file_data = json.load(f)
            vacancies = []

            for i in file_data:
                vacancy = Vacancy(i['api'], i['title'], i['url'], i['salary_from'],
                                  i['salary_to'], i['currency'], i['employer'])
                vacancies.append(vacancy)

            return vacancies

    def delete_save_file(self):
        """Удаляет фаил в который сохраняли json данные"""
        remove(self.file_path)

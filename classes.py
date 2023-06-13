from abc import ABC, abstractmethod
from requests import *
import os
from configparser import ParsingError
import json
from pprint import pprint


class AbstractClass(ABC):
    @abstractmethod
    def get_vacancies(self, search_query, top_n):
        pass


class HeadHunterAPI(AbstractClass):
    """Получает вакансии с HeadHunter"""
    
    def __init__(self):
        self.__vacancies = []

    @property
    def vacancies(self):
        return self.__vacancies

    @staticmethod
    def get_formatted_vacancies(data):
        formatted_vacancies = []
        for vacancy in data:
            formatted_vacancies.append({
                'api': 'HeadHunter',
                'title': vacancy['name'],
                'url': vacancy['alternate_url'],
                'salary_from': vacancy['salary']['from'],
                'salary_to': vacancy['salary']['to'],
                'currency': vacancy['salary']['currency'],
                'employer': vacancy['employer']['name'],
            })
        return formatted_vacancies

    def get_vacancies(self, search_query, top_n):
        params = {'text': search_query,
                  'page': 0,
                  'per_page': 100}
        response = get('https://api.hh.ru/vacancies/', params=params)
        if response.status_code != 200:
            raise ParsingError
        else:
            data = response.json()['items']
            self.__vacancies.extend(self.get_formatted_vacancies(data))
            return self.vacancies
                # print(item['profession'])
                # vacancies = Vacancy(item['name'], item['url'], item['salary'], item['snippet']['requirement'])

hh = HeadHunterAPI()
hh.get_vacancies(['Python'], 5)

class SuperJobAPI(AbstractClass):
    """Получает вакансии с SuperJob"""
    header = {"X-Api-App-Id": os.getenv('SJ_API_KEY')}

    def __init__(self):
        pass

    def get_vacancies(self, search_query, top_n):
        pass


class Vacancy:
    """Создает экземпляры класса для работы с вакансиями"""
    __slots__ = ('name', 'url', 'salary', 'conditions')

    def __init__(self, name, url, salary, conditions):
        self.name = name
        self.url = url
        self.salary = salary
        self.conditions = conditions


class JSONSaver:
    def __init__(self):
        pass

    def add_vacancy(self, vacancy):
        pass

    def get_vacancies_by_salary(self, salary):
        pass

    def delete_vacancy(self, vacancy):
        pass

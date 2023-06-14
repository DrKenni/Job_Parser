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
            if vacancy['salary'] is None:
                currency, salary_from, salary_to = None, 0, 0
            else:
                currency, salary_from, salary_to = \
                    vacancy['salary']['currency'], vacancy['salary']['from'], vacancy['salary']['to']
            formatted_vacancies.append({
                'api': 'HeadHunter',
                'title': vacancy['name'],
                'url': vacancy['alternate_url'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'currency': currency,
                'employer': vacancy['employer']['name'],
            })
        return formatted_vacancies

    def get_reqest(self, search_query):
        params = {'text': search_query,
                  'page': 0,
                  'per_page': 100}
        response = get('https://api.hh.ru/vacancies/', params=params)
        if response.status_code != 200:
            raise ParsingError
        else:
            return response.json()['items']

    def get_vacancies(self, search_query, top_n):
        try:
            data = self.get_reqest(search_query)
            self.__vacancies.extend(self.get_formatted_vacancies(data))
            return self.vacancies
        except ParsingError:
            raise ParsingError('Ошибка получения данных с HeadHunter')

# hh = HeadHunterAPI()
# pprint(hh.get_vacancies('Python', 5))


class SuperJobAPI(AbstractClass):
    """Получает вакансии с SuperJob"""
    header = {"X-Api-App-Id": os.getenv('SJ_API_KEY')}

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
                'api': 'SuperJob',
                'title': vacancy['profession'],
                'url': vacancy['link'],
                'salary_from': vacancy['payment_from'],
                'salary_to': vacancy['payment_to'],
                'currency': vacancy['currency'],
                'employer': vacancy['firm_name'],
            })
        return formatted_vacancies

    def get_request(self, search_query):
        params = {'keyword': search_query,
                  'page': 0,
                  'count': 100}
        response = get('https://api.superjob.ru/2.0/vacancies/', params=params, headers=self.header)
        if response.status_code != 200:
            raise ParsingError
        else:
            return response.json()['objects']

    def get_vacancies(self, search_query, top_n):
        try:
            data = self.get_request(search_query)
            self.__vacancies.extend(self.get_formatted_vacancies(data))
            return self.vacancies
        except ParsingError:
            raise ParsingError('Ошибка получения данных с SuperJob')

sj = SuperJobAPI()
pprint(sj.get_vacancies('Python', 5))
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

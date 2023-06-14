from abc import ABC, abstractmethod
from requests import *
import os
from configparser import ParsingError


class AbstractClass(ABC):

    @abstractmethod
    def get_request(self, search_query):
        pass

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

    def get_request(self, search_query):
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
            data = self.get_request(search_query)
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

# sj = SuperJobAPI()
# pprint(sj.get_vacancies('Python', 5))


class Vacancy:
    """Создает экземпляры класса для работы с вакансиями"""
    __slots__ = ('api', 'title', 'url', 'salary_from', 'salary_to', 'currency', 'employer')

    def __init__(self, api, title, url, salary_from, salary_to, currency, employer):
        self.api = api
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.employer = employer

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__slots__})'

    def __str__(self):
        salary_from = f'От {self.salary_from}' if self.salary_from else ''
        salary_to = f'От {self.salary_to}' if self.salary_to else ''
        if self.salary_from and self.salary_to is 0:
            self.salary_to = "Не указана"
            self.salary_from = ''
            self.currency = ''
        return f'Компания: {self.employer}\nВакансия: {self.title}' \
               f'Зарплата: {salary_from} {salary_to} {self.currency}' \
               f'Url: {self.url}'

    # def __getitem__(self, item):
    #     return item

    def __gt__(self, other):
        if other.salary_from is None:
            return True
        elif self.salary_from is None:
            return False
        return self.salary_from > other.salary_from

    def __lt__(self, other):
        if other.salary_from is None:
            return True
        elif self.salary_from is None:
            return False
        return self.salary_from < other.salary_from

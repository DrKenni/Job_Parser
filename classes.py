from abc import ABC, abstractmethod
from requests import *
import os
from configparser import ParsingError


class AbstractClass(ABC):

    @abstractmethod
    def get_request(self, search_query):
        pass

    @abstractmethod
    def get_vacancies(self, search_query):
        pass


class MixinSalary:
    @staticmethod
    def formatted_salary(s_from, s_to, currency):
        new_format = [0, 0, 0]
        new_format[0] = s_from if s_from != 0 else 0
        new_format[1] = s_to if s_to != 0 else 0
        new_format[2] = currency if s_to or s_from != 0 or None else 'Не указана'
        return new_format


class HeadHunterAPI(AbstractClass, MixinSalary):
    """Получает вакансии с HeadHunter"""
    
    def __init__(self):
        self.__vacancies = []

    def __str__(self):
        return "HeadHunter"

    @property
    def vacancies(self):
        return self.__vacancies

    def get_formatted_vacancies(self, data):
        """Собирает нужные данные в список сo словарем
        data: список json с вакансиями с сайта
        return: словарь с нужными ключами"""
        formatted_vacancies = []
        for vacancy in data:

            if vacancy['salary'] is None:
                s_from, s_to, currency = 0, 0, 'Не указана'
            else:
                s_from, s_to, currency = self.formatted_salary(
                    vacancy['salary']['from'], vacancy['salary']['to'], vacancy['salary']['currency'])
            formatted_vacancies.append({
                'api': 'HeadHunter',
                'title': vacancy['name'],
                'url': vacancy['alternate_url'],
                'salary_from': s_from,
                'salary_to': s_to,
                'currency': currency,
                'employer': vacancy['employer']['name'],
            })
        return formatted_vacancies

    def get_request(self, search_query):
        """Получает список json с вакансиями с сайта
        search_query: Слово по которому идет поиск вакансий"""
        params = {'text': search_query,
                  'page': 0,
                  'per_page': 100}
        response = get('https://api.hh.ru/vacancies/', params=params)
        if response.status_code != 200:
            raise ParsingError
        else:
            return response.json()['items']

    def get_vacancies(self, search_query):
        """Возвращает отфильтрованный по атрибуту список с вакансиями
        search_query: Слово по которому идет поиск вакансий
        return: список класса отфильтрованный по атрибуту с вакансиями"""
        try:
            data = self.get_request(search_query)
            self.__vacancies.extend(self.get_formatted_vacancies(data))
            return self.vacancies
        except ParsingError:
            raise ParsingError('Ошибка получения данных с HeadHunter')


class SuperJobAPI(AbstractClass, MixinSalary):
    """Получает вакансии с SuperJob"""
    header = {"X-Api-App-Id": os.getenv('SJ_API_KEY')}

    def __init__(self):
        self.__vacancies = []

    def __str__(self):
        return "SuperJob"

    @property
    def vacancies(self):
        return self.__vacancies

    def get_formatted_vacancies(self, data):
        """Собирает нужные данные в список сo словарем
        data: список json с вакансиями с сайта
        return: словарь с нужными ключами"""
        formatted_vacancies = []
        for vacancy in data:
            s_from, s_to, currency = self.formatted_salary(
                vacancy['payment_from'], vacancy['payment_to'], vacancy['currency'])
            formatted_vacancies.append({
                'api': 'SuperJob',
                'title': vacancy['profession'],
                'url': vacancy['link'],
                'salary_from': s_from,
                'salary_to': s_to,
                'currency': currency,
                'employer': vacancy['firm_name'],
            })
        return formatted_vacancies

    def get_request(self, search_query):
        """Получает список json с вакансиями с сайта
        search_query: Слово по которому идет поиск вакансий"""
        params = {'keyword': search_query,
                  'page': 0,
                  'count': 100}
        response = get('https://api.superjob.ru/2.0/vacancies/', params=params, headers=self.header)
        if response.status_code != 200:
            raise ParsingError
        else:
            return response.json()['objects']

    def get_vacancies(self, search_query):
        """Возвращает отфильтрованный по атрибуту список с вакансиями
        search_query: Слово по которому идет поиск вакансий
        return: список класса отфильтрованный по атрибуту с вакансиями"""
        try:
            data = self.get_request(search_query)
            self.__vacancies.extend(self.get_formatted_vacancies(data))
            return self.vacancies
        except ParsingError:
            raise ParsingError('Ошибка получения данных с SuperJob')


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
        salary_to = f'До {self.salary_to}' if self.salary_to else ''
        return f'{self.api}\n' \
               f'Компания: {self.employer}\nВакансия: {self.title}\n' \
               f'Зарплата: {salary_from} {salary_to} {self.currency}\n' \
               f'Url: {self.url}\n'

    def __gt__(self, other):
        if other.salary_from is None:
            return True
        elif self.salary_from is None:
            return False
        return self.salary_from > other.salary_from

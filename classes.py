from abc import ABC, abstractmethod
import requests


class AbstractClass(ABC):
    def get_vacancies(self, name_vacancy):
        pass


class HeadHunterAPI(AbstractClass):
    """Получает вакансии с HeadHunter"""
    def __init__(self):
        pass

    def get_vacancies(self, name_vacancy):
        pass


class SuperJobAPI(AbstractClass):
    """Получает вакансии с SuperJob"""
    def __init__(self):
        pass

    def get_vacancies(self, name_vacancy):
        pass


class Vacancy:
    """Создает экземпляры класса для работы с вакансиями"""
    def __init__(self, name, url, salary, requirements):
        pass


class JSONSaver:
    def __init__(self):
        pass

    def add_vacancy(self, vacancy):
        pass

    def get_vacancies_by_salary(self, salary):
        pass

    def delete_vacancy(self, vacancy):
        pass

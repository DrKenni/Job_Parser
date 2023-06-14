from utils import filter_vacancies, sort_vacancies, get_top_vacancies, print_vacancies
from classes import Vacancy, HeadHunterAPI, SuperJobAPI
from connector import JSONSaver
# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()
sj_api = SuperJobAPI()

# Сохранение информации о вакансиях в файл
json_saver = JSONSaver()
json_saver.add_vacancy(vacancy)
json_saver.get_vacancies_by_salary("100 000-150 000 руб.")
json_saver.delete_vacancy(vacancy)


# Функция для взаимодействия с пользователем
def user_interaction():
    platforms = [hh_api, sj_api]
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    search_query = input("Введите ключевое слово для фильтрации вакансий: ").split()
    # Получение вакансий с разных платформ
    hh_vacancies = hh_api.get_vacancies(search_query, top_n)
    superjob_vacancies = sj_api.get_vacancies(search_query, top_n)
    filtered_vacancies = filter_vacancies([hh_vacancies, superjob_vacancies])

    if not filtered_vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()

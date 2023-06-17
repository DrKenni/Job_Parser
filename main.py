from classes import HeadHunterAPI, SuperJobAPI
from connector import JSONSaver
from utils import sort_vacancies, get_top_vacancies, choosing_actions, finish

# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()
sj_api = SuperJobAPI()


# Функция для взаимодействия с пользователем
def user_interaction():
    platforms = [hh_api, sj_api]
    search_query = input("Введите ключевое слово для фильтрации вакансий: ")

    # Получение вакансий с разных платформ
    vacancy_list = []
    for platform in platforms:
        vacancy_list.extend(platform.get_vacancies(search_query))
        print(f'На {str(platform)} найдено {len(platform.vacancies)} вакансий.')

    # Сохранение вакансий в отдельный фаил
    connector = JSONSaver(search_query, vacancy_list)

    # Интерфейс взаимодействия с пользователем
    while True:
        user_command = str(input('\n1 - Вывести список вакансий\n'
                                 '2 - Отсортировать вакансии по ЗП\n'
                                 '3 - Вывести топ вакансий по ЗП\n'
                                 '0 - Завершить работу\n'))

        if user_command == '1':
            vacancies = connector.select()
            for vacancy in vacancies:
                print(vacancy, end='\n')
            choosing_actions(connector)

        elif user_command == '2':
            while True:
                sort = sort_vacancies(connector.select())
                for v in sort:
                    print(v)
                choosing_actions(connector)

        elif user_command == '3':
            top_n = int(input("Введите количество вакансий для вывода в топ N: "))
            vacancies = get_top_vacancies(connector.select(), top_n)
            for vacancy in vacancies:
                print(vacancy)
            choosing_actions(connector)

        elif user_command == '0':
            finish(connector)

        else:
            print('Такой команды нет!')
            continue


if __name__ == "__main__":
    user_interaction()

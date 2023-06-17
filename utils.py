
def sort_vacancies(filtered_vacancies):
    """Сортирует отфильтрованные вакансии"""
    have_salary = []
    for vacancy in filtered_vacancies:
        try:
            if vacancy.salary_from > 1:
                have_salary.append(vacancy)
        except TypeError:
            continue
    return sorted(have_salary, reverse=True)


def get_top_vacancies(filtered_vacancies, top_n):
    """Возвращает последние top_n лучших вакансий"""
    return sort_vacancies(filtered_vacancies)[:top_n]


def choosing_actions(connector):
    """Вспомогательная функция действия"""
    user_input = input('1 - Продолжить\n'
                       '0 - Завершить работу\n')
    while True:
        if user_input == '1':
            break
        elif user_input == '0':
            finish(connector)
            return quit('До свидания!')
        else:
            print('Такой команды нет!')
            continue


def finish(connector):
    """Вспомогательная функция завершения работы"""
    user_finish = input('1 - Сохранить фаил с вакансиями\n'
                        '2 - Удалить фаил с вакансиями\n')
    while True:
        if user_finish == '1':
            quit('До свидания!')
        elif user_finish == '2':
            connector.delete_save_file()
            quit('До свидания!')
        else:
            print('Такой команды нет!')

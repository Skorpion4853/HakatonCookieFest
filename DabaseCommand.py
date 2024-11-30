from Config import get_config
from connect_to_mysql import connect_to_mysql
import pandas as pd


status_op = ( #Так как статусов на самом деле много, было принято решение остановиться на 4 основных
     'Готово для согласования',
     'Зарегистрировано',
     'Обязательства выполнены',
     'Договор разорван'
)

status_payment = ( #Для статусов оплаты были выбраны эти 4 процесса
    'Не оплачен',
    'Частично оплачен',
    'Оплачен',
    'Возврат'
)

def get_worker_top(cur_user: str, sorting: str) -> str: #Функция для вывода топ 10 работников

    cnx = connect_to_mysql(get_config(), attempts=3) #делаем коннект к БД

    if cnx and cnx.is_connected(): #Если коннект прошел успешно создаем курсор
        cursor = cnx.cursor()
        #создание цен для разных типов операций
        prices = {
            1: 10,
            2: 11,
            3: 13
                  }
        #Вытаскивание данных из БД

        #Запрос на вывод филиала залогиненого сотрудника
        query = "SELECT id, filial FROM Users WHERE login = %s"
        cursor.execute(query, [cur_user])
        cur_filial = cursor.fetchall()
        cur_user = cur_filial[0][0]
        cur_filial = cur_filial[0][1]

        #Запрос на вывод всех сотрудников филиала
        query = "SELECT id, full_name FROM Users WHERE filial = %s"
        cursor.execute(query, [cur_filial])
        users = cursor.fetchall()

        #Создание списка всех сотрудников филиала
        users_id = []
        for user in users:
            users_id.append(user[0])

        #Запрос на вывод всех операций сотрудников данного филиала
        format_strings = ','.join(['%s'] * len(users_id))
        cursor.execute("SELECT * FROM Operations WHERE worker_id IN (%s)" %format_strings,
                       tuple(users_id))
        operations = cursor.fetchall()

        #Сохранение данных из БД в формате DataFrame для работы с ними
        users_df = pd.DataFrame(columns=["id", "full_name"], data=users)
        operation_df = pd.DataFrame(columns=["id", "counterparty", "worker_id", "type", "status", "status_payment",
                                             "date", "price"], data=operations)

        user_full_name = users_df[users_df["id"] == cur_user]['full_name'] #Сохранение ФИО пользователя
        data = [] #Пустышка для сохранения данных для итогового, дата фрейма с рейтингом
        for user in users_id: #перебираем всех юзеров, что работали в этом месяце
            price = 0.00
            salary = 0.00
            for operation in operation_df[operation_df["worker_id"].isin([user])].to_numpy(): #Создаем объект дата фрейма со всеми операциями пользователя
                price += operation[-1]
                salary += operation[-1] * prices[operation[3]] / 100
            full_name = users_df[users_df["id"].isin([user])]["full_name"].to_numpy()[0] #Вытаскиваем фио сотрудника
            data.append([full_name, round(price, 2), round(salary, 2)])



        df_top_u = pd.DataFrame(columns=["full_name", "price", "salary"], data=data) #Создаем pd серию для вывода
        df_top_u = df_top_u.sort_values(sorting, ascending=False) #Делаем сортировку по выбранному параметру

        user_place = -1 #Сохранение позиции в топе у user
        place = 0 #Место в топе
        top_str = "" #Строка для возврата рейтинга

        for top_user in df_top_u.to_numpy():
            place += 1 #Делаем перемещение по местам в топе
            if user_full_name.to_numpy()[0] == top_user[0]: #Сохраняем позицию пользователя если ФИО совпадает
                user_place = place

            #Делаем проверку для первых 3 пользователей и добавляем им стикеры соответсвующее их месту в топе
            if place == 1:
                top_str += "\U0001F947 " + " ".join(map(str,top_user)) + "\n"
            elif place == 2:
                top_str += "\U0001F948 " + " ".join(map(str,top_user)) + "\n"
            elif place == 3:
                top_str += "\U0001F949 "+ " ".join(map(str,top_user))+ "\n"
            elif place <= 10:
                #Выводим оставшейся места с указанием их позиции в топе
                top_str += str(place)+ " " + " ".join(map(str,top_user))+ "\n"
            elif user_place > 10 and user_full_name.to_numpy()[0] == top_user[0]:
                #Если пользователь не входит в 10 лучших, то выводим его место отдельно от остальных
                top_str += ". . .\n"
                top_str += str(place)+ " " + " ".join(map(str,top_user))+ "\n"

        cursor.close()
        cnx.close()

        return top_str
    else:
        return "Could not connect"


def return_worker_top(cur_user: str, sorting: str) -> pd.DataFrame or str: #Функция для вывода топ 10 работников

    cnx = connect_to_mysql(get_config(), attempts=3) #делаем коннект к БД

    if cnx and cnx.is_connected(): #Если коннект прошел успешно создаем курсор
        cursor = cnx.cursor()
        #создание цен для разных типов операций
        prices = {
            1: 10,
            2: 11,
            3: 13
                  }
        #Вытаскивание данных из БД

        # Запрос на вывод филиала залогиненого сотрудника
        query = "SELECT id, filial FROM Users WHERE login = %s"
        cursor.execute(query, [cur_user])
        cur_filial = cursor.fetchall()
        cur_filial = cur_filial[0][1]

        # Запрос на вывод всех сотрудников филиала
        query = "SELECT id, full_name FROM Users WHERE filial = %s"
        cursor.execute(query, [cur_filial])
        users = cursor.fetchall()

        #Создание списка всех сотрудников филиала
        users_id = []
        for user in users:
            users_id.append(user[0])


        #Запрос на вывод всех операций сотрудников данного филиала
        format_strings = ','.join(['%s'] * len(users_id))
        cursor.execute("SELECT * FROM Operations WHERE worker_id IN (%s)" %format_strings,
                       tuple(users_id))
        operations = cursor.fetchall()


        #Сохранение данных из БД в формате DataFrame для работы с ними
        users_df = pd.DataFrame(columns=["id", "full_name"], data=users)
        operation_df = pd.DataFrame(columns=["id", "counterparty", "worker_id", "type", "status", "status_payment",
                                             "date", "price"], data=operations)

        data = [] #Пустышка для сохранения данных для итогового, дата фрейма с рейтингом
        for user in users_id: #перебираем всех юзеров, что работали в этом месяце
            price = 0.00
            salary = 0.00
            for operation in operation_df[operation_df["worker_id"].isin([user])].to_numpy(): #Создаем объект дата фрейма со всеми операциями пользователя
                price += operation[-1]
                salary += operation[-1] * prices[operation[3]] / 100
            full_name = users_df[users_df["id"].isin([user])]["full_name"].to_numpy()[0] #Вытаскиваем фио сотрудника
            data.append([full_name, round(price, 2), round(salary, 2)])



        df_top_u = pd.DataFrame(columns=["full_name", "price", "salary"], data=data) #Создаем pd серию для вывода
        df_top_u = df_top_u.sort_values(sorting, ascending=False) #Делаем сортировку по выбранному параметру
        cursor.close()
        cnx.close()

        return df_top_u
    else:
        return "Could not connect"


def auth(login: str, password: str) -> bool or None:
    cnx = connect_to_mysql(get_config(), attempts=3) #делаем коннект к БД

    if cnx and cnx.is_connected(): #Если коннект прошел успешно создаем курсор
        cursor = cnx.cursor()

        # Делаем запрос в БД на нахождение пользователя
        query = 'SELECT access FROM Users WHERE login = (%s) AND password = (%s)'

        data = (login, password)

        cursor.execute(query, data)

        back = cursor.fetchall()

        cursor.close()
        cnx.close()
        try:
            return back[0][0] #Возвращаем True если пользователь работодатель, или False если это работник
        except IndexError:
            return None #Возвращаем None если пользователь не найден
    else:
        return "Could not connect"


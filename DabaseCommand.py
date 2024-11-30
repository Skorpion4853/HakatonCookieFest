from Config import get_config
from connect_to_mysql import connect_to_mysql
import pandas as pd

def get_worker_top(cur_user: int, sorting: str) -> str: #Функция для вывода топ 10 работников

    cnx = connect_to_mysql(get_config(), attempts=3) #делаем коннект к БД

    if cnx and cnx.is_connected(): #Если коннект прошел успешно создаем курсор
        cursor = cnx.cursor()
        #создание цен для разных типов операций
        prices = {
            1: 10,
            2: 10,
            3: 10
                  }
        #Вытаскивание данных из БД
        cursor.execute("SELECT id, full_name FROM Users")
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM Operations")
        operation = cursor.fetchall()

        #Сохранение данных из БД в формате DataFrame для работы с ними
        users_df = pd.DataFrame(columns=["id", "full_name"], data=users)
        operation_df = pd.DataFrame(columns=["id", "worker_id", "type", "price"], data=operation)

        uniq_id = operation_df["worker_id"].unique() #Сохранение уникальных id из table операций
        user_full_name = users_df[users_df["id"] == cur_user]['full_name'] #Сохранение ФИО пользователя
        data = [] #Пустышка для сохранения данных для итогового датафрейма с рейтингом

        for user in uniq_id: #перебираем всех юзеров, что работали в этом месяце
            price = 0.00
            salary = 0.00
            for operation in operation_df[operation_df["worker_id"].isin([user])].to_numpy(): #Создаем объект датафрейма со всеми операциями пользователя
                price += operation[3]
                salary += operation[3] * prices[operation[2]] / 100
            full_name = users_df[users_df["id"].isin([user])]["full_name"].to_numpy()[0] #Вытаскиваем фио сотрудника
            print(price, salary)
            data.append([full_name, round(price, 2), round(salary, 2)])



        df_top_u = pd.DataFrame(columns=["full_name", "price", "salary"], data=data) #Создаем pd серию для вывода
        df_top_u = df_top_u.sort_values(sorting, ascending=False) #Делаем сортировку по выбранному параметру

        user_place = -1 #Сохранение позиции в топе у user'a
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
                #Если пользователь не входит в 10 лучших то выводим его место отдельно от остальных
                top_str += ". . .\n"
                top_str += str(place)+ " " + " ".join(map(str,top_user))+ "\n"

        cursor.close()
        cnx.close()

        return top_str
    else:
        return "Could not connect"

def auth(login: str, password: str) -> bool or None:
    cnx = connect_to_mysql(get_config(), attempts=3) #делаем коннект к БД
    print("aaaa")
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

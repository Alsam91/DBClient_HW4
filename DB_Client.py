import psycopg2
from pprint import pprint


class DatabaseClient:
    def __init__(self):
        pass

    def creating_tables(self):  # создание таблиц
        conn = psycopg2.connect(database='clients', user='postgres', password='sav2210x')
        with conn.cursor() as cur:
            cur.execute(
                '''
                DROP TABLE IF EXISTS phone_numbers;
                DROP TABLE  IF EXISTS client;
                ''')
            cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS client(
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(40) NOT NULL UNIQUE,
                    CHECK (email LIKE '%@%' AND email LIKE '%.%' AND email NOT LIKE '% %'));
                CREATE TABLE IF NOT EXISTS phone_numbers(
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER REFERENCES client(id),
                    phone_number VARCHAR(15));
                ''')
            conn.commit()
            print('Таблицы созданы')
        conn.close()

    def add_client(self):  # добавление тестовых клиентов
        conn = psycopg2.connect(database='clients', user='postgres', password='sav2210x')
        with conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO client(first_name, last_name, email)
                VALUES
                    ('Arnold','Schwarzenegger','iron@arny.com'),
                    ('Ronnie','Coleman','lightweight@baby.com'),
                    ('Lou','Ferrigno','big@lou.com')
                    RETURNING *;
                ''')
            conn.commit()
            print('Тестовые клиенты добавлены:')
            pprint(cur.fetchall())
        conn.close()

    def add_client_by_user(self, client_name, client_surname, client_email):  # добавление клиента пользователем программы
        conn = psycopg2.connect(database='clients', user='postgres', password='sav2210x')
        with conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO client(first_name, last_name, email)
                VALUES (%s,%s,%s)
                RETURNING *;
                ''', (client_name, client_surname, client_email))
            conn.commit()
            print('Запись добавлена', cur.fetchall())
        conn.close()

    def add_phone_number(self):  # добавление тестовых номеров телефонов
        conn = psycopg2.connect(database='clients', user='postgres', password='sav2210x')
        with conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO phone_numbers(client_id, phone_number)
                VALUES
                    (1, '984161716551'),
                    (2, '789461596587'),  
                    (2, '789461596534'),
                    (3, '123456789123')
                    RETURNING client_id,phone_number;
                ''')
            conn.commit()
            print('Тестовые номера добавлены:')
            pprint(cur.fetchall())
        conn.close()

    def add_phone_number_by_user(self, client_id, client_phone):  # добавление телефона пользователем программы
        conn = psycopg2.connect(database='clients', user='postgres', password='sav2210x')
        with conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO phone_numbers(client_id, phone_number)
                VALUES (%s,%s)
                RETURNING *;
                ''', (client_id, client_phone))
            conn.commit()
            print('Запись добавлена', cur.fetchall())
        conn.close()

    def change_client_data_by_user(self, table_name, column_name, new_value, client_id):  # изменение данных пользователем программы
        conn = psycopg2.connect(database='clients', user='postgres', password='sav2210x')
        with conn.cursor() as cur:
            cur.execute(
                '''
                UPDATE {}
                SET {} = %s
                WHERE id = %s
                RETURNING *;
                '''.format(table_name, column_name),
                (new_value, client_id))
            conn.commit()
            print('Запись обновлена', cur.fetchall())
        conn.close()

    def delete_phone_by_user(self, deleted_phone):  # удаление номера телефона пользователем программы
        conn = psycopg2.connect(database='clients', user='postgres', password='sav2210x')
        with conn.cursor() as cur:
            cur.execute(
                '''
                DELETE
                FROM phone_numbers
                WHERE phone_number = %s;
                ''', (deleted_phone,))
            conn.commit()
            print('Запись удалена')
        conn.close()

    def delete_client_by_user(self, client_id):  # удаление клиента пользователем программы
        conn = psycopg2.connect(database='clients', user='postgres', password='sav2210x')
        with conn.cursor() as cur:
            cur.execute(
                '''
                DELETE FROM phone_numbers
                WHERE client_id = %s;
                DELETE FROM client 
                WHERE id = %s;
                ''', (client_id, client_id))
            conn.commit()
            print('Клиент удалён')
        conn.close()

    def search_client_by_user(self, search):  # поиск клиента пользователем программы
        conn = psycopg2.connect(database='clients', user='postgres', password='sav2210x')
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT c.id, c.first_name, c.last_name, c.email, phn.phone_number FROM client c
                JOIN phone_numbers phn ON c.id = phn.client_id
                WHERE c.first_name = %s OR c.last_name = %s OR c.email = %s OR phn.phone_number = %s
                order by c.first_name;
                ''', (search, search, search, search))
            conn.commit()
            print(cur.fetchall())
        conn.close()

    def choosing_function(self, function):  # выбор пользовательской функции
        if function == 1:
            print('Выбрана функция добавления клиента')
            return self.add_client_by_user(input('Введите имя: '), input('Введите фамилию: '), input('Введите почту: '))
        elif function == 2:
            print('Выбрана функция добавления номера телефона')
            return self.add_phone_number_by_user(input('Введите ID клиента: '), input('Введите номер телефона: '))
        elif function == 3:
            print('Выбрана функция изменения данных')
            return self.change_client_data_by_user(input('Введите таблицу (client или phone_numbers): '),
                                                   input('Введите изменяемый столбец (first_name, last_name, email '
                                                         'для client или phone_number для phone_numbers): '),
                                                   input('Введите новое значение: '), input('Введите ID клиента: '))
        elif function == 4:
            print('Выбрана функция удаления номера телефона')
            return self.delete_phone_by_user(input('Введите удаляемый номер телефона: '))
        elif function == 5:
            print('Выбрана функция удаления клиента')
            return self.delete_client_by_user(input('Введите ID удаляемого клиента: '))
        elif function == 6:
            print('Выбрана функция поиска клиента')
            return self.search_client_by_user(input('Ведите имя, фамилию, почту или телефон клиента: '))
        else:
            print('Такой функции нет')


if __name__ == '__main__':
    # DatabaseClient().creating_tables()
    # DatabaseClient().add_client()
    # DatabaseClient().add_phone_number()
    DatabaseClient().choosing_function(int(input('Выберите функцию: ')))

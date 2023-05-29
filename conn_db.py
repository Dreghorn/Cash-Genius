import sqlite3
import psycopg2

def delete_row(telegram_id):
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    # Используем параметр %s для безопасного выполнения запроса
    cursor.execute("DELETE FROM players WHERE telegram_id = %s", (telegram_id,))

    # Применяем изменения
    conn.commit()

    # Закрываем соединение
    conn.close()

def player_db(telegram_id, first_name):
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    # Проверяем, есть ли игрок с заданным telegram_id в базе данных
    cursor.execute('SELECT * FROM players WHERE telegram_id = %s', (telegram_id,))
    player = cursor.fetchone()

    if not player:
        # Если игрока нет в базе данных, создаем новую запись
        cursor.execute('INSERT INTO players (telegram_id, first_name, time, relationships_with_family, relationships_with_friends, skills, health, motivation, money, name, year, birja_list, property, earnings, education, monthe) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (telegram_id, first_name, 340, 100, 100, 1, 100, 100, 0, '', 14, '', '', 0, 'no 0 0', 0))
        conn.commit()

        # Получаем информацию о новом игроке из базы данных
        cursor.execute('SELECT * FROM players WHERE telegram_id = %s', (telegram_id,))
        player = cursor.fetchone()

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

    return player

def update_db(telegram_id, event_categories, event_time, event_relationships_with_family, event_relationships_with_friends, event_skills, event_health, event_motivation, event_money, time, event_ubytki):
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    # Получение текущей информации об игроке из базы данных
    cursor.execute('SELECT * FROM players WHERE telegram_id = %s', (telegram_id,))
    player = cursor.fetchone()

    # Инициализация переменных
    time = player[2]
    relationships_with_family = player[3]
    relationships_with_friends = player[4]
    skills = player[5]
    health = player[6]
    motivation = player[7]
    money = player[8]
    earnings = player[13]

    if event_time is not None:
        if event_categories == 'Освіта':
            time += event_time

    if event_relationships_with_family is not None:
        relationships_with_family += event_relationships_with_family

    if event_relationships_with_friends is not None:
        relationships_with_friends += event_relationships_with_friends

    if event_skills is not None:
        skills += event_skills

    if event_health is not None:
        health += event_health

    if event_motivation is not None:
        motivation += event_motivation

    if event_ubytki is not None:
        earnings += event_ubytki

    if event_money is not None:
        money += event_money

    if relationships_with_family > 100:
        relationships_with_family = 100
    if relationships_with_friends > 100:
        relationships_with_friends = 100
    if motivation > 100:
        motivation = 100
    if health > 100:
        health = 100

    # Обновление информации об игроке в базе данных
    cursor.execute(
        '''
        UPDATE players SET money = %s, earnings = %s, time = %s, relationships_with_family = %s, relationships_with_friends = %s, skills = %s, health = %s, motivation = %s WHERE telegram_id = %s
        ''',
        (money, earnings, time, relationships_with_family, relationships_with_friends, skills, health, motivation, telegram_id)
    )

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

def update_db_gb(telegram_id, event_time, event_relationships_with_family, event_relationships_with_friends, event_skills, event_health, event_motivation, event_money):
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    # Получение текущей информации об игроке из базы данных
    cursor.execute('SELECT * FROM players WHERE telegram_id = %s', (telegram_id,))
    player = cursor.fetchone()

    # Инициализация переменных
    time = player[2]
    relationships_with_family = player[3]
    relationships_with_friends = player[4]
    skills = player[5]
    health = player[6]
    motivation = player[7]
    money = player[8]
    earnings = player[13]

    if event_relationships_with_family is not None:
        relationships_with_family += event_relationships_with_family

    if event_relationships_with_friends is not None:
        relationships_with_friends += event_relationships_with_friends

    if event_skills is not None:
        skills += event_skills

    if event_health is not None:
        health += event_health

    if event_motivation is not None:
        motivation += event_motivation

    if event_money is not None:
        money += event_money

    if relationships_with_family > 100:
        relationships_with_family = 100
    if relationships_with_friends > 100:
        relationships_with_friends = 100
    if motivation > 100:
        motivation = 100
    if health > 100:
        health = 100

    # Обновление информации об игроке в базе данных
    cursor.execute(
        '''
        UPDATE players SET time = %s, relationships_with_family = %s, relationships_with_friends = %s, skills = %s, health = %s, motivation = %s, money = %s, earnings = %s WHERE telegram_id = %s
        ''',
        (time, relationships_with_family, relationships_with_friends, skills, health, motivation, money, earnings, telegram_id)
    )

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

def salary_save(robota_salary, robota_time, time, telegram_id):
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    # Обновление информации о зарплате и времени работы игрока в базе данных
    cursor.execute(
        '''
        UPDATE players SET robota_salary = %s, robota_time = %s, time = %s WHERE telegram_id = %s
        ''',
        (robota_salary, robota_time, time, telegram_id)
    )

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

def save_character(money, name, earnings, property, relationships_with_family, relationships_with_friends, health, motivation, telegram_id):
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    # Обновление информации о характеристиках игрока в базе данных
    cursor.execute(
        '''
        UPDATE players SET money = %s, name = %s, earnings = %s, property = %s, relationships_with_family = %s, relationships_with_friends = %s, health = %s, motivation = %s WHERE telegram_id = %s
        ''',
        (money, name, earnings, property, relationships_with_family, relationships_with_friends, health, motivation, telegram_id)
    )

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

def monthe_db(monthe, telegram_id):
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    # Обновление информации о текущем месяце игрока в базе данных
    cursor.execute(
        '''
        UPDATE players SET monthe = %s WHERE telegram_id = %s
        ''',
        (monthe, telegram_id)
    )

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

def save_m_y(monthe, year, time, telegram_id):
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    # Обновление информации о текущем месяце, годе и времени игрока в базе данных
    cursor.execute(
        '''
        UPDATE players SET monthe = %s, year = %s, time = %s WHERE telegram_id = %s
        ''',
        (monthe, year, time, telegram_id)
    )

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

def all_cards():
    # Подключаемся к базе данных
    conn = sqlite3.connect("cash_db.db")

    # Получаем все карточки событий из базы данных
    cards = conn.execute('SELECT * FROM creat_table_event_cards').fetchall()
    return cards

def all_cards_one():
    # Подключаемся к базе данных
    conn = sqlite3.connect("cash_db.db")

    # Получаем все карточки событий из базы данных do 18 year
    cards = conn.execute('SELECT * FROM event_cards_one').fetchall()

    return cards

def save_education(education, telegram_id):
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    # Обновление информации об образовании игрока в базе данных
    cursor.execute(
        '''
        UPDATE players SET education = %s WHERE telegram_id = %s
        ''',
        (education, telegram_id)
    )

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

def saving_card(event, telegram_id):
    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM players WHERE telegram_id = %s', (telegram_id,))
    player = cursor.fetchone()
    event_cards = player[19]
    event_cards = []
    for i in range(len(event)):
        event_cards.append(str(event[i][0]))
    event_cards = ' '.join(event_cards)

    # Обновление информации о картах событий игрока в базе данных
    cursor.execute(
        '''
        UPDATE players SET event_cards = %s WHERE telegram_id = %s
        ''',
        (event_cards, telegram_id)
    )

    # Сохранение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

def open_card(telegram_id, year):
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players WHERE telegram_id = %s', (telegram_id,))
    player = cursor.fetchone()

    cards_id = player[19].split()
    event = []
    conn = sqlite3.connect("cash_db.db")
    for i in range(len(cards_id)):
        if year < 18:
            cards = conn.execute('SELECT * FROM event_cards_one WHERE id = ?', (cards_id[i],)).fetchall()
        else:
            cards = conn.execute('SELECT * FROM creat_table_event_cards WHERE id = ?', (cards_id[i],)).fetchall()
        event += cards
    print(event)
    conn.close()
    return event

def user_choice_save(user_choice, telegram_id):
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE players SET user_choice = %s WHERE telegram_id = %s
    ''', (user_choice, telegram_id))

    conn.commit()
    conn.close()

def update_list(education, earnings, property, robota, money, telegram_id):
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE players SET education = %s, earnings = %s, property = %s, robota = %s, money = %s WHERE telegram_id = %s
    ''', (education, earnings, property, robota, money, telegram_id))

    conn.commit()
    conn.close()

def good_bad_card_one():
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("cash_db.db")

    # Извлекаем все строки из таблицы good_bad_event_cards_one do 18 year
    good_bad_list = conn.execute('SELECT * FROM good_bad_event_cards_one').fetchall()
    # Закрываем соединение с базой данных
    conn.close()
    return good_bad_list

def good_bad_cards():
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("cash_db.db")

    good_bad_list = conn.execute('SELECT * FROM good_bad_event_cards').fetchall()
    # Закрываем соединение с базой данных
    conn.close()
    return good_bad_list

def save_event_count_last_12(event_count_last_12_months, telegram_id):
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE players SET event_count_last_12_months = %s WHERE telegram_id = %s
    ''', (event_count_last_12_months, telegram_id))

    conn.commit()
    conn.close()

def save_robota(robota, telegram_id):
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE players SET robota = %s WHERE telegram_id = %s
    ''', (robota, telegram_id))

    conn.commit()
    conn.close()

def save_earnings(earnings, telegram_id):
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE players SET earnings = %s WHERE telegram_id = %s
    ''', (earnings, telegram_id))

    conn.commit()
    conn.close()

def birja_save(money, birja_list, telegram_id):
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE players SET money = %s, birja_list = %s WHERE telegram_id = %s
    ''', (money, birja_list, telegram_id))

    conn.commit()
    conn.close()

def pension_save(pension_1, telegram_id):
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE players SET pension = %s WHERE telegram_id = %s
    ''', (pension_1, telegram_id))

    conn.commit()
    conn.close()

def money_save(money, telegram_id):
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE players SET money = %s WHERE telegram_id = %s
    ''', (money, telegram_id))

    conn.commit()
    conn.close()

def save_credit(credit_months, balance, telegram_id):
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE players SET credit_months = %s, balance = %s WHERE telegram_id = %s
    ''', (credit_months, balance, telegram_id))

    conn.commit()
    conn.close()

def save_deposit(balance, deposit_month, telegram_id):
    conn = psycopg2.connect(database="cashdb", user="cashgenius", password="lsdS4.eWqQlf!d", host="10.0.0.48", port="13203")
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE players SET deposit_month = %s, balance_deposit = %s WHERE telegram_id = %s
    ''', (deposit_month, balance, telegram_id))

    conn.commit()
    conn.close()



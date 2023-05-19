import psycopg2

def delete_row(telegram_id):
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Используем параметр %s для безопасного выполнения запроса
    query = "DELETE FROM players WHERE telegram_id = %s"
    cursor.execute(query, (telegram_id,))

    # Применяем изменения
    conn.commit()

    # Закрываем соединение
    cursor.close()
    conn.close()

def player_db(telegram_id, first_name):
    # Подключаемся к базе данных
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )

    # Создаем курсор для выполнения операций с базой данных
    cursor = conn.cursor()

    # Проверяем, есть ли игрок с заданным telegram_id в базе данных
    cursor.execute('SELECT * FROM players WHERE telegram_id = %s', (telegram_id,))
    player = cursor.fetchone()

    if not player:
        # Если игрока нет в базе данных, создаем новую запись
        cursor.execute(
            'INSERT INTO players (telegram_id, first_name, time, relationships_with_family, relationships_with_friends, skills, health, motivation, money, name, year, birja_list, property, earnings, education, monthe, robota, pension, event_count_last_12_months, event_cards, event_user_card, user_choice ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (telegram_id, first_name, 340, 100, 100, 0, 100, 100, 0, '', 14, '', '', 0, 'no 0 0', 0, 'Непрацюєте', 0, 0, '', '', '',)
        )
        conn.commit()

        # Получаем информацию о новом игроке из базы данных
        cursor.execute('SELECT * FROM players WHERE telegram_id = %s', (telegram_id,))
        player = cursor.fetchone()

    # Закрываем курсор и соединение с базой данных
    cursor.close()
    conn.close()

    return player

def update_db(telegram_id, event_categories, event_time, event_relationships_with_family, event_relationships_with_friends, event_skills, event_health, event_motivation, event_money, time):
    # Подключаемся к базе данных
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    player = conn.execute('SELECT * FROM players WHERE telegram_id = %s', (telegram_id,)).fetchone()

    # Инициализируем переменные
    time = player[2]
    relationships_with_family = player[3]
    relationships_with_friends = player[4]
    skills = player[5]
    health = player[6]
    motivation = player[7]
    money = player[8]

    if event_time is not None:
        if event_categories == 'Робота' or event_categories == 'Освіта':
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

    if event_money is not None:
        money += event_money

    # Обновляем информацию об игроке в базе данных
    conn.execute('''
    UPDATE players SET time = %s, relationships_with_family = %s, relationships_with_friends = %s, skills = %s, health = %s, motivation = %s, money = %s WHERE telegram_id = %s
    ''', (time, relationships_with_family, relationships_with_friends, skills, health, motivation, money, telegram_id))

    # Сохраняем изменения
    conn.commit()

    conn.close()

def save_character(money, name, earnings, property, telegram_id):
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Используем оператор %s для безопасного выполнения запроса
    cursor.execute("""
        UPDATE players SET money = %s, name = %s, earnings = %s, property = %s WHERE telegram_id = %s
        """, (money, name, earnings, property, telegram_id))

    # Применяем изменения
    conn.commit()

    # Закрываем соединение
    conn.close()

def all_cards():
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Выполняем запрос для получения всех карточек событий
    cursor.execute("SELECT * FROM event_cards")

    # Извлекаем все строки из результата
    cards = cursor.fetchall()

    # Закрываем соединение
    conn.close()

    return cards

def all_cards_one():
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Выполняем запрос для получения всех карточек событий
    cursor.execute("SELECT * FROM event_cards_one")

    # Извлекаем все строки из результата
    cards = cursor.fetchall()

    # Закрываем соединение
    conn.close()

    return cards

def save_education(education, telegram_id):
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Выполняем запрос для обновления поля education
    cursor.execute("UPDATE players SET education = %s WHERE telegram_id = %s", (education, telegram_id))

    # Сохраняем изменения
    conn.commit()

    # Закрываем соединение
    conn.close()

def saving_card(event, telegram_id):
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Получаем текущий список карточек событий игрока
    cursor.execute("SELECT event_cards FROM players WHERE telegram_id = %s", (telegram_id,))
    player = cursor.fetchone()
    event_cards = player[0] if player else ''

    # Формируем новый список карточек событий
    event_cards_list = [str(event[i][0]) for i in range(len(event))]
    event_cards_new = ' '.join(event_cards_list)

    # Обновляем список карточек событий игрока
    cursor.execute("UPDATE players SET event_cards = %s WHERE telegram_id = %s", (event_cards_new, telegram_id))

    # Сохраняем изменения
    conn.commit()

    # Закрываем соединение
    conn.close()

def open_card(telegram_id):
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Получаем список идентификаторов карточек событий игрока
    cursor.execute("SELECT event_cards FROM players WHERE telegram_id = %s", (telegram_id,))
    player = cursor.fetchone()
    cards_id = player[0].split() if player else []

    event = []
    for card_id in cards_id:
        # Получаем карточку события по идентификатору
        cursor.execute("SELECT * FROM event_cards WHERE id = %s", (card_id,))
        cards = cursor.fetchall()
        event += cards

    # Закрываем соединение
    conn.close()

    return event

def user_choice_save(user_choice, telegram_id):
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Обновляем значение поля user_choice в таблице players
    cursor.execute("UPDATE players SET user_choice = %s WHERE telegram_id = %s", (user_choice, telegram_id))

    # Фиксируем изменения
    conn.commit()

    # Закрываем соединение
    conn.close()

def update_list(education, earnings, property, robota, money, telegram_id):
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Обновляем значения полей education, earnings, property, robota, money в таблице players
    cursor.execute("UPDATE players SET education = %s, earnings = %s, property = %s, robota = %s, money = %s WHERE telegram_id = %s",
                   (education, earnings, property, robota, money, telegram_id))

    # Фиксируем изменения
    conn.commit()

    # Закрываем соединение
    conn.close()

def good_bad_cards():
    # Устанавливаем соединение с базой данных
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Извлекаем все строки из таблицы good_bad_event_cards
    cursor.execute("SELECT * FROM good_bad_event_cards")
    good_bad_list = cursor.fetchall()

    # Закрываем соединение с базой данных
    conn.close()

    return good_bad_list

def save_event_count_last_12(event_count_last_12_months, telegram_id):
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Обновляем значение event_count_last_12_months для заданного telegram_id
    cursor.execute("UPDATE players SET event_count_last_12_months = %s WHERE telegram_id = %s", (event_count_last_12_months, telegram_id))

    # Сохраняем изменения
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()

def save_robota(robota, telegram_id):
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Обновляем значение robota для заданного telegram_id
    cursor.execute("UPDATE players SET robota = %s WHERE telegram_id = %s", (robota, telegram_id))

    # Сохраняем изменения
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()

def birja_save(money, birja_list, telegram_id):
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Обновляем значения money и birja_list для заданного telegram_id
    cursor.execute("UPDATE players SET money = %s, birja_list = %s WHERE telegram_id = %s", (money, birja_list, telegram_id))

    # Сохраняем изменения
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()

def pension_save(pension_1, telegram_id):
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Update the pension value for the given telegram_id
    cursor.execute("UPDATE players SET pension = %s WHERE telegram_id = %s", (pension_1, telegram_id))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

def money_save(money, telegram_id):
    conn = psycopg2.connect(
        host="localhost",
        database="test_cash_genius",
        user="postgres",
        password="cash_genius"
    )
    cursor = conn.cursor()

    # Обновляем значения money и birja_list для заданного telegram_id
    cursor.execute("UPDATE players SET money = %s WHERE telegram_id = %s", (money, telegram_id))

    # Сохраняем изменения
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()



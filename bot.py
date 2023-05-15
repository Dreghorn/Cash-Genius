import sqlite3
import random
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import ConversationHandler
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# Определение состояний для ConversationHandler
CHARACTER_CHOICE = 1
CARD_CHOICE = 1
GET_PENSION = 1
# Подключаемся к базе данных
conn = sqlite3.connect('event_cards.db', check_same_thread=False)
time = 340
time_minus = 0
relationships_with_family = 0
relationships_with_friends = 0
skills = 0
health = 0
motivation = 0
money = 0
education_g = ['no', 0]
earnings = 0
monthe = 0
year = 14
event_count_last_12_months = 0
robota = ['', 'Yes', '/quit']
name = ''
property = []
number = []

# Обработчик команды /start
def start(update, context):
    user = update.effective_user
    global first_name
    global telegram_id
    first_name = user.first_name
    telegram_id = user.id

    # Создаем разметку для кнопок
    keyboard = [
        [KeyboardButton('/start')],
        [KeyboardButton('/get_pensoin')],
        [KeyboardButton('/character')],
        [KeyboardButton('/play_card')],
        [KeyboardButton('/send_information')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Отправляем сообщение с кнопками
    update.message.reply_text(text="Выберите действие:", reply_markup=reply_markup)

    # Отправляем дополнительное сообщение
    context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите персонажа и введите сумму желаемой пенсии:")

    # Устанавливаем следующий шаг в диалоге
    return GET_PENSION

def get_pension(update, context):
    message = update.message
    pension = message.text

    # Выполняем необходимые действия с введенной пенсией
    # Например, сохраняем ее в переменной или обрабатываем по своему усмотрению
    global number
    number.append(pension) 
    # Отправляем ответ пользователю
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вы выбрали пенсию: {pension}")

    # Устанавливаем следующий шаг в диалоге
    return ConversationHandler.END



def character(update, context):
    character_1 = ['Адель золота молодь Легкий рівень','Заможна сім’я Багато друзів',5000,'телефон, ноутбук']
    character_2 = ['Євген звичайний хлопець Середній рівень','Звичайна сім’я Декілька друзів',1500,' ноутбук']
    character_3 = ['Михайло бідний хлопець Складний рівень','Бідна неповна сім’я Один друг',400,'телефон']
    character = [character_1, character_2, character_3]
    global list_character
    list_character = character
    
    # Формируем список кнопок
    buttons = [
            InlineKeyboardButton('Легкий рівень', callback_data='1'),
            InlineKeyboardButton('Середній рівень', callback_data='2'),
            InlineKeyboardButton('Складний рівень', callback_data='3')
        ]
    # Создаем разметку для кнопок
    keyboard = [buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляем сообщение с кнопками
    update.message.reply_text(text="Оберіть складність гри:", reply_markup=reply_markup)
    # Запуск ConversationHandler
    return CHARACTER_CHOICE



def character_choice(update, context):
    global name
    global earnings
    global money
    global person
    global property
    user = update.effective_user
    global first_name
    global telegram_id
    first_name = user.first_name
    telegram_id = user.id
    person = 1
    query = update.callback_query
    user_choice = int(query.data)
    if user_choice == 1:
        character = list_character[0]
        character_text = f"""Имя: {character[0]}
            Сем'я: {character[1]}
            Деньги: {character[2]}
            Имущество: {character[3]}
            """
        person = 0
    elif user_choice == 2:
        character = list_character[1]
        character_text = f"""Имя: {character[0]}
            Сем'я: {character[1]}
            Деньги: {character[2]}
            Имущество: {character[3]}
            """
        person = 0
    elif user_choice == 3:
        character = list_character[2]
        character_text = f"""Имя: {character[0]}
            Сем'я: {character[1]}
            Деньги: {character[2]}
            Имущество: {character[3]}
            """
        person = 0
    name = character[0]
    property.append(character[3])
    earnings += character[2]
    money += character[2]
    # Проверяем, есть ли игрок с заданным telegram_id в базе данных
    player = conn.execute('SELECT * FROM players WHERE telegram_id = ?', (telegram_id,)).fetchone()

    if not player:
        # Если игрока нет в базе данных, создаем новую запись
        conn.execute('INSERT INTO players (telegram_id, first_name, time, relationships_with_family, relationships_with_friends, skills, health, motivation, money, games_played, max_money) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (telegram_id, first_name, 100, 100, 100, 0, 100, 100, 0, 0, 0 ))
        conn.commit()

        # Получаем информацию о новом игроке из базы данных
        player = conn.execute('SELECT * FROM players WHERE telegram_id = ?', (telegram_id,)).fetchone()
    
    # Обновляем параметры игрока
    money = player[8] + character[2]


    # Обновляем информацию об игроке в базе данных
    conn.execute('''
    UPDATE players SET money = ? WHERE telegram_id = ?
    ''', (money, telegram_id))

    # Сохраняем изменения
    conn.commit()

    # Закрываем соединение с базой данных
    #conn.close()
    # отправляем информацию о персонаже
    if list_character:
        query.edit_message_text(text=f"Вы выбрали персонажа: {user_choice}. {character_text}")
    # Завершение ConversationHandler
    return ConversationHandler.END

# Создание ConversationHandler
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('character', character)],
    states={
        CHARACTER_CHOICE: [CallbackQueryHandler(character_choice)],
    },
    fallbacks=[],
)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        GET_PENSION: [MessageHandler(Filters.text, get_pension)]
    },
    fallbacks=[CommandHandler('character', character)]
)

# Получаем все карточки событий из базы данных
cards = conn.execute('SELECT * FROM creat_table_event_cards').fetchall()


# Обработчик команды /start
def play_card(update, context):
    
    global monthe
    global year
    global time
    global cards    
    if monthe == 12:
        monthe = 0
        year += 1
        if year == 18:
            time += 120
    else:
        monthe += 1
    
    def event_random():
        global education_g
        event = random.sample(cards, random.randint(1, 3))
        
        if any(card[1] == 'Освіта' for card in event):
            # Проверяем учится ли сейчас
            if education_g[1] == 0:
                # Образование возможно получить только в 7-8 месяцах года
                if monthe == 7 or monthe == 8:
                    return event
                else:
                    return event_random()
            elif education_g[1] == 1:
                return event_random()
        
        return event
    event = event_random()
    global event_cards
    event_cards = event
    

    # Формируем список кнопок
    if len(event) == 1:
            buttons_1 = [
            InlineKeyboardButton(event[0][1], callback_data='1')
        ]
    elif len(event) == 2:
        buttons_1 = [
            InlineKeyboardButton(event[0][1], callback_data='1'),
            InlineKeyboardButton(event[1][1], callback_data='2')
        ]
    elif len(event) == 3:
         buttons_1 = [
            InlineKeyboardButton(event[0][1], callback_data='1'),
            InlineKeyboardButton(event[1][1], callback_data='2'),
            InlineKeyboardButton(event[2][1], callback_data='3')
        ]
    # Создаем разметку для кнопок
    keyboard = [buttons_1]
    reply_markup_play_card = InlineKeyboardMarkup(keyboard)
    # Отправляем сообщение с кнопками
    update.message.reply_text(text="Выберите карточку:", reply_markup=reply_markup_play_card)

# Обработчик выбора карточки
def card_choice(update, context):
    user = update.effective_user
    global first_name
    global telegram_id
    first_name = user.first_name
    telegram_id = user.id
    global property
    global time
    global time_minus
    global relationships_with_family
    global relationships_with_friends
    global skills
    global health
    global motivation
    global money
    global education_g
    global earnings
    query = update.callback_query
    global user_choice
    user_choice = int(query.data)
    global event_
    chat_id = update.effective_chat.id
    # Выбираем карточку в соответствии с выбором пользователя
    if user_choice == 1:
        event_user = event_cards[0]
        event_id, event_categories, event_text, event_time, event_relationships_with_family, \
        event_relationships_with_friends, event_skills, event_health, event_motivation, event_money = event_user

        card_text = f"Событие: {event_text}\n"
        if event_time is not None:
            card_text += f"Время: {event_time}\n"
            
        if event_relationships_with_family is not None:
            card_text += f"Отношения с семьей: {event_relationships_with_family}\n"
            
        if event_relationships_with_friends is not None:
            card_text += f"Отношения с друзьями: {event_relationships_with_friends}\n"
            
        if event_skills is not None:
            card_text += f"Навыки: {event_skills}\n"
            
        if event_health is not None:
            card_text += f"Здоровье: {event_health}\n"
            
        if event_motivation is not None:
            card_text += f"Мотивация: {event_motivation}\n"
            
        if event_money is not None:
            card_text += f"Деньги: {event_money}\n"
            

        #event_cards.pop(0)
    elif user_choice == 2:
        event_user = event_cards[1]
        event_id, event_categories, event_text, event_time, event_relationships_with_family, \
        event_relationships_with_friends, event_skills, event_health, event_motivation, event_money = event_user

        card_text = f"Событие: {event_text}\n"
        if event_time is not None:
            card_text += f"Время: {event_time}\n"
            
        if event_relationships_with_family is not None:
            card_text += f"Отношения с семьей: {event_relationships_with_family}\n"
            
        if event_relationships_with_friends is not None:
            card_text += f"Отношения с друзьями: {event_relationships_with_friends}\n"
            
        if event_skills is not None:
            card_text += f"Навыки: {event_skills}\n"
            
        if event_health is not None:
            card_text += f"Здоровье: {event_health}\n"
            
        if event_motivation is not None:
            card_text += f"Мотивация: {event_motivation}\n"
            
        if event_money is not None:
            card_text += f"Деньги: {event_money}\n"
            
        #event_cards.pop(1)
    elif user_choice == 3:
        event_user = event_cards[2]
        event_id, event_categories, event_text, event_time, event_relationships_with_family, \
        event_relationships_with_friends, event_skills, event_health, event_motivation, event_money = event_user

        card_text = f"Событие: {event_text}\n"
        if event_time is not None:
            card_text += f"Время: {event_time}\n"
            
        if event_relationships_with_family is not None:
            card_text += f"Отношения с семьей: {event_relationships_with_family}\n"
            
        if event_relationships_with_friends is not None:
            card_text += f"Отношения с друзьями: {event_relationships_with_friends}\n"
            
        if event_skills is not None:
            card_text += f"Навыки: {event_skills}\n"
            
        if event_health is not None:
            card_text += f"Здоровье: {event_health}\n"
            
        if event_motivation is not None:
            card_text += f"Мотивация: {event_motivation}\n"
            
        if event_money is not None:
            card_text += f"Деньги: {event_money}\n"
            
        #event_cards.pop(2)
    buttons_2 = [
        InlineKeyboardButton('Принять', callback_data='1'),
        InlineKeyboardButton('Отказаться', callback_data='2')
    ]
    keyboard = [buttons_2]
    reply_markup_card_choice = InlineKeyboardMarkup(keyboard)
    #context.bot.send_message(chat_id=chat_id, text=f"Вы выбрали карточку {user_choice}. {card_text}", reply_markup=reply_markup_card_choice)
    query.edit_message_text(text=f"Вы выбрали карточку {user_choice}. {card_text}", reply_markup=reply_markup_card_choice)
    global user_choice_if
    user_choice_if = user_choice
    return ConversationHandler.END

# Создание ConversationHandler
conversation_handler_card = ConversationHandler(
    entry_points=[CommandHandler('play_card', play_card)],
    states={
        CARD_CHOICE: [CallbackQueryHandler(card_choice)],
    },
    fallbacks=[],
)

def accept_or_refuse(update, context):
    # Подключаемся к базе данных
    conn = sqlite3.connect('event_cards.db')
    user = update.effective_user
    telegram_id = user.id
    player = conn.execute('SELECT * FROM players WHERE telegram_id = ?', (telegram_id,)).fetchone()
    query = update.callback_query
    global user_choice
    global user_choice_if
    global event_user
    if user_choice_if == 1:
        if event_time is not None:
            time_minus += event_time
            
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
            money += event_money + earnings
            earnings += event_money
        
        if health <= 0:
            query.message.reply_text(text="Cмерть")
        elif motivation <= 0:
            query.message.reply_text(text="Cамогубство")

        query.edit_message_text(text="Вы выбрали карточк")
        event_cards.pop(user_choice - 1)
    else:
        query.edit_message_text(text="Next")
    games_played = player[9] + 1
    max_money = max(player[10], money)
    if event_user[1] == 'Освіта':
        education_g.insert(1, 1)
    # Отправляем сообщение с выбранной карточкой
    #update.callback_query.answer()

    # Обновляем информацию об игроке в базе данных
    conn.execute('''
    UPDATE players SET time = ?, relationships_with_family = ?, relationships_with_friends = ?, skills = ?, health = ?, motivation = ?, money = ?, games_played = ?, max_money = ? WHERE telegram_id = ?
    ''', (time, relationships_with_family, relationships_with_friends, skills, health, motivation, money, games_played, max_money, telegram_id))


    # Сохраняем изменения
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()
    
    # Отправляем сообщение с содержимым оставшихся карточек
    for i, card in enumerate(event_cards):
        event_id, event_categories, event_text, event_time, event_relationships_with_family, \
        event_relationships_with_friends, event_skills, event_health, event_motivation, event_money = event_cards[i]

        card_text = f"Событие: {event_text}\n"
        if event_time is not None:
            card_text += f"Время: {event_time}\n"
        if event_relationships_with_family is not None:
            card_text += f"Отношения с семьей: {event_relationships_with_family}\n"
        if event_relationships_with_friends is not None:
            card_text += f"Отношения с друзьями: {event_relationships_with_friends}\n"
        if event_skills is not None:
            card_text += f"Навыки: {event_skills}\n"
        if event_health is not None:
            card_text += f"Здоровье: {event_health}\n"
        if event_motivation is not None:
            card_text += f"Мотивация: {event_motivation}\n"
        if event_money is not None:
            card_text += f"Деньги: {event_money}\n"
        query.message.reply_text(text=card_text)
    # Получаем все карточки событий из базы данных
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('event_cards.db')
    good_bad_list = conn.execute('SELECT * FROM good_bad_event_cards').fetchall()
    # Закрываем соединение с базой данных
    conn.close()
    global event_count_last_12_months
    global monthe
    # Случайное событие не более 4 раз за 12 месяцев и в случайном месяце
    if event_count_last_12_months < 4:
        # С вероятностью 1/3 выпадает случайное событие
        if random.random() < 1/3:
            # Рандом события
            good_bad_cards = random.choice(good_bad_list)
            event_id, event_text, event_time, event_relationships_with_family, \
            event_relationships_with_friends, event_skills, event_health, event_motivation, event_money = good_bad_cards
            card_text = f"ВНИМАНИЕ!!!: {event_text}\n"
            if event_time is not None:
                card_text += f"Время: {event_time}\n"
            if event_relationships_with_family is not None:
                card_text += f"Отношения с семьей: {event_relationships_with_family}\n"
            if event_relationships_with_friends is not None:
                card_text += f"Отношения с друзьями: {event_relationships_with_friends}\n"
            if event_skills is not None:
                card_text += f"Навыки: {event_skills}\n"
            if event_health is not None:
                card_text += f"Здоровье: {event_health}\n"
            if event_motivation is not None:
                card_text += f"Мотивация: {event_motivation}\n"
            if event_money is not None:
                card_text += f"Деньги: {event_money}\n"
            
            query.message.reply_text(card_text)
            #print(random.choice(good_bad_cards)) 
            # Увеличиваем счетчик выпавших событий
            event_count_last_12_months += 1
    else:
        # Счетчик выпавших событий достиг максимального значения, случайное событие не выпадает
        pass

    # Обнуляем счетчик выпавших событий в начале каждого нового года
    if monthe == 0:
        event_count_last_12_months = 0

def quit(update, context):
    global robota
    buttons_3 = [
        [InlineKeyboardButton('Звільнитися?', callback_data='1')]
    ]
    keyboard = InlineKeyboardMarkup(buttons_3)
    update.message.reply_text('Ви бажаєте звільнитися?', reply_markup=keyboard)

def handle_button(update, context):
    query = update.callback_query
    user_choice_quit = query.data
    if user_choice_quit == '1':
        if robota[1] == 'no':
            query.message.reply_text('Ви ще не працюєте)')
        else:
            robota[1] = 'no'
            query.message.reply_text('Ви успішно звільнились')

# Словарь для хранения ценных бумаг и их текущих цен
stocks = {
    'Цінні папери': 100,
    'Apple': 200,
    'Tesla': 150,
    'Samsung': 300,
    'Nokia': 250
}

def birja(update, context):
    chat_id = update.message.chat_id

    # Генерация случайных изменений ценных бумаг
    for stock in stocks:
        # Генерация случайного процента изменения цены
        percent_change = random.uniform(-5, 5)
        # Изменение цены акции
        stocks[stock] += stocks[stock] * percent_change / 100

    # Формирование клавиатуры с доступными действиями
    keyboard = []
    for stock, price in stocks.items():
        keyboard.append([InlineKeyboardButton(f'Купити {stock}', callback_data=f'buy_{stock}')])
        keyboard.append([InlineKeyboardButton(f'Продати {stock}', callback_data=f'sell_{stock}')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправка сообщения с клавиатурой и текущими ценами акций
    message = "Биржа. Выберите действие:"
    for stock, price in stocks.items():
        message += f"\n{stock}: {price}"
    context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)
birja_list = []
# Обработчик callback-запросов для покупки и продажи ценных бумаг
def handle_stock_action(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    action, stock = query.data.split('_')
    stock_price = stocks[stock]
    global birja_list
    if action == 'buy':
        global money
        if money > stock_price:
            birja_list.append(stock)
            context.bot.send_message(chat_id=chat_id, text=f"Ви купили {stock} по ціні {stock_price}")
        else:
            context.bot.send_message(chat_id=chat_id, text="Вам не вистачає грошей")
        
            
    elif action == 'sell':
        if stock in birja_list:
            birja_list.remove(stock)
            context.bot.send_message(chat_id=chat_id, text=f"Ви продали {stock} по ціні {stock_price}")
        else:
            context.bot.send_message(chat_id=chat_id, text="У вас немає таких акцій")
        

    # Обновление сообщения с клавиатурой и текущими ценами акций
    message = "Биржа. Выберите действие:"
    for stock, price in stocks.items():
        message += f"\n{stock}: {price}"
    query.edit_message_text(text=message, reply_markup=query.message.reply_markup)


def send_information(update, context):
    global name
    global year
    global education_g
    global property
    global time
    global health
    global motivation
    global relationships_with_family
    global relationships_with_friends
    global money
    global earnings
    global number
    global robota
    
    information = {
        'имя': name,
        'HB': year,
        'образование': education_g,
        'имущество': ', '.join(property),
        'остаток времени': time,
        'здоровье': health,
        'мотивация': motivation,
        'отношения с семьей': relationships_with_family,
        'отношения с друзьями': relationships_with_friends,
        'баланс': money,
        'доход': earnings,
        'желаемая пенсия': number,
        'робота': ', '.join(robota),
        'Биржа': '/birja'
    }

    information_text = ''
    for key, value in information.items():
        information_text += f'{key}: {value}\n'

    update.message.reply_text(text=information_text)



# Создаем экземпляр Updater и привязываем его к токену бота
updater = Updater(token='6293796882:AAELqkYaPG-WsIt7YqE69B4jX6e5wKW1uuU', use_context=True)

# Создаем обработчики команд и коллбэков
start_handler = CommandHandler('start', start)
character_handler = CommandHandler('character', character)
character_choice_handler = CallbackQueryHandler(character_choice, pattern='character_choice')
play_handler = CommandHandler('play_card', play_card)
card_choice_handler = CallbackQueryHandler(card_choice, pattern='play_card')
accept_or_refuse_handler = CallbackQueryHandler(accept_or_refuse, pattern='accept_or_refuse')
quit_handler = CommandHandler('quit', quit)
birja_handler = CommandHandler('birja', birja)
stock_action_handler = CallbackQueryHandler(handle_stock_action, pattern='^(buy|sell)_')
send_information_handler = CommandHandler('send_information', send_information)


# Регистрируем обработчики в диспетчере
updater.dispatcher.add_handler(conversation_handler)
#updater.dispatcher.add_handler(conversation_handler_card)
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(conv_handler)
updater.dispatcher.add_handler(character_handler)
updater.dispatcher.add_handler(character_choice_handler)
updater.dispatcher.remove_handler(character_choice_handler)
updater.dispatcher.add_handler(play_handler)

updater.dispatcher.add_handler(card_choice_handler)
#updater.dispatcher.remove_handler(card_choice_handler)
updater.dispatcher.add_handler(accept_or_refuse_handler)
updater.dispatcher.add_handler(quit_handler)
updater.dispatcher.add_handler(birja_handler)
updater.dispatcher.add_handler(stock_action_handler)
updater.dispatcher.add_handler(send_information_handler)
# Запускаем бота
updater.start_polling()
updater.idle()

# Закрываем соединение с базой данных
conn.close()


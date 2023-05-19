import random

from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import ConversationHandler
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from conn_post import delete_row, player_db, update_db, money_save, saving_card, open_card, save_character, all_cards_one, all_cards, user_choice_save, save_education, update_list, good_bad_cards, save_event_count_last_12, save_robota, birja_save, pension_save

# Визначення станів для ConversationHandler
CHARACTER_CHOICE = 1
CARD_CHOICE = 1
INPUT_PENSION = 1
DEPOSIT_AMOUNT, DEPOSIT_MONTHS, CREDIT_AMOUNT, CREDIT_MONTHS, PENSION, WISH = range(6)
number = []


def stop_bot(update, context):
    # Остановить бота
    context.bot.stop()


# Оброблювач команди /start
def start(update, context):
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name
    # Створюємо розмітку для кнопок
    keyboard = [
        [KeyboardButton('/start')],
        [KeyboardButton('/play_card')],
        [KeyboardButton('/send_information')],
        [KeyboardButton('/bank')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # Надсилаємо повідомлення з кнопками
    update.message.reply_text(text=f"Привіт {first_name}, я тестова версія Cash Genius. Давай зіграємо. Обери спочатку складність гри /character", reply_markup=reply_markup)
    delete_row(telegram_id)
    # Встановлюємо наступний крок у діалозі
    return INPUT_PENSION

# Обробник команди /character
def character(update, context):
    character_1 = ['Адель золота молодь Легкий рівень','Заможна сім’я Багато друзів',5000,'телефон, ноутбук']
    character_2 = ['Євген звичайний хлопець Середній рівень','Звичайна сім’я Декілька друзів',1500,' ноутбук']
    character_3 = ['Михайло бідний хлопець Складний рівень','Бідна неповна сім’я Один друг',400,'телефон']
    character = [character_1, character_2, character_3]
    global list_character
    list_character = character
    
    # Формуємо список кнопок
    buttons = [
            InlineKeyboardButton('Легкий рівень', callback_data='character_1'),
            InlineKeyboardButton('Середній рівень', callback_data='character_2'),
            InlineKeyboardButton('Складний рівень', callback_data='character_3')
        ]
    # Створюємо розмітку для кнопок
    keyboard = [buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Надсилаємо повідомлення з кнопками
    update.message.reply_text(text="Оберіть складність гри:", reply_markup=reply_markup)
    # Запуск ConversationHandler
    return CHARACTER_CHOICE

# Обробник вибору складності гри
def character_choice(update, context):
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name
    player = player_db(telegram_id, first_name)
    name = player[9]
    earnings = player[13]
    money = player[8]
    property = player[12]
    query = update.callback_query
    user_choice = query.data
    if 'Адель' in name or 'Євген' in name or 'Михайло' in name:
        query.edit_message_text(text="Ви вже обрали складність гри")
    else:
        if user_choice == 'character_1':
            character = list_character[0]
            character_text = f"""Имя: {character[0]}
                Сем'я: {character[1]}
                Деньги: {character[2]}
                Имущество: {character[3]}
                """
            
        elif user_choice == 'character_2':
            character = list_character[1]
            character_text = f"""Имя: {character[0]}
                Сем'я: {character[1]}
                Деньги: {character[2]}
                Имущество: {character[3]}
                """
            
        elif user_choice == 'character_3':
            character = list_character[2]
            character_text = f"""Имя: {character[0]}
                Сем'я: {character[1]}
                Деньги: {character[2]}
                Имущество: {character[3]}
                """
            
        name = character[0]
        property = character[3]
        earnings += character[2]
        money += character[2]
        money = player[8] + character[2]
        name = name + player[9]

        save_character(money, name, earnings, property, telegram_id)
        
        # надсилаємо інформацію про персонажа
        if list_character:
            query.edit_message_text(text=f"Ви вибрали персонажа: {user_choice}. {character_text}")
    # Завершення ConversationHandler    
    updater.dispatcher.remove_handler(character_choice_handler)
    return ConversationHandler.END

# Створюємо ConversationHandler
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('character', character)],
    states={
        CHARACTER_CHOICE: [CallbackQueryHandler(character_choice)],
    },
    fallbacks=[],
)

# Обробник команди /start
def play_card(update, context):
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name
    
    
    player = player_db(telegram_id, first_name)
    monthe = player[15]
    year = player [10]
    time = player[2]
    if year <= 18:
        cards = all_cards_one()
    else:
        cards = all_cards()
    query = update.callback_query
    # Утворимо до списку
    education = player[14].split()
    if monthe == 12:
        monthe = 0
        year += 1
        query.message.reply_text(text="Вітання з Днем Народження)")
        if year == 18:
            time += 120
    else:
        monthe += 1
    
    def event_random(education, monthe):
        event = random.sample(cards, random.randint(1, 3))
        if any(card[1] == 'Освіта' for card in event):
            # Перевіряємо чи вчиться зараз
            if education[1] == '0' and year >= 18:
                # Освіту можна здобути лише у 7-8 місяцях року
                if monthe == 7 or monthe == 8:
                    return event
                else:
                    return event_random(education, monthe)
            elif education[1] == '1':
                if education[2] == '4':
                    education.insert(1, '0')
                    education.insert(0, 'Yes')
                else:
                    education[2] = str(int(education[2] + 1))
                # Повернемо в рядок
                education = ' '.join(education)
                save_education(education, telegram_id)
                return event_random(education, monthe)
        return event
    
    event = event_random(education, monthe)
    saving_card(event, telegram_id)
    

    # Формуємо список кнопок
    if len(event) == 1:
            buttons_1 = [
            InlineKeyboardButton(event[0][1], callback_data='card_1')
        ]
    elif len(event) == 2:
        buttons_1 = [
            InlineKeyboardButton(event[0][1], callback_data='card_1'),
            InlineKeyboardButton(event[1][1], callback_data='card_2')
        ]
    elif len(event) == 3:
         buttons_1 = [
            InlineKeyboardButton(event[0][1], callback_data='card_1'),
            InlineKeyboardButton(event[1][1], callback_data='card_2'),
            InlineKeyboardButton(event[2][1], callback_data='card_3')
        ]
    # Створюємо розмітку для кнопок
    keyboard = [buttons_1]
    reply_markup_play_card = InlineKeyboardMarkup(keyboard)
    # Створюємо розмітку для кнопок
    update.message.reply_text(text="Виберіть картку:", reply_markup=reply_markup_play_card)
    return CARD_CHOICE
event_user = []
# Обробник вибору картки
def card_choice(update, context):
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name
    query = update.callback_query
    event_cards = open_card(telegram_id)
    player = player_db(telegram_id, first_name)
    global event_user
    user_choice = player[21]
    user_choice = query.data
    user_choice_save(user_choice, telegram_id)

    # Вибираємо картку відповідно до вибору користувача
    if user_choice == 'card_1':
        event_user = event_cards[0]
        event_id, event_categories, event_text, event_time, event_relationships_with_family, \
        event_relationships_with_friends, event_skills, event_health, event_motivation, event_money, event_ubytki, event_property_type = event_user


        card_text = f"Подія: {event_text}\n"
        if event_time is not None:
            card_text += f"Час: {event_time}\n"
            
        if event_relationships_with_family is not None:
            card_text += f"Відносини із сім'єю: {event_relationships_with_family}\n"
            
        if event_relationships_with_friends is not None:
            card_text += f"Відносини з друзями: {event_relationships_with_friends}\n"
            
        if event_skills is not None:
            card_text += f"Навички: {event_skills}\n"
            
        if event_health is not None:
            card_text += f"Здоров'я: {event_health}\n"
            
        if event_motivation is not None:
            card_text += f"Мотивація: {event_motivation}\n"
            
        if event_money is not None:
            card_text += f"Гроші: {event_money}\n"

        if event_ubytki is not None:
            card_text += f"Щомісячні витрати: {event_ubytki}\n"
            
    elif user_choice == 'card_2':
        event_user = event_cards[1]
        event_id, event_categories, event_text, event_time, event_relationships_with_family, \
        event_relationships_with_friends, event_skills, event_health, event_motivation, event_money, event_ubytki, event_property_type = event_user


        card_text = f"Подія: {event_text}\n"
        if event_time is not None:
            card_text += f"Час: {event_time}\n"
            
        if event_relationships_with_family is not None:
            card_text += f"Відносини із сім'єю: {event_relationships_with_family}\n"
            
        if event_relationships_with_friends is not None:
            card_text += f"Відносини з друзями: {event_relationships_with_friends}\n"
            
        if event_skills is not None:
            card_text += f"Навички: {event_skills}\n"
            
        if event_health is not None:
            card_text += f"Здоров'я: {event_health}\n"
            
        if event_motivation is not None:
            card_text += f"Мотивація: {event_motivation}\n"
            
        if event_money is not None:
            card_text += f"Гроші: {event_money}\n"

        if event_ubytki is not None:
            card_text += f"Щомісячні витрати: {event_ubytki}\n"
            
    elif user_choice == 'card_3':
        event_user = event_cards[2]
        print(event_user)
        event_id, event_categories, event_text, event_time, event_relationships_with_family, \
        event_relationships_with_friends, event_skills, event_health, event_motivation, event_money, event_ubytki, event_property_type = event_user


        card_text = f"Подія: {event_text}\n"
        if event_time is not None:
            card_text += f"Час: {event_time}\n"
            
        if event_relationships_with_family is not None:
            card_text += f"Відносини із сім'єю: {event_relationships_with_family}\n"
            
        if event_relationships_with_friends is not None:
            card_text += f"Відносини з друзями: {event_relationships_with_friends}\n"
            
        if event_skills is not None:
            card_text += f"Навички: {event_skills}\n"
            
        if event_health is not None:
            card_text += f"Здоров'я: {event_health}\n"
            
        if event_motivation is not None:
            card_text += f"Мотивація: {event_motivation}\n"
            
        if event_money is not None:
            card_text += f"Гроші: {event_money}\n"

        if event_ubytki is not None:
            card_text += f"Щомісячні витрати: {event_ubytki}\n"
                    
    buttons_2 = [
        InlineKeyboardButton('Прийняти', callback_data='aor_1'),
        InlineKeyboardButton('Відмовитись', callback_data='aor_2')
    ]
    keyboard = [buttons_2]
    reply_markup_card_choice = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"Ви обрали картку: {card_text}", reply_markup=reply_markup_card_choice)
    return ConversationHandler.END

# Створюємо ConversationHandler
conversation_handler_card = ConversationHandler(
    entry_points=[CommandHandler('play_card', play_card)],
    states={
        CARD_CHOICE: [CallbackQueryHandler(card_choice)],
    },
    fallbacks=[],
)
# Обробник прийняття рішення
def accept_or_refuse(update, context):
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name
    query = update.callback_query
    user_choice_aor = query.data
    player = player_db(telegram_id, first_name)
    time = player[2]
    skills = player[5]
    health = player[6]
    motivation = player[7]
    money = player[8]
    property = player[12].split()
    earnings = player[13]
    education = player[14].split()
    monthe = player[15]
    robota = player[16]
    global event_user
    user_choice = player[21]
    event_cards = open_card(telegram_id)
    event_id, event_categories, event_text, event_time, event_relationships_with_family, \
    event_relationships_with_friends, event_skills, event_health, event_motivation, event_money, event_ubytki, event_property_type = event_user

    if user_choice_aor == 'aor_1':
        if event_user[1] != 'Робота':
            if money is not None and event_money is not None:
                if money < event_money:
                    query.message.reply_text(text='Вам бракує грошей')
        elif skills is not None and event_skills is not None:
            if skills < event_skills:
                query.message.reply_text(text='Вам бракує навичок')
        elif event_user[1] == 'Робота' and robota == 'Працюєте':
            query.message.reply_text(text="На разі ви вже працюєте, спочатку звільніться через команду /quit потім улаштовуйтесь на нову роботу!")
        elif health <= 0:
            query.message.reply_text(text="Смерть")
            updater.dispatcher.add_handler(stop_handler)
            return stop_bot
        elif motivation <= 0:
            query.message.reply_text(text="Самогубство")
            updater.dispatcher.add_handler(stop_handler)
            return stop_bot
        elif money < 0 :
            query.message.reply_text(text="Банкрутство")
        else:
            update_db(telegram_id, event_categories, event_time, event_relationships_with_family, event_relationships_with_friends, event_skills, event_health, event_motivation, event_money, time)
        event_cards.pop(int(user_choice[5]) - 1)
    else:
        query.edit_message_text(text="Тоді продовжимо")
    if event_user[1] == 'Освіта' and user_choice_aor == 'aor_1':
        education.insert(1, '1')

    education = ' '.join(education)
    if event_user[1] == 'Майно' and user_choice_aor == 'aor_1':
        property.append(event_property_type)
        earnings += event_ubytki
        money += earnings

    property = ' '.join(property)
    if event_user[1] == 'Робота'and user_choice_aor == 'aor_1':
        robota = 'Працюєте'

    update_list(education, earnings, property, robota, money, telegram_id)

    # Відправляємо повідомлення з вмістом карток, що залишилися.
    for i, card in enumerate(event_cards):
        event_id, event_categories, event_text, event_time, event_relationships_with_family, \
        event_relationships_with_friends, event_skills, event_health, event_motivation, event_money, event_ubytki, event_property_type = event_cards[i]

        card_text = f"Подія: {event_text}\n"
        if event_time is not None:
            card_text += f"Час: {event_time}\n"
        if event_relationships_with_family is not None:
            card_text += f"Відносини із сім'єю: {event_relationships_with_family}\n"
        if event_relationships_with_friends is not None:
            card_text += f"Відносини з друзями: {event_relationships_with_friends}\n"
        if event_skills is not None:
            card_text += f"Навички: {event_skills}\n"
        if event_health is not None:
            card_text += f"Здоров'я: {event_health}\n"
        if event_motivation is not None:
            card_text += f"Мотивация: {event_motivation}\n"
        if event_money is not None:
            card_text += f"Деньги: {event_money}\n"
        if event_ubytki is not None:
            card_text += f"Щомісячні витрати: {event_ubytki}\n"
        query.message.reply_text(text=card_text)
    
    good_bad_list = good_bad_cards()

    player = player_db(telegram_id, first_name)
    event_count_last_12_months = player[18]
    # Випадкова подія не більше 4 разів за 12 місяців та у випадковому місяці
    if event_count_last_12_months < 4:
        # З ймовірністю 1/3 випадає випадкова подія
        if random.random() < 1/3:
            # Рандом події
            good_bad_card = random.choice(good_bad_list)
            event_id, event_text, event_health, event_motivation, \
            event_money, event_time, event_relationships_with_family, event_relationships_with_friends, event_skills = good_bad_card
            card_text = f"Увага!!!: {event_text}\n"
            if event_time is not None:
                card_text += f"Час: {event_time}\n"
            if event_relationships_with_family is not None:
                card_text += f"Відносини із сім'єю: {event_relationships_with_family}\n"
            if event_relationships_with_friends is not None:
                card_text += f"Відносини з друзями: {event_relationships_with_friends}\n"
            if event_skills is not None:
                card_text += f"Навички: {event_skills}\n"
            if event_health is not None:
                card_text += f"Здоров'я: {event_health}\n"
            if event_motivation is not None:
                card_text += f"Мотивація: {event_motivation}\n"
            if event_money is not None:
                card_text += f"Гроші: {event_money}\n"
            update_db(telegram_id, event_categories, event_time, event_relationships_with_family, event_relationships_with_friends, event_skills, event_health, event_motivation, event_money, time)
            query.message.reply_text(card_text) 
            # Збільшуємо лічильник подій, що випали
            event_count_last_12_months += 1
            
    else:
        # Лічильник подій досяг максимального значення, випадкова подія не випадає
        pass

    # Обнуляємо лічильник подій, що випали, на початку кожного нового року
    if monthe == 0:
        event_count_last_12_months = 0
    save_event_count_last_12(event_count_last_12_months, telegram_id)
# Обробник команди /quit
def quit(update, context):
    buttons_3 = [
        [InlineKeyboardButton('Звільнитися?', callback_data='quit_1')]
    ]
    keyboard = InlineKeyboardMarkup(buttons_3)
    update.message.reply_text('Ви бажаєте звільнитися?', reply_markup=keyboard)
# Обробник прийняття рішення для звільнення
def handle_button(update, context):
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name
    player = player_db(telegram_id, first_name)
    robota = player[16].split()
    query = update.callback_query
    user_choice_quit = query.data
    if user_choice_quit == 'quit_1':
        if robota[0] == 'Непрацюєте':
            query.edit_message_text('Ви ще не працюєте)')
        else:
            robota = 'Непрацюєте'
            query.edit_message_text('Ви успішно звільнились')
            save_robota(robota, telegram_id)

# Словник для зберігання цінних паперів та їх поточних цін
stocks = {
    'Microsoft': 100,
    'Apple': 200,
    'Tesla': 150,
    'Samsung': 300,
    'Nokia': 250
}

def birja(update, context):
    chat_id = update.message.chat_id

    # Генерація випадкових змін цінних паперів
    for stock in stocks:
        # Генерація випадкового відсотка зміни ціни
        percent_change = random.uniform(-5, 5)
        # Зміна ціни акції
        stocks[stock] += stocks[stock] * percent_change / 100

    # Формування клавіатури з доступними діями
    keyboard = []
    for stock, price in stocks.items():
        keyboard.append([InlineKeyboardButton(f'Купити {stock}', callback_data=f'buy_{stock}')])
        keyboard.append([InlineKeyboardButton(f'Продати {stock}', callback_data=f'sell_{stock}')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Надсилання повідомлення з клавіатурою та поточними цінами акцій
    message = "Біржа. Виберіть дію:"
    for stock, price in stocks.items():
        message += f"\n{stock}: {price}"
    context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

# Обробник callback-запитів для купівлі та продажу цінних паперів
def handle_stock_action(update, context):
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name
    player = player_db(telegram_id, first_name)
    query = update.callback_query
    chat_id = query.message.chat_id
    action, stock = query.data.split('_')
    stock_price = stocks[stock]
    birja_list = player[11]
    if birja_list is not None:
        birja_list = birja_list.split()
    else:
        birja_list = []
    money = player[8]
    if action == 'buy':
        if money > stock_price:
            birja_list.append(stock)
            money -= stock_price
            context.bot.send_message(chat_id=chat_id, text=f"Ви купили {stock} по ціні {stock_price}")
        else:
            context.bot.send_message(chat_id=chat_id, text="Вам не вистачає грошей")
        
            
    elif action == 'sell':
        if stock in birja_list:
            birja_list.remove(stock)
            money += stock_price
            context.bot.send_message(chat_id=chat_id, text=f"Ви продали {stock} по ціні {stock_price}")
        else:
            context.bot.send_message(chat_id=chat_id, text="У вас немає таких акцій")
    birja_list = ' '.join(birja_list)
    birja_save(money, birja_list, telegram_id)
    # Оновлення повідомлення з клавіатурою та поточними цінами акцій
        # Генерація випадкових змін цінних паперів
    for stock in stocks:
        # Генерація випадкового відсотка зміни ціни
        percent_change = random.uniform(-5, 5)
        # Зміна ціни акції
        stocks[stock] += stocks[stock] * percent_change / 100
    message = "Біржа. Виберіть дію:"
    for stock, price in stocks.items():
        message += f"\n{stock}: {price}"
    query.edit_message_text(text=message, reply_markup=query.message.reply_markup)


def bank(update, context):
    keyboard = [
        [KeyboardButton('/make_deposit')],
        [KeyboardButton('/request_credit')],
        [KeyboardButton('/pension')],
        [KeyboardButton('/back')],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # Отправляем сообщение с кнопками
    update.message.reply_text(text="Вітаємо у банку! Навіщо завітали?", reply_markup=reply_markup)

def back(update, context):
    start(update, context)



def make_deposit(update, context):
    update.message.reply_text("Яку суму хочете покласти на депозит?")
    return DEPOSIT_AMOUNT

def deposit_amount(update, context):
    if not update.message.text.isnumeric():
        update.message.reply_text("Введіть коректне число")
        return DEPOSIT_AMOUNT

    # retrieve the deposit amount entered by the user
    deposit_amount = int(update.message.text)
    context.user_data['balance'] = deposit_amount
    update.message.reply_text(f"""Ваш баланс зменшився на {deposit_amount} грн.
    Скільки місяців плануєте зберігати депозит?""")
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name
    player = player_db(telegram_id, first_name)
    money = player[8] - deposit_amount
    money_save(money, telegram_id)
    # move to the next state
    return DEPOSIT_MONTHS
monthly_rate = 0.03
interest_rate = 1
def deposit_months(update, context):
    deposit_month = int(update.message.text)
    # calculate the monthly interest and the final amount
    balance = context.user_data['balance']
    for month in range(deposit_month):
        balance += int(balance * monthly_rate)
    # send a message with the final amount
    update.message.reply_text(f"Ваша сума через {deposit_month} місяців : {balance}")
    return ConversationHandler.END

def deposit_output(update, context, deposit_month, balance, money):
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name
    player = player_db(telegram_id, first_name)
    money = player[8]
    monthe = player[15]
    if monthe == deposit_month:
        update.message.reply_text(f"""Вітаємо! Ви можете забрати гроші, які клали на депозит {deposit_month} місяців назаад.
        Ваш баланс поповнюється на {balance} грн!""")
        money += balance
        money_save(money, telegram_id)
        return ConversationHandler.END   
     

def request_credit(update, context):
    update.message.reply_text("На яку суму хочете взяти кредит?")
    return CREDIT_AMOUNT

def credit_amount(update, context):
    if not update.message.text.isnumeric():
        update.message.reply_text("Введіть коректне число")
        return CREDIT_AMOUNT

    credit_amount = int(update.message.text)
    context.user_data['balance'] = credit_amount
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name
    player = player_db(telegram_id, first_name)
    money = player[8] - credit_amount
    money_save(money, telegram_id)
    update.message.reply_text(f"""Ваш баланс збільшився на {credit_amount} грн.
    На скільки місяців плануєте брати кредит?""")
    # money = money - credit_amount
    return CREDIT_MONTHS

def credit_months(update, context):
    credit_months = int(update.message.text)
    balance = context.user_data['balance']
    interest_rate = credit_months*10
    balance = balance+interest_rate
    
    # send a message with the final amount
    update.message.reply_text(f"Ви маєте повернути {balance} грн через {credit_months} місяців. Кредит під {interest_rate/10}%.")
    # end the conversation
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("bye")
    # end the conversation
    return ConversationHandler.END


deposit_handler = ConversationHandler(
    entry_points=[CommandHandler('make_deposit', make_deposit)],
    states={
        DEPOSIT_AMOUNT: [MessageHandler(Filters.text, deposit_amount)],
        DEPOSIT_MONTHS: [MessageHandler(Filters.text, deposit_months)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

credit_handler = ConversationHandler(
    entry_points=[CommandHandler('request_credit', request_credit)],
    states={
        CREDIT_AMOUNT: [MessageHandler(Filters.text, credit_amount)],
        CREDIT_MONTHS: [MessageHandler(Filters.text, credit_months)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)



def pension(update, context):
    keyboard = [
        [KeyboardButton('/invest_to_my_pension')],
        [KeyboardButton('/back')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text="Яку пенсію ви бажаєте мати після 60 років (по завершенню гри)?", reply_markup=reply_markup)
    return WISH

def invest_to_my_pension(update, context):
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name
    player = player_db(telegram_id, first_name)
    money = player[8]
    message = update.message
    pension = message.text
    player = player_db(telegram_id, first_name)
    pension_1 = player[17] + int(pension)
    pension_save(pension_1, telegram_id)
    update.message.reply_text(f"Скільки хочете зараз відкласти у накопичувальний пенсійний фонд? Ваш баланс {money} грн")
    return PENSION

def no(update, context):
    update.message.reply_text("Що хочете зробити далі?")
    return ConversationHandler.END


pension_handler = ConversationHandler(
    entry_points=[CommandHandler('pension', pension)],
    states={
        WISH: [MessageHandler(Filters.text, invest_to_my_pension)],
        PENSION: [MessageHandler(Filters.text, no)],
    },
    fallbacks=[CommandHandler('no', no)]
)


# Обробник команди /send_information
def send_information(update, context):
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name
    player = player_db(telegram_id, first_name)
    time = player[2]
    relationships_with_family = player[3]
    relationships_with_friends = player[4]
    skills = player[5]
    health = player[6]
    motivation = player[7]
    money = player[8]
    money = player[8]
    name = player[9]
    year = player[10]
    education = player[14]
    education = education.split()
    property = player[12]
    earnings = player[13]
    number = 0
    robota = player[16]
    
    information = {
        'Ім\'я': name[0:5],
        'Років': year,
        'Освіта': education[0],
        'Имущество': property,
        'Час': time,
        'Здоров\'я': health,
        'Мотивация': motivation,
        'Відносини із сім\'єю': relationships_with_family,
        'Відносини з друзями': relationships_with_friends,
        'Баланс': money,
        'Дохід': earnings,
        'Бажана пенсія': number,
        'Робота': robota + ' ' + '/quit',
        'Біржа': '/birja'
    }

    information_text = ''
    for key, value in information.items():
        information_text += f'{key}: {value}\n'

    update.message.reply_text(text=information_text)



# Створюємо екземпляр Updater і прив'язуємо його до токену бота
updater = Updater(token='6293796882:AAELqkYaPG-WsIt7YqE69B4jX6e5wKW1uuU', use_context=True)

# Створюємо обробники команд та коллбеків
stop_handler = CommandHandler('stop', stop_bot)

start_handler = CommandHandler('start', start)

character_handler = CommandHandler('character', character)
character_choice_handler = CallbackQueryHandler(character_choice, pattern='character_choice')

play_handler = CommandHandler('play_card', play_card)
card_choice_handler = CallbackQueryHandler(card_choice, pattern='^card')
accept_or_refuse_handler = CallbackQueryHandler(accept_or_refuse, pattern='^aor')

quit_handler = CommandHandler('quit', quit)
handle_button_handler = CallbackQueryHandler(handle_button, pattern='^quit')

birja_handler = CommandHandler('birja', birja)
stock_action_handler = CallbackQueryHandler(handle_stock_action, pattern='^(buy|sell)_')

send_information_handler = CommandHandler('send_information', send_information)


# Реєструємо оброблювачі в диспетчері
updater.dispatcher.add_handler(conversation_handler)

updater.dispatcher.add_handler(start_handler)

updater.dispatcher.add_handler(conversation_handler)

updater.dispatcher.add_handler(character_handler)
updater.dispatcher.add_handler(character_choice_handler)
updater.dispatcher.remove_handler(character_choice_handler)

updater.dispatcher.add_handler(play_handler)
updater.dispatcher.add_handler(card_choice_handler)

updater.dispatcher.add_handler(conversation_handler_card)
updater.dispatcher.add_handler(accept_or_refuse_handler)

updater.dispatcher.add_handler(quit_handler)
updater.dispatcher.add_handler(handle_button_handler)

updater.dispatcher.add_handler(birja_handler)
updater.dispatcher.add_handler(stock_action_handler)

updater.dispatcher.add_handler(send_information_handler)

updater.dispatcher.add_handler(deposit_handler)
updater.dispatcher.add_handler(credit_handler)
updater.dispatcher.add_handler(pension_handler)

updater.dispatcher.add_handler(CommandHandler('bank', bank))
updater.dispatcher.add_handler(CommandHandler('take_deposit', make_deposit))
updater.dispatcher.add_handler(CommandHandler('deposit_amount', deposit_amount))
updater.dispatcher.add_handler(CommandHandler('deposit_months', deposit_months))
updater.dispatcher.add_handler(CommandHandler('deposit_output'), deposit_output)
updater.dispatcher.add_handler(CommandHandler('cancel', cancel))
updater.dispatcher.add_handler(CommandHandler('request_credit', request_credit))
updater.dispatcher.add_handler(CommandHandler('credit_amount', credit_amount))
updater.dispatcher.add_handler(CommandHandler('credit_months', credit_months))
updater.dispatcher.add_handler(CommandHandler('back', back))
updater.dispatcher.add_handler(CommandHandler('no', no))

# Запускаємо бота
updater.start_polling()
updater.idle()


import telebot
from telebot import types

bot = telebot.TeleBot("7255987525:AAHoQ_EvDOBnOo53wSUahOwX1ilXt_KzIgc")

query_vacancy = ''
is_remote = ''


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Укажи название вакансии:")
        bot.register_next_step_handler(message, get_vacancy_query)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


def get_vacancy_query(message):
    global query_vacancy
    print(message)
    query_vacancy = message.text
    # bot.send_message(message.from_user.id, 'Удалёнка или нет?')
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да, удалёнка', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет, оффлайн', callback_data='no')
    keyboard.add(key_no)
    bot.send_message(message.from_user.id, text='Удалёнка или нет?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    print("call - ", call)
    if call.data == "yes":
        bot.send_message(call.message.chat.id, f'{call.from_user.username}, {query_vacancy}, удалённо')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, f'{call.from_user.username}, {query_vacancy}, не удалённо')


bot.polling(none_stop=True, interval=0)

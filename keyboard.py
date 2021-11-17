import datetime
import telebot



text_about = '''
Что-то очень инетересное по Python
Сcылки на что-то
'''

text_start = '''
Здравствуйте! Вас приветствует бот
салона красоты "Из уродки в красотку".
Чем могу помочь?
'''
text_promo = '''
Сейчас в нашем салоне действуют следющие акции:\n
1. Маникюр на каждый 11 палец - БЕСПЛАТНО!\n
2.\n
3.\n
4.\n
'''
text_services = '''
1. Маникюр 600 рублей (топ мастер 900рублей)\n
2.\n
3.\n
4.\n
'''



class Keyboard:
    def __init__(self, bot):
        self.bot = bot

    def display_start(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Записаться на процедуру')
        markup.row('Записаться к мастеру')
        markup.row('Посмотреть услуги и цены')
        markup.row('Посмотреть акции')
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_start,
                              reply_markup=markup)
    def display_services(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Записаться на процедуру')
        markup.row('Записаться к мастеру')
        markup.row('Посмотреть акции')
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_services,
                              reply_markup=markup)
    def display_promo(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Записаться на процедуру')
        markup.row('Записаться к мастеру')
        markup.row('Посмотреть услуги и цены')
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_promo,
                              reply_markup=markup)

    def display_procedures(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('на маникюр')
        markup.row('на педикюр')
        markup.row('на наращивание ресниц')
        markup.row('эпиляцию')
        text_procedures='Отлично! На какую процедуду хотите записаться?'
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_procedures,
                              reply_markup=markup)

    def display_do_you_want_master(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Да')
        markup.row('Нет')
        text_master='Хотите записаться к определенному мастеру?'
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_master,
                              reply_markup=markup)
    def display_of_masters(self, message, list_of_masters):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        for master in list_of_masters:
            markup.row(master)
        text_choose='Выберете мастера:'
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_choose,
                              reply_markup=markup)
    def display_last(self, message, procedure,date):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Записаться на процедуру')
        markup.row('Записаться к мастеру')
        markup.row('Посмотреть услуги и цены')
        markup.row('Посмотреть акции')
        text_choose='Вы записаны на процедуру {} на {}. Ждем Вас!'.format(procedure, date)
        self.bot.send_message(chat_id=message.from_user.id,
                              text=text_choose,
                              reply_markup=markup)
import telebot
import psycopg2 as ps
from keyboard import Keyboard
import telegramcalendar as tgc



# ваш токен
TOKEN = '2126834952:AAHnqsA1jtlibXDBVb_MENfJq4YI3PG6Fbs'  # Нурия
# пароль, чтобы залогиниться как админ
bot = telebot.TeleBot(TOKEN)
keyboard = Keyboard(bot)
@bot.message_handler(commands=['start'])
def start_message(message):
   keyboard.display_start(message)


bot.polling()
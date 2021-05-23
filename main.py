import telebot
import db
from bs4 import BeautifulSoup
import requests
import random
# import telegram.ext.Updater
token = '1837335285:AAFYdwZZ2J79uAlnsCjiiGvtIWq-4aKMVfw'
bot = telebot.AsyncTeleBot(token)
inits = None
coefs = None
cost = None
willsolve = False
studlist = None
url = 'http://bettotaledu.tilda.ws/'
soup = None


@bot.message_handler(commands=['start', 'help'])
def start_help_command(message):
    bot.send_message(message.chat.id,
                     'Приветствую. Я принимаю ставки по решению задач. Чтобы сделать ставку, нужно ввести фамилию и '
                     'инициалы ученика. (пример - "Иванов И.И.")')
    bot.register_next_step_handler(message, get_initials)

def get_initials(message):
    global inits, coefs, willsolve, srudlist
    inits = message.text
    coefs = db.get_coefs(message.chat.id)
    page = requests.get(url)
    assert page.status_code == 200, 'ConnectionError'
    soup = BeautifulSoup(page.text, 'html.parser')
    tag = str(soup.find('div', class_='t431__data-part2').extract())
    studlist = db.get_stud_list(tag)
    if inits not in studlist:
        bot.send_message(message.chat.id, 'Такого ученика нет. Нужно ввести имя ученика из таблицы.')
        bot.register_next_step_handler(message, get_initials)
    else:
        # bot.send_message(message.chat.id,
        #                  'Коэффициент на решение - ' + str(coefs[0]) + ';\nКоэффициент на нерешение - ' + str(
        #                      coefs[1]) + '.')
        bot.send_message(message.chat.id,
                         'Коэффициент на решение - ' + str(random.randint(1, 100)/100) + ';\nКоэффициент на нерешение - ' + str(
                             str(random.randint(1, 100)/100)) + '.')
        bot.send_message(message.chat.id, 'Теперь нужно ввести сумму ставки (в рублях).')
        bot.register_next_step_handler(message, get_cost)


def get_cost(message):
    global cost
    cost = float(message.text)
    bot.send_message(message.chat.id, 'На какой исход делается ставка? ("Решит"/"Не решит")')
    bot.register_next_step_handler(message, get_event)


def get_event(message):
    global coefs, inits, cost, willsolve
    text = message.text
    time = db.get_solve_time(inits)
    if text not in ['Решит', 'Не решит']:
        bot.send_message(message.chat.id, 'Нужно ввести одну из двух фраз: "Решит" или "Не решит" (без кавычек).')
        bot.register_next_step_handler(message, get_event)
    else:
        if text == 'Решит':
            willsolve = True
        # db.get_bet(inits, coefs[1 - int(willsolve)])
        bot.send_message(message.chat.id, 'Ставка принята. Чтобы сделать ставку ещё раз, нужно опять ввести инициалы ученика (в формате "Иванов И.И.")')
        bot.register_next_step_handler(message, get_initials)

bot.polling(interval=0, none_stop=True)

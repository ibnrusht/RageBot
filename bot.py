import config
import telebot
from SQLighter import SQLighter
import random
import utils
from telebot import types

bot = telebot.TeleBot(config.token)


# echo-bot
#@bot.message_handler(content_types=["text"])
#def repeat_all_messages(message):
#    bot.send_message(message.chat.id, message.text)


commands = {'start': 'Hello message',
            'help': 'Gives you information about the available commands',
            'game': 'A guess the melody game'}

# Guess the melody
@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    if message.chat.type == "private":
        bot.send_message(cid, 'Hi, fuckface.')
    if message.chat.type == "group":
        bot.send_message(cid, 'Hello, motherfuckers.')

@bot.message_handler(commands=['help'])
def help(message):
    cid = message.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

@bot.message_handler(commands=['game'])
def game(message):
    cid = message.chat.id
    db_worker = SQLighter(config.database_name)
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    markup = utils.generate_markup(row[2],row[3])
    if message.chat.type == "private":
        bot.send_voice(cid, row[1], reply_markup=markup)
        utils.set_user_game(cid, row[2])
    elif message.chat.type == "group":
        bot.send_voice(cid, row[1], reply_markup=markup, reply_to_message_id=message.message_id)
        utils.set_user_game(cid, row[2])
    db_worker.close()

@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    cid = message.chat.id
    answer = utils.get_answer_for_user(cid)
    if not answer:
        bot.send_message(cid, 'Чтобы начать игру, выберите команду /game')
    else:
        keyboard_hider = types.ReplyKeyboardRemove()
        if message.text == answer:
            bot.send_message(cid, 'Верно!', reply_markup=keyboard_hider, reply_to_message_id=message.message_id)
        else:
            bot.send_message(cid, 'Увы, Вы не угадали. Попробуйте ещё раз!', reply_markup=keyboard_hider, reply_to_message_id=message.message_id)
        utils.finish_user_game(cid)

if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.polling(none_stop=True)
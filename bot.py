import config
import telebot
from SQLighter import SQLighter
import random
import utils
import imageio
from telebot import types
import os

bot = telebot.TeleBot(config.token)


# echo-bot
#@bot.message_handler(content_types=["text"])
#def repeat_all_messages(message):
#    bot.send_message(message.chat.id, message.text)


commands = {'start': 'Hello message',
            'help': 'Gives you information about the available commands',
            'game': 'A guess the melody game',
            'barrel': 'Make a barrel roll'}

# Guess the melody
@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    chat_type = message.chat.type
    if chat_type == "private":
        bot.send_message(cid, 'Hi, fuckface.')
    if (chat_type == "group")|(chat_type == "supergroup"):
        bot.send_message(cid, 'Hello, motherfuckers.')


@bot.message_handler(commands=['help'])
def help(message):
    cid = message.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

@bot.message_handler(commands=['barrel'])
def barrel(message):
    cid = message.chat.id
    uid = message.from_user.id
    uname = message.from_user.username
    db_worker = SQLighter(config.users_db)
    user_photo = bot.get_user_profile_photos(uid,0,1) # getting user profile photo
    fid = user_photo.photos[0][0].file_id # getting user profile photo id
    if db_worker.check_user(uid): # if user exists
        if db_worker.check_barrel(uid): # if barrel_roll-gif already exists and uploaded
            bar_id = db_worker.get_barrel(uid) # getting file id
            bot.send_document(cid,bar_id) # sending barrel_roll-gif
        else:
            file_path = bot.get_file(fid).file_path # getting file_path of users profile image
            utils.make_barrel_roll(file_path) # making gif-animation
            barrel_roll = open('barrel_roll.gif', 'rb')
            msg = bot.send_document(cid,barrel_roll) # sending gif-animation to chat
            barrel_roll_id = msg.document.file_id # saving gif-animation file id
            db_worker.add_barrel(uid,barrel_roll_id) # saving file-id in database
    else:
        db_worker.add_user(uid,uname,fid)
        file_path = bot.get_file(fid).file_path
        utils.make_barrel_roll(file_path)
        barrel_roll = open('barrel_roll.gif', 'rb')
        msg = bot.send_document(cid, barrel_roll)
        barrel_roll_id = msg.document.file_id
        db_worker.add_barrel(uid, barrel_roll_id)
        #os.remove('barrel_roll.gif')

@bot.message_handler(commands=['game'])
def game(message):
    cid = message.chat.id
    uid = message.from_user.id
    chat_type = message.chat.type
    db_worker = SQLighter(config.database_name)
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    markup = utils.generate_markup(row[2],row[3])
    if chat_type == "private":
        bot.send_voice(cid, row[1], reply_markup=markup)
        utils.set_user_game(cid, row[2])
    elif (chat_type == "group")|(chat_type == "supergroup"):
        bot.send_voice(cid, row[1], reply_markup=markup, reply_to_message_id=message.message_id)
        utils.set_user_game(uid, row[2])
    db_worker.close()

@bot.message_handler(func=lambda message: message.content_type == 'new_chat_members')
def new_chat_member(message):
    pass



@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    cid = message.chat.id
    uid = message.from_user.id
    if 'петрос' in message.text.lower(): # если встречается слово "петрос"
        anech = utils.petros()
        bot.send_message(cid, anech)
    else:
        pass
    if utils.check_user_in_game(uid):
        answer = utils.get_answer_for_user(uid)
        keyboard_hider = types.ReplyKeyboardRemove()
        if message.text == answer:
            bot.send_message(cid, 'Верно!', reply_markup=keyboard_hider, reply_to_message_id=message.message_id)
        else:
            bot.send_message(cid, 'Увы, Вы не угадали. Попробуйте ещё раз!', reply_markup=keyboard_hider, reply_to_message_id=message.message_id)
        utils.finish_user_game(uid)
    else:
        pass



if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.polling(none_stop=True)
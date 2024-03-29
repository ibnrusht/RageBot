import shelve
import urllib3
from imageio import *
import config as config
import imageio
import shutil
import os
import random
from SQLighter import SQLighter
from config import shelve_name, database_name
from telebot import types
from random import shuffle
from PIL import Image

def count_rows():
    """
    It counts rows in database
    :return: rows number
    """
    db = SQLighter(database_name)
    rowsnum = db.count_rows()
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] = rowsnum


def get_rows_count():
    """
    it gets the rouws number from shelve
    :return: int, rows number
    """
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['rows_count']
    return rowsnum

def set_user_game(user_id, estimated_answer):
    """
    Set user as gamer and save his answer
    :param user_id: id of user
    :param estimated_answer: right answer from DB
    :return:
    """
    with shelve.open(shelve_name) as storage:
        storage[str(user_id)] = estimated_answer

def finish_user_game(user_id):
    """
    Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    :param user_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        del storage[str(user_id)]

def check_user_in_game(user_id):
    with shelve.open(shelve_name) as storage:
        try:
            tmp = storage[str(user_id)]
        except KeyError:
            tmp = 0
    return tmp


def get_answer_for_user(user_id):
    """
    Getting right answer
    :param user_id: user id
    :return: (str) right answer / None
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(user_id)]
            return answer
        # Если человек не играет, ничего не возвращаем
        except KeyError:
            return None

def generate_markup(right_answer, wrong_answer):
    """
    Creates custom keyboard
    :param right_answer: right answer
    :param wrong_answer: wrong answer
    :return: object custom keyboard
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, selective=True)
    all_answers = '{},{}'.format(right_answer,wrong_answer)
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)

    shuffle(list_items)
    for item in list_items:
        markup.add(item)
    return markup

def make_barrel_roll(file_path):
    """
    Making rotated image and save it as gif-file
    :param file_path: string
    :return: file in storage
    """
    http = urllib3.PoolManager()
    url = 'https://api.telegram.org/file/bot{0}/{1}'.format(config.token,file_path)
    with http.request('GET', url, preload_content=False) as r, open('avatar.jpg', 'wb') as out_file:
        shutil.copyfileobj(r, out_file)
    im1 = Image.open('avatar.jpg')
    im = []
    for i in range(-3,4): #
        tmp = im1.rotate(i*45)
        tmp.save(str(i)+'.JPEG', "JPEG")
    positions = [x for x in range(0, 4)] + [x for x in range(2, -4, -1)] + [x for x in range(-3,1)]
    images = []
    for i in positions:
        images.append(imageio.imread(str(i)+'.JPEG'))
    imageio.mimsave('barrel_roll.gif', images, duration = 0.5)
    for i in range(-3,4):
        os.remove('{0}.JPEG'.format(str(i)))
    os.remove('avatar.jpg')

def petros():
    """
    Send random aneqdotue from nech.txt file
    :param message: shoud consists string "petros"
    :return:
    """
    with open("petros\\nech.txt","r") as f:
        anech = f.read().split('\n\n')
        aneque = anech[random.randint(2,len(anech))]
    return aneque

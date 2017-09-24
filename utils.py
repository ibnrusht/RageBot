import shelve
from SQLighter import SQLighter
from config import shelve_name, database_name
from telebot import types
from random import shuffle

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



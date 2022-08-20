import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Getting all entries """
        with self.connection:
            return self.cursor.execute('SELECT * FROM music').fetchall()

    def select_single(self, rownum):
        """ Getting entry with rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM music WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM music').fetchall()
            return len(result)

    def check_user(self, user_id):
        with self.connection:
            check_table = self.cursor.execute("""SELECT count(name)
            FROM sqlite_master
            WHERE type='table'""").fetchall()
            if check_table[0][0]:
                return True if \
                     self.cursor.execute('SELECT * FROM users WHERE\
                        user_id = '+str(user_id)).fetchall() else False
            else:
                self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    avatar_file_id INTEGER,
                    barrel_roll_id INTEGER
                    );""").fetchall()
                return False

    def add_user(self, user_id, username, avatar_file_id):
        with self.connection:
            vls = [str(user_id), username, avatar_file_id]
            self.cursor.execute("""INSERT INTO users
            (user_id, username, avatar_file_id)
            VALUES (?, ?, ?)""", vls)

    def check_barrel(self,user_id):
        """
        Checking barrel_roll-gis existance
        :param user_id: int, user_id
        :return: bool
        """
        with self.connection:
            tmp = self.cursor.execute('SELECT barrel_roll_id FROM users WHERE user_id = '+str(user_id)).fetchall()
            return True if tmp[0][0] else False

    def add_barrel(self,user_id,barrel_roll_id):
        """
        Adding entry about barrel_roll-gif file id
        :param user_id: int
        :param barrel_roll_id: int
        """
        with self.connection:
            vls = [barrel_roll_id, user_id]
            self.cursor.execute('UPDATE users SET barrel_roll_id = ? WHERE user_id = ?', vls)

    def get_barrel(self,user_id):
        """
        Getting barrel_roll-gif file id
        :param user_id: int
        :return: int, barrer-roll file id
        """
        with self.connection:
            bar_id = self.cursor.execute("""SELECT barrel_roll_id
            FROM users 
            WHERE user_id = """+str(user_id)).fetchall()
            return bar_id[0][0]

    def close(self):
        self.connection.close()



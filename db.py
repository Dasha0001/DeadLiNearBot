import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли пользователь в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))



    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_record(self, user_id, operation, value):
        """Создаем запись о дедлайне"""
        self.cursor.execute("INSERT INTO `records` (`users_id`, `operation`, `value`) VALUES (?, ?, ?)",
            (self.get_user_id(user_id),
            operation == "+",
            value))
        return self.conn.commit()

    def delete_record(self, user_id, operation, value):
        """Удаляем запись о дедлайне"""

        self.cursor.execute("DELETE FROM `records` WHERE value=?",(value,) )
        return self.conn.commit()

    def get_records(self, user_id):
        result = self.cursor.execute("SELECT `value`   FROM `records` WHERE `users_id` = ? ",(self.get_user_id(user_id),))
        return result.fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
# -*- coding: utf-8 -*-
import config
import sqlite3
import telebot
import time

class SQLite:

    def __init__(self, database):
        self.connection = sqlite3.connect(database, isolation_level=None, timeout=5000)
        self.cursor = self.connection.cursor()

    def new_state(self, chat_id, state):
        self.cursor.execute('REPLACE INTO users (user_id, state) VALUES (' + str(chat_id) + ', ' + str(state) + ')')

    # def create_new_table(self, table_name):
    #     self.cursor.execute('CREATE TABLE ' + table_name + '(some_column)')

    def close(self):
        self.connection.close()

bot = telebot.TeleBot(config.token)

about_string = 'Этот бот попытается помочь вам подготовиться к сдаче IELTS.'

@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, about_string)

@bot.message_handler(commands=['saymyname'])
def send_user_first_name(message):
    bot.send_message(message.chat.id, 'Hi, ' + message.chat.first_name + '!')

@bot.message_handler(commands=['start'])
def start_chat(message):
    bot.send_message(message.chat.id, 'Привет!')
    db_worker = SQLite(config.database_name)
    db_worker.new_state(message.chat.id, 0)
    db_worker.close()


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
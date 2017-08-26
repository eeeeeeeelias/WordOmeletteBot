# -*- coding: utf-8 -*-
import config
import sqlite3
import telebot
import time

class SQLite:

    def __init__(self, database):
        self.connection = sqlite3.connect(database, isolation_level=None, timeout=5000)
        self.cursor = self.connection.cursor()

    def check_if_user_is_familiar(self, chat_id):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = " + str(chat_id))
        result = self.cursor.fetchone()
        return result[0]

    def set_new_state(self, chat_id, word):
        if (state == 0):
            self.cursor.execute("REPLACE INTO users (user_id, user_state, words_number) VALUES (" + str(chat_id) + ", " + str(state) + ", 0)")

    def check_if_word_is_familiar(self, chat_id, word):
        self.cursor.execute("SELECT COUNT(*) FROM english_words WHERE english_words.word = \"" + word + "\" AND english_words.user_id = " + str(chat_id))
        result = self.cursor.fetchone()
        return result[0]

    def add_new_word(self, chat_id, word, appearance_date):
        # return "INSERT INTO english_words (word, appearance_date, user_id) VALUES (\"" + word + "\", " + str(appearance_date) + ", " + str(user_id) + ")"
        self.cursor.execute("INSERT INTO english_words (word, appearance_date, user_id) VALUES (\'" + word + "\', " + str(appearance_date) + ", " + str(chat_id) + ")")

    # def create_new_table(self, table_name):
    #     self.cursor.execute("CREATE TABLE " + table_name + "(some_column)")


    def close(self):
        self.connection.close()

bot = telebot.TeleBot(config.token)

about_string = "Этот бот поможет вам учить иностранные слова."

@bot.message_handler(commands=["about"])
def send_about(message):
    bot.send_message(message.chat.id, about_string)

# @bot.message_handler(commands=["newword"])
@bot.message_handler(regexp="\/newword [A-Za-z \']+")
def add_new_word(message):
    new_word = message.text[9:]
    db_worker = SQLite(config.db_name)
    # bot.send_message(message.chat.id, "result[0] = " + str(db_worker.check_if_word_is_familiar(message.chat.id, new_word)))
    if (db_worker.check_if_word_is_familiar(message.chat.id, new_word)):
        bot.send_message(message.chat.id, "Это слово уже есть в базе!")
    else:
        bot.send_message(message.chat.id, "Слово успешно добавлено!")
        db_worker.add_new_word(message.chat.id, new_word, message.date)
    db_worker.close()

@bot.message_handler(commands=["saymyname"])
def send_user_first_name(message):
    bot.send_message(message.chat.id, "Hi, " + message.chat.first_name + "!")

@bot.message_handler(commands=["start"])
def start_chat(message):
    db_worker = SQLite(config.db_name)
    if (db_worker.check_if_user_is_familiar(message.chat.id)):
        bot.send_message(message.chat.id, "Мы уже знакомы!")
    else:
        db_worker.set_new_state(message.chat.id, 0)
        bot.send_message(message.chat.id, "Привет, " + message.chat.first_name + "! Кажется, мы ещё не знакомы.")
    db_worker.close()

@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_msg(message):
    bot.send_message(message.chat.id, "Простите, наш бот это не понимает :(")

bot.polling()
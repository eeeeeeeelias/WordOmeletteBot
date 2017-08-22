# -*- coding: utf-8 -*-
import config
import sqlite3
import telebot
import time

conn = sqlite3.connect('user_states.db')
cursor = conn.cursor()

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
    cursor.execute('INSERT INTO users (user_id, state) VALUES (' + str(message.chat.id) + ', 0)')

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
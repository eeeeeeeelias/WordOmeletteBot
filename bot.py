# -*- coding: utf-8 -*-
import config
import telebot
import time

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['saymyname'])
def send_user_first_name(message):
    bot.send_message(message.chat.id, 'Hi, ' + message.chat.first_name + '!')

# @bot.message_handler(commands=['about'])
# def 

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
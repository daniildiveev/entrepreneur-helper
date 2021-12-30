import telebot
from config import *
from text_handling import search_for_relevant_part_in_json

bot = telebot.TeleBot(api)

@bot.message_handler(commands=['start'])
def welcome_message(message):
	bot.send_message(message.chat.id, 
		'Hello, this is a bot, that helps you with your law practice')

@bot.message_handler(content_types=['text'])
def send_links(message):
	query = message.text

	best_part = search_for_relevant_part_in_json(path_to_json, query)

	bot.send_message(message.chat.id, best_part)

if __name__ == '__main__':
	print('Bot started!')
	bot.polling()
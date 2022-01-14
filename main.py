import telebot
from config import *
from transformers import pipeline
from db_management import *

bot = telebot.TeleBot(API)
'''qa = pipeline(task='question-answering', 
			  model='AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru',
			  tokenizer='AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru')'''

@bot.message_handler(commands=['start'])
def welcome_message(message):
	bot.send_message(message.chat.id, 
		'Hello, this is a bot, that helps you with your law practice')

@bot.message_handler(content_types=['text'])
def send_links(message):
	query = message.text
	user = message.from_user.id
	user_stats = get_user_stats(USER_DATABASE, user)

	if not user_stats:
		add_user_record(USER_DATABASE, user, 1)
	else:
		update_users_table(USER_DATABASE, user)

	best_part = "Mistborn is a series of epic fantasy novels written by American author Brandon Sanderson."#search_for_relevant_part_in_json(path_to_json, query)

	'''reply = qa({
		"context": 'Даня любит играть в доту.',
		"question": 'Что любит делать Даня?'
	})['answer']'''

	reply = 'ti loch'

	add_request_record(REQUEST_DATABASE, user, query)
	bot.send_message(message.chat.id, reply)

if __name__ == '__main__':
	print('Bot started!')
	bot.polling()
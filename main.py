import telebot
from config import *
from parser import *
from text_handling import *

bot = telebot.TeleBot(api)

@bot.message_handler(commands=['start'])
def welcome_message(message):
	bot.send_message(message.chat.id, 
		'Hello, this is a bot, that helps you with your law practice')

@bot.message_handler(content_types=['text'])
def send_links(message):
	url = 'http://www.consultant.ru/search/?q='
	links = []

	query = message.text
	processor = TextPreprocessing([query])
	query_preprocessed = processor.full_preprocessing()[0]

	for word in query_preprocessed.split():
		url += f'{word}+'
	url = url[:-1]

	print(url)

	while len(links) == 0:
		links = parse_search_links(url)[:num_links_to_get]

	texts = parse_texts(links)

	reply = f'Cсылки по запросу: {query}\n'

	for i, text in enumerate(texts):
		reply += f'{i+1}.{text}} \n'

	bot.send_message(message.chat.id, reply)

if __name__ == '__main__':
	print('Bot started!')
	bot.polling()
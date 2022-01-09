import telebot
from config import *
#from text_handling import search_for_relevant_part_in_json
#from simpletransformers.question_answering import QuestionAnsweringModel
#from simpletransformers.question_answering import QuestionAnsweringArgs
'''
model_args = QuestionAnsweringArgs()
model_args.n_best_size = 1

model = QuestionAnsweringModel(
    "roberta",
    "deepset/roberta-base-squad2",
	use_cuda = False,
    args=model_args)'''

from transformers import pipeline

qa = pipeline(task='question-answering', 
			  model='AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru',
			  tokenizer='AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru')

@bot.message_handler(commands=['start'])
def welcome_message(message):
	bot.send_message(message.chat.id, 
		'Hello, this is a bot, that helps you with your law practice')

@bot.message_handler(content_types=['text'])
def send_links(message):
	query = message.text

	best_part = "Mistborn is a series of epic fantasy novels written by American author Brandon Sanderson."#search_for_relevant_part_in_json(path_to_json, query)

	'''prediction, _ = model.predict([
		{
			"context" : best_part,
			"qas":[
				{
					"question" : query,
					"id" : 0
				}
			]
		}
	])

	bot.send_message(message.chat.id, prediction[0]["answer"][0])'''

	reply = qa({
		"context": 'Даня любит играть в доту.',
		"question": 'Что любит делать Даня?'
	})['answer']

	bot.send_message(message.chat.id, reply)

if __name__ == '__main__':
	print('Bot started!')
	bot.polling()
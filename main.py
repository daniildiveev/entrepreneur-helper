import telebot
from config import *
from db_management import *
from parsers import multiple_parse
from text_handling import *
from nn import *

bot = telebot.TeleBot(API)
qa = get_model_for_qa(QA_MODEL)
sentence_model = get_model_for_sentence_similarity(SENTENCE_MODEL)

@bot.message_handler(commands=['start'])
def welcome_message(message):
	bot.send_message(message.chat.id, 
		'Hello, this is a bot, that helps you with your law practice')


@bot.message_handler(content_types=['text'])
def send_reply(message):
    query = message.text
    user = message.from_user.id
    user_stats = get_user_stats(USER_DATABASE, user)

    if not user_stats:
        add_user_record(USER_DATABASE, user, 1)
    else:
        update_users_table(USER_DATABASE, user)

    texts = multiple_parse(query)

    preprocessing = TextPreprocessing(texts)
    texts = preprocessing.preprocess_html()

    best_part = get_most_similar_part(sentence_model, query, texts)
    reply = get_answer_from_text(qa, query, best_part)
    
    add_request_record(REQUEST_DATABASE, user, query)
    bot.send_message(message.chat.id, reply) 

if __name__ == '__main__':
	print('Bot started!')
	bot.polling()
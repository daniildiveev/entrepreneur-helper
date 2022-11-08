import telebot
from telebot import types
from modules.database.database import * 
from modules.setup import config as cfg
from modules.parsing import parsers

bot = telebot.TeleBot(cfg.TOKEN)

@bot.message_handler(commands=['start'])
def send_keyboard(message, text:str='Hello, how can i help you?'):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    search_button = types.KeyboardButton(cfg.SEARCH)
    history_button = types.KeyboardButton(cfg.HISTORY)

    keyboard.add(search_button, history_button)

    if len(get_user_requests(message.user_id)) == 0:
        bot.send_message(message.chat.id, "Looks like you've never been before here!")

    message = bot.send_message(
        message.from_user.id,
        text=text,
        reply_markup=keyboard
    )

def callback_worker(message):
    if message.text == cfg.SEARCH:
        pass

    elif message.text == cfg.HISTORY:
        pass

    else:
        send_keyboard(message, "Did not understand you!")


if __name__ == '__main__':
    print("Bot started")
    bot.infinity_polling()

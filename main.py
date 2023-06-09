from config import BOT_TOKEN, OPENAI_API_KEY, USER_ID
from classes import PersonalBot
import openai
import logging

logger = logging.getLogger(__name__)
openai.api_key = OPENAI_API_KEY


bot = PersonalBot(BOT_TOKEN, USER_ID)


@bot.telebot.message_handler(commands=['clear_history'])
def clear_history(message):
    bot.history.clear()


@bot.telebot.message_handler(commands=['clear_last'])
def clear_last_interaction(message):
    bot.history = bot.history[:-2]
    if bot.history and bot.history[-1]['role'] == 'user':
        bot.history.pop()


@bot.telebot.message_handler(func=bot.is_owner)
def handle_message(message):
    logger.info(f'new message: {message.text}')
    try:
        response_text = bot.ask_ai(message.text)
    except Exception as e:
        response_text = f'SOMETHING IS WRONG ABOUT ME :( HELP :((\nError: {e}'
    bot.send_message(response_text)


if __name__ == '__main__':
    logger.info('starting polling...')
    bot.telebot.polling()

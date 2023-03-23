import logging
import telebot
import json
from config import ENGINE_ID
import openai


logger = logging.getLogger(__name__)


class PersonalBot:
    def __init__(self, token, user_id):
        logger.info('initiaing a bot')
        self.telebot = telebot.TeleBot(token)
        self.user_id = user_id

        with open("context.json") as file:
            self.context = json.loads(file.read())
            logger.info(f'loaded {len(self.context)} context strings')
#        future feature: save important messages locally to load as a part of context next time
#        with open("key_memories.json") as file:
#            self.key_memories = json.loads(file.read())
#            logger.info(f'loaded {len(self.key_memories)} key_memories strings')

        self.history = []

    def ask_ai(self, message):
        your_question = self.create_memory(message, is_user=True)
        self.history.append(your_question)
        logger.info(f'sending a message {message}')
        response = openai.ChatCompletion.create(
            model=ENGINE_ID,
            messages=self.context + self.history,  # + self.key_memories
            temperature=0.8,
        )
        logger.info('got result!')
        logger.debug(f'response: {response}')
        bot_answer = response["choices"][0]["message"]
        self.history.append(bot_answer)
        self.clean_history()
        return bot_answer['content']

    def clean_history(self, limit=20):
        self.history = self.history[limit::]

    def send_message(self, message):
        self.telebot.send_message(self.user_id, message)

    def is_owner(self, message):
        return message.from_user.id == self.user_id

    @staticmethod
    def create_memory(message, is_user=False):
        role = "assistant"
        if is_user:
            role = "user"
        return {"role": role, "content": message}

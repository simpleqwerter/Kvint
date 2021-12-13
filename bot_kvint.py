from pprint import pprint

from pony.orm import db_session
from transitions import Machine
from telebot import types

import handlers
import settings
from db import UserState, OrderConfirmed
from my_token import _token
import telebot
import logging


OWNER = '569630204'


class MyBot:

    def __init__(self):
        self.bot = telebot.TeleBot(_token)
        self.bot.set_update_listener(self.handle_messages)

    def run(self):
        self.bot.infinity_polling()

    def handle_messages(self, messages):
        """ Получает сообщения по одному """
        for message in messages:
            print(message)
            self.on_event(message)

    @db_session
    def on_event(self, message):
        """ обрабатывает входящее сообщение """
        user_id = message.from_user.id
        text = message.text.lower()
        user_state = UserState.get_or_none(user_id=user_id)
        logging.info(f'USER STATE = {user_state}')
        for intent in settings.INTENTS:
            if any(token in text for token in intent['tokens']):
                if intent['answer']:
                    self.send_text(intent['answer'], user_id)
                else:
                    logging.info(f'USER STATE = {user_state} start_scenario')
                    self.start_scenario(user_id, intent['scenario'])
                break
            elif user_state is not None:
                logging.info(f'USER STATE = {user_state} continue_scenario')
                self.continue_scenario(text, user_state, user_id)
                break
        else:
            self.send_text(settings.DEFAULT_ANSWER, user_id)

    def send_text(self, text_to_send, user_id, context=None):
        """ отправляет текст. добавляет кнопки из имеющихся вариантов """
        if context:
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            buttons = [but for but in context['variables']]
            keyboard.add(*buttons)
            self.bot.send_message(user_id, text_to_send.format(*context['variables']), reply_markup=keyboard)
        else:
            self.bot.send_message(user_id, text_to_send)

    def start_scenario(self, user_id, scenario_name):
        """ сбрасывает/начинает сценарий заново """
        scenario = settings.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text = step['text']
        s = UserState.get_or_none(user_id=user_id)
        context = {'variables': handlers.SIZES}
        if s:
            s.delete_instance()
        s = UserState(user_id=user_id, scenario_name=scenario_name, step_name=first_step, context={})
        s.save()
        self.send_text(text, user_id, context=context)

    @db_session
    def continue_scenario(self, text, user_state, user_id):
        """ продолжает сценарий  """
        steps = settings.SCENARIOS[user_state.scenario_name]['steps']
        step_name = user_state.step_name
        try:
            if 'handler' in steps[step_name]:
                handler = getattr(handlers, steps[step_name]['handler'])
                if handler(text=text, context=user_state.context):
                    if 'next_step' in steps[step_name]:
                        next_step_name = steps[step_name]['next_step']
                        next_step = steps[next_step_name]
                        self.send_text(next_step['text'].format(**user_state.context), user_id, user_state.context)
                        if steps[step_name]['next_step']:
                            user_state.step_name = next_step_name
                            user_state.save()
                    if 'next_step' not in user_state.step_name:
                        if 'confirm' in user_state.context and user_state.context['confirm'] is True:
                            order = OrderConfirmed(
                                pay=user_state.context['pay'],
                                size=user_state.context['size'],
                                user_id=user_id)
                            order.save()
                            self.bot.send_message(chat_id=OWNER, text=f'клиент id:{str(order.user_id)}\n'
                                                                      f'размер - {order.size}\n'
                                                                      f'оплата - {order.pay}')
                            user_state.delete_instance()
                else:
                    text_to_send = steps[step_name]['failure_text'].format(**user_state.context)
                    self.send_text(text_to_send, user_id)
            else:
                text_to_send = settings.DEFAULT_ANSWER
                self.send_text(text_to_send, user_id)
                user_state.delete_instance()

        except BaseException as exc:
            logging.error(f'ошибка в обработке события {exc}')
            text_to_send = 'was error. try again'
            self.send_text(text_to_send, user_id)
            user_state.delete_instance()  # если хотим запускать заново


if __name__ == "__main__":
    bot = MyBot()
    bot.run()

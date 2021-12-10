from transitions import Machine
from telebot import types
# from handlers import handle_size
from my_token import _token
import telebot


class Order(object):
    states = ['size_choise', 'pay_choise', 'order_confirm']
    order = {}
    def __init__(self):

        self.machine = Machine(model=self, states=Order.states, initial='size_choise')
        self.machine.add_transition(trigger='pay_choise', source='size_choise', dest='pay_choise')
        self.machine.add_transition(trigger='order_confirm', source='pay_choise', dest='order_confirm')


bot = telebot.TeleBot(_token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.order = Order()
    # bot.reply_to(message, "Какую вы хотите пиццу? Большую или маленькую?")
    bot.send_message(message.from_user.id, text="Какую вы хотите пиццу? Большую или маленькую?")
    bot.register_next_step_handler(message, size_choise)


@bot.message_handler(regexp="бол|мал") #content_types=['text']
def size_choise(message):
    if 'бол' in message.text:
        bot.order.order['size'] = 'большую'
    elif 'мал' in message.text:
        bot.order.order['size'] = 'маленькую'
    else:
        return bot.reply_to(message, "надо выбрать 'большую' или 'маленькую'")
    bot.send_message(message.from_user.id, text="Как вы будете платить?")
    # bot.reply_to(message, 'Как вы будете платить?')
    bot.register_next_step_handler(message, pay_choise)


@bot.message_handler(regexp="нал|кар")
def pay_choise(message):
    if 'нал' in message.text:
        bot.order.order['pay'] = 'наличными'
    elif 'кар' in message.text:
        bot.order.order['pay'] = 'картой'
    else:
        return bot.reply_to(message, "надо выбрать 'наличными' или 'картой'")
    confirm(message)


@bot.message_handler(regexp="да|нет")
def confirm(message):
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = f"Вы хотите {bot.order.order['size']} пиццу, оплата - {bot.order.order['pay']}. Верно?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    # if 'да' in message.text:
    #     bot.reply_to(message, "спасибо заказ готовиться")
    #     bot.order.order['confirm'] = True
    # elif 'нет' in message.text:
    #     bot.register_next_step_handler(message, size_choise)
    #     size_choise(message)
    # else:
    #     return failure(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.order.order['confirm'] = True #код сохранения данных, или их обработки
        text = 'начали готовить!'
        if bot.order.order['pay'] == 'картой':
            text += ' вот ссылка на оплату yandex.ru'
        bot.send_message(call.from_user.id, text)
    elif call.data == "no":
        bot.register_next_step_handler(call.message, size_choise)
        bot.send_message(call.from_user.id, text='давай начнем подбор заново')
        bot.send_message(call.from_user.id, text="Какую вы хотите пиццу? Большую или маленькую?")
        # bot.register_next_step_handler(call.message, size_choise)


bot.infinity_polling()

from transitions import Machine
from token import _token
class Order(object):
    states = ['size_choise', 'pay_choise', 'order_confirm']

    def __init__(self, pizza):

        self.machine = Machine(model=self, states=Order.states, initial='size_choise')
        self.machine.add_transition(trigger='wake_up', source='asleep', dest='hanging out')


import telebot

bot = telebot.TeleBot("TOKEN", parse_mode=None)





import re


FOOD = ['pizza', 'burger', 'sushi']
SIZES = ['большую', 'среднюю', 'маленькую']
PAY = ['картой', 'наличными']
CONFIRM = ['да', 'нет, начать заново']


def handle_size(text, context):

    for s in SIZES:
        if s in text:
            context['size'] = s
            context['variables'] = PAY
            return True
    else:
        context['variables'] = SIZES
        return False


def handle_pay(text, context):

    for s in PAY:
        if s in text:
            context['pay'] = s
            context['variables'] = CONFIRM
            return True
    else:
        context['variables'] = PAY
        return False

def handle_confirm(text, context):
    if "return_to" in context:
        context.pop('return_to')
        context.pop('variables')
    context['confirm'] = False
    if text == 'да':
        context['confirm'] = True
        return True
    # elif text == '1':
    #     context['return_to'] = "step_1"   # по логике continue_scenario  добавит +1
    #     return True
    # elif text == '2':
    #     context['return_to'] = "step_2"   # по логике continue_scenario  добавит +1
    #     return True
    else:
        return False




def handle_size(text, context):
    match = find_identical(text, size_var)
    if match:
        context['size'] = match
        return True
    else:
        context['variables'] = [key for key, value in size_var.items()]
        return False


def handle_pay(text, context):
    match = find_identical(text, pay_var)
    if match:
        context['pay'] = match
        return True
    else:
        context['variables'] = [key for key, value in pay_var.items()]
        return False



def find_identical(text, identical):
    for key, value in identical.items():
        result = value.match(text)
        if result:
            return key


size_var = {
    'Большая': re.compile(r"^[Б|б]ол"),
    'Маленькая': re.compile(r"^[М|м]ал"),
}

pay_var = {
    'Наличными курьеру': re.compile(r"^[Н|н]ал"),
    'Картой онлайн': re.compile(r"^[К|к]арт"),
}

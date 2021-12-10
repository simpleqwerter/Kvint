INTENTS = [
    {
        "name": "подбор пиццы",
        "tokens": ("\ticket", "начать"),
        "scenario": "pizza_order",
        "answer": None
    },
    {
        "name": "помощь",
        "tokens": ("помощь", "\help", "help", 'привет'),
        "scenario": None,
        "answer": "привет я умею подбирать пиццу. Напиши 'начать'."
    },
]

SCENARIOS = {
    "pizza_order":
        {
            "first_step": "step_1",
            "steps":
                {
                    "step_1": {
                        "text": "вы хотите пиццу большую(30см) или маленькую(20см)",
                        "failure_text": "напишите 'большую' или 'маленькую'",
                        "handler": "handle_size",
                        "next_step": "step_2"
                    },
                    "step_2": {
                        "text": "выберите вариант оплаты",
                        "failure_text": "напишите 'картой' или 'наличными'",
                        "handler": "handle_pay",
                        "next_step": "step_3"
                    },
                    "step_3": {
                        "text": "Давай проверим: {size} пицца - оплата {pay}. верно?"
                                "Если все ок напиши 'да', мы сразу начнем готовить \n "
                                "Если билет НЕ верный то напиши 'начать' (запустит всё заново) \n",
                        "failure_text": "не понятно.. выбери из вариантов",
                        "handler": 'handle_confirm',
                        "next_step": "step_4"
                    },
                    "step_4":   {
                            "text": "Заказ принят ждите курьера!"
                                    "Чтобы заказать еще - напиши 'начать' "
                    }
                }
        }
}

DEFAULT_ANSWER = "мне этого не понять. Я лишь умею подбирать размер пиццы и варианты оплаты"

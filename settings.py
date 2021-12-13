INTENTS = [
    {
        "name": "подбор пиццы",
        "tokens": ("/start", "начать", 'привет'),
        "scenario": "pizza_order",
        "answer": None
    },
]

SCENARIOS = {
    "pizza_order":
        {
            "first_step": "step_1",
            "steps":
                {
                    "step_1": {
                        "text": "вы хотите пиццу большую или маленькую",
                        "failure_text": "выберите размер из {variables}",
                        "handler": "handle_size",
                        "next_step": "step_2"
                    },
                    "step_2": {
                        "text": "выберите вариант оплаты 'картой' или 'наличными'",
                        "failure_text": "выберите оплату из {variables}",
                        "handler": "handle_pay",
                        "next_step": "step_3"
                    },
                    "step_3": {
                        "text": "Давай проверим: {size} пиццу - оплата {pay}. верно?\n"
                                "Если все ок напиши 'да', мы сразу начнем готовить\n"
                                "Заказ НЕ верный то напиши 'начать' или /start (запустит всё заново) \n",
                        "failure_text": "мне это не понятно.. выбери из {variables}",
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

DEFAULT_ANSWER = "мне этого не понять. Я лишь умею подбирать размер пиццы и варианты оплаты. напиши /start"

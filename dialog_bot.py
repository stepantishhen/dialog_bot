from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


def start(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живете?")

    return 1


def first_response(update, context):
    locality = update.message.text
    update.message.reply_text("Какая погода в городе {locality}?".format(**locals()))
    return 2  # Следующее текстовое сообщение будет обработано обработчиком states[2]


def second_response(update, context):
    weather = update.message.text  # Ответ на второй вопрос. Мы можем его сохранить в базе данных или переслать куда-либо.
    update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными


def skip(update, context):
    update.message.reply_text("Какая погода у вас за окном?")
    return 2  # Следующее текстовое сообщение будет обработано обработчиком states[2]


def stop(update, context):
    update.message.reply_text("Жаль. А было бы интересно пообщаться. Всего доброго!")
    return ConversationHandler.END  # Константа, означающая конец диалога.


def main():
    updater = Updater("1797418204:AAEnwsPu8xmN16Oe6W0EGNUBTizVuWjCRi4", use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],  # Точка входа в диалог.
        # В данном случае команда /start. Она задает первый вопрос.

        states={
            # Состояния внутри диалога. В данном случае два обработчика сообщений, фильтрующих текстовые сообщения.
            1: [CommandHandler('skip', skip), MessageHandler(Filters.text, first_response)],
            # Функция читает ответ на первый вопрос и задает второй.
            2: [MessageHandler(Filters.text, second_response)]
            # Функция читает ответ на второй вопрос и завершает диалог.
        },
        fallbacks=[CommandHandler('stop', stop)]  # Точка прерывания диалога. В данном случае команда /stop.
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

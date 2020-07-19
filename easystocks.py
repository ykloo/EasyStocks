#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from getNews import initialise_driver

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued.
       This two commands have the same function, but context.bot.send_message is more time consuming and annoying, 
       update.message is simply a shortcut, it handles the setting of chat_id and reply_to_message_id for you"""

    # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    text = '<b>Hello! Welcome to EasyStocks! Enter a stock ticker to start! \n\neg. AAPL, TSLA</b>'
    update.message.reply_text(text, parse_mode = 'HTML')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Please enter a stock ticker to start!')

def enter(update, context, text):
    """Send a message when the command /help is issued."""
    update.message.reply_text(f'This is what you have entered: {text}')
    update.message.reply_text('Searching...')
    data = initialise_driver(text)

    name = data[0]
    price_changes = data[1]
    articles_objects = data[2]

    price = price_changes[0]
    changes = price_changes[1]

    output = f'<b>{name}</b>\n{price} \n{changes} \n\n<b>LATEST NEWS \n\n</b>'

    for i in range(len(articles_objects)):
        article = articles_objects[i]
        author = article.author
        date = article.date
        headline = article.headline
        link = article.link
        # output += f'{author} {date} \n{i+1}.{headline} \n{link} \n\n '
        output += f'{author} | {date} \n{i+1}.  <a href="{link}">{headline}</a> \n\n'



    update.message.reply_text(output, parse_mode = 'HTML', disable_web_page_preview = True)
    

    # return text


def echo(update, context):
    """Echo the user message."""
    text = update.message.text
    return enter(update, context, text)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1375620415:AAHFeCrxPDEg0LciMuhQM1D7EIfJ9bDJqkg", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))


    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

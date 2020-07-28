#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
from getNews import initialise_driver
from db import check_user, overwrite, create_update

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

REVIEW, CHANGE = range(2)

temp = {}


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued.
       This two commands have the same function, but context.bot.send_message is more time consuming and annoying, 
       update.message is simply a shortcut, it handles the setting of chat_id and reply_to_message_id for you"""

    text = '<b>Hello! Welcome to EasyStocks! Enter a stock ticker to start!</b>\n\neg. AAPL, TSLA \n\nFor stocks listed in SGX, please add .SI suffix at the end of your input. \n\n<b>Looking for a stock that not based in SG or US, click <a href="https://help.yahoo.com/kb/exchanges-data-providers-yahoo-finance-sln2310.html">here</a> for relevant suffixes</b>'
    update.message.reply_text(text, parse_mode = 'HTML', disable_web_page_preview = True)


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Please enter a stock ticker to start!')

def loading(update, context, text):
    update.message.reply_text(f'This is what you have entered: {text}')
    update.message.reply_text('Searching...')
    enter(update, context, text)

def enter(update, context, text):
    try:
        data = initialise_driver(text)
        print("Stock found!")
        output = get_output(data)
    except:
        print("Stock not found!")
        output = 'Stock not found! Please enter the correct ticker!'
    
    update.message.reply_text(output, parse_mode = 'HTML', disable_web_page_preview = True)
    
def get_output(data):
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
        output += f'{author} | {date} \n{i+1}.  <a href="{link}">{headline}</a> \n\n'
    return output

def echo(update, context):
    text = update.message.text
    return loading(update, context, text)


def shortlisted(update, context):
    update.message.reply_text(
    'Please enter the stock ticker(s) that you want to shortlist, leaving a space between each ticker')
    global id
    id = update.message.chat_id
    return REVIEW

def review(update, context):
    global shortlist
    shortlist = update.message.text
    print(shortlist)
    update.message.reply_text(
        f'This is what you have entered: {shortlist}\n' 
        'Do you want to make any changes? Re-enter the ticker(s) if you wish to or send /skip if you don\'t want to.')
    return CHANGE

def skip_review_add(update, context):
    # change = False
    return store_to_db(shortlist, id, update, context, change)

def change(update, context):
    # change = True
    shortlist = update.message.text
    # update.message.reply_text('Re-enter the ticker(s) that you want to shortlist, leaving a space between each ticker')
    return store_to_db(shortlist, id, update, context, change)



def store_to_db(shortlist, id, update, context, change):
    if check_user(id):
        overwrite(id, shortlist)
    else:
        create_update(id, shortlist)
    update.message.reply_text("Shortlist updated!")
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text('Action cancelled. Please enter a stock ticker to continue.')

    return ConversationHandler.END




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
    # dp.add_handler(CommandHandler("selected", display_selected))

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('store', shortlisted)],

        states={
            REVIEW: [MessageHandler(Filters.text, review)],

            CHANGE: [MessageHandler(Filters.text & ~Filters.command, change),
                CommandHandler('skip', skip_review_add )],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # on noncommand i.e message - by default launches a search for the inputted ticker
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

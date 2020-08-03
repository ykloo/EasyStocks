import logging

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
from getNews import initialise_driver
from db import check_user, overwrite, create_update, retrieve_stocks

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

REVIEW, CHANGE = range(2)

temp = {}

#starts the bot
def start(update, context):
    """Send a message when the command /start is issued.
       This two commands have the same function, but context.bot.send_message is more time consuming and annoying, 
       update.message is simply a shortcut, it handles the setting of chat_id and reply_to_message_id for you"""
    global id
    id = update.message.chat_id
    text = '<b>Hello! Welcome to EasyStocks! Enter a stock ticker to start!</b>\n\neg. AAPL, TSLA \n\nFor stocks listed in SGX, please add .SI suffix at the end of your input. \n\n<b>Looking for a stock not based in Singapore or United States? click <a href="https://help.yahoo.com/kb/exchanges-data-providers-yahoo-finance-sln2310.html">here</a> for relevant suffixes</b>\n\nShortlisted some stock(s) previously? Enter /selected to view them now.'
    update.message.reply_text(text, parse_mode = 'HTML', disable_web_page_preview = True)

#displays help
def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Welcome to EasyStocks!\n'
        'Commands available:\n'
        '/start - starts the bot\n'
        '/shortlist - shortlists stocks for one-click viewing\n'
        '/selected - shows shortlisted stocks\n'
        'Have a great day!')

#upon input of a stock ticker
def echo(update, context):
    text = update.message.text
    return loading(update, context, text)

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


'''
The following 6 functions: 
SHORTLISTED, REVIEW, SKIP_REVIEW_ADD, CHANGE, STORE_TO_DB, CANCEL
work as part of the ConversationHandler
'''
def shortlisted(update, context):
    update.message.reply_text(
    'Please enter the stock ticker(s) that you want to shortlist, leaving a space between each ticker')

    return REVIEW

def review(update, context):
    global shortlist
    shortlist = update.message.text
    update.message.reply_text(
        f'This is what you have entered: {shortlist}\n' 
        'Do you want to make any changes? Re-enter the ticker(s) if you wish to or send /skip if you don\'t want to.')
    return CHANGE

def skip_review_add(update, context):
    return store_to_db(shortlist, id, update, context, change)

def change(update, context):
    shortlist = update.message.text
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

#displays stocks previously shortlisted
def display_selected(update, context):
    #checks if the user has shortlisted stock(s) previously
    update.message.reply_text("Searching...")
    if check_user(id):
        stocks = retrieve_stocks(id)
        update.message.reply_text(f'This is what you have shortlisted: {stocks}')
        stocks = stocks.split(' ')
        for ticker in stocks:
            enter(update, context, ticker)
    else:
        update.message.reply_text("User has not shortlisted any")



def main():
    """Start the bot."""
    updater = Updater("<BOT TOKEN>", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands 
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("selected", display_selected))

    # Add conversation handler with the states REVIEW, CHANGE
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('shortlist', shortlisted)],

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
import os

BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
QUOTE_API_TOKEN = os.getenv("DATA_API_TOKEN")

import requests
import json

import logging
from telegram import ForceReply, Update

from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send a message when the command /start is issued."""

    user = update.effective_user

    await update.message.reply_text(
        rf"Hi {user.full_name}! I'm Poly - your 'that' life assistant. Use /help to see available commands!",
    ) 



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send a message when the command /help is issued."""

    await update.message.reply_text("/today - todays dashboard")



async def today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    quote_category = 'success'
    api_urls = {'quote' : 'https://api.api-ninjas.com/v1/quotes?category={}'.format(quote_category),
                'currency' : 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/eur/jpy.json'
                }
    
    quote_response = requests.get(api_urls, headers={'X-Api-Key': QUOTE_API_TOKEN})

    if quote_response.status_code == requests.codes.ok:
        response = quote_response.json()[0]
        await update.message.reply_text(rf"<i>{response['quote']}</i> - <ins>{response['author']}</ins>", parse_mode="HTML")
    else:
        print("Error:", response.status_code, response.text)
        await update.message.reply_text("Nothing to display :(")



def main() -> None:

    """Start the bot."""

    # Create the Application and pass it your bot's token.

    application = Application.builder().token(BOT_API_TOKEN).build()


    # on different commands - answer in Telegram

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("help", help_command))


    # on non command i.e message - echo the message on Telegram

    application.add_handler(CommandHandler("today", today))


    # Run the bot until the user presses Ctrl-C

    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":

    main()

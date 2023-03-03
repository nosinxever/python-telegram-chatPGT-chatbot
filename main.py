# pip install openai python-telegram-bot==13.7

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext

import openai
openai.api_key = ""
telegram_token=""
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the commands that the bot will accept

def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Hi, I\'m a chatbot! Send me a message and I\'ll try to respond with something relevant.')


def help(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Help! I need somebody. Help! Not just anybody. Help! You know I need someone. Help!')


def chat(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    # Get the message text
    text = update.message.text
# Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=[{"role": "user", "content": text}],   # The conversation history up to this point, as a list of dictionaries
        max_tokens=2048,        # The  number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    
    # Get the generated response
    message = response['choices'][0]['message']['content']

    # Send the response back to the user
    update.message.reply_text(message)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it the bot's token.
    updater = Updater(telegram_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    # Register message handler
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, chat))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()

# nohup python3 script.py
# ps -ef | grep python
# kill -9 PID
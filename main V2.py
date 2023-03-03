import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext

import openai
from openai.error import OpenAIError
openai.api_key = " "
telegram_token=" "
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the commands that the bot will accept

history = []

def ask_gpt_response(prompt):

    try:
        # add the prompt to the history
        history.append(prompt+"\n")
        if len(history)>4:
            del history[0: 2]

        prompt=" ".join(history)

        # Use OpenAI's ChatCompletion API to get the chatbot's response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
            messages=[{"role": "user", "content": prompt}],   # The conversation history up to this point, as a list of dictionaries
            max_tokens=2000,        # The  number of tokens (words or subwords) in the generated response
            stop=None,              # The stopping sequence for the generated response, if any (not used here)
            temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
        )
        # Get the generated response
        message = response['choices'][0]['message']['content']
        # return the response
        return message
    except OpenAIError as err:
        logging.error(f'error occure :{err}')


def hist(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(" ".join(history))


def chat(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    # Get the message text
    user_message = update.message.text

    gpt_response = ask_gpt_response("You: " + user_message )
     # add ChatGPT's response to the history
    history.append("AI: "+gpt_response+"\n")
    # Send the response back to the user
    update.message.reply_text(gpt_response)
    # print(gpt_response)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it the bot's token.
    updater = Updater(telegram_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("hist", hist))

    # Register message handler
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, chat))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()


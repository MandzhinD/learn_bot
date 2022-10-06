from emoji import emojize
from glob import glob
import logging
from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename = 'bot.log', level = logging.INFO)

def greet_user(update,context):
    print("вызван /start")
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Hi user {context.user_data['emoji']}!")

def talk_to_me(update,context):    
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text
    print(text)
    update.message.reply_text(f"{text} {context.user_data['emoji']}") 

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Your number is {user_number}, mine is {bot_number}, you win!"
    elif user_number == bot_number:
        message = f"Your number is {user_number}, mine is {bot_number}, draw!"
    else: 
        message = f"Your number is {user_number}, mine is {bot_number}, you lose!"
    return message

def guess_number(update,context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Input an integer"
    else:
        message = "Input a number"
    update.message.reply_text(message)

def send_panda_picture(update,context):
    panda_photo_list = glob('images/panda*.jp*g')
    panda_photo_filename = choice(panda_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(panda_photo_filename, 'rb'))

def main():
    mybot = Updater(settings.API_KEY)  

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("panda", send_panda_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Bot has started")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main() 

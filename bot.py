import os
from dotenv import load_dotenv

import telebot

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
print(BOT_TOKEN)
bot = telebot.TeleBot(BOT_TOKEN)

personName = None
personBirthday = None

Birthdays = {}


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(
        message.chat.id,
        "Some of the following commands are available:\n /start\n /help\n /about\n /addBirthday\n /addManyBirthdays",
    )


@bot.message_handler(commands=["addBirthday"])
def getBirthday(message):
    bot.send_message(message.chat.id, "Please enter Person's name")
    bot.register_next_step_handler(message, getPersonName)


def getPersonName(message):
    global personName
    print(message.text)
    personName = message.text
    bot.send_message(
        message.chat.id, "Please enter Person's birthday in format DD.MM.YYYY"
    )
    bot.register_next_step_handler(message, getPersonBirthday)


def getPersonBirthday(message):
    global personBirthday
    print(message.text)
    personBirthday = message.text

    bot.send_message(message.chat.id, "Person's name is " + personName)
    bot.send_message(message.chat.id, "Person's birthday is " + personBirthday)
    Birthdays[personBirthday] = personName
    print(Birthdays)


bot.infinity_polling()

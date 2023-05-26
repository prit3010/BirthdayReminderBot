import os
from dotenv import load_dotenv

import telebot
import datetime
import threading
import time
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()
uri = os.getenv("MONGO_URI")
client = pymongo.MongoClient(uri, server_api=ServerApi("1"))
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

my_db = client["mydb"]
my_col = my_db["birthdays"]

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

personName = None
personBirthday = None


def isSomeoneBirthdayToday():
    while True:
        print("Checking if someone has birthday today")
        today = datetime.datetime.now()
        today = today.strftime("%d.%m")
        print(today)
        myquery = {"birthday": "07.12"}
        mydoc = my_col.find(myquery, {})
        birthdayList = []
        for x in mydoc:
            if x["reminder"] == 0:
                birthdayList.append((x["name"], x["year"], x["user_id"]))
                my_col.update_one(x, {"$set": {"reminder": 1}})
        for birthday in birthdayList:
            bot.send_message(
                birthday[2],
                "Happy Birthday " + birthday[0] + " !\n" + "He is " + birthday[1],
            )
        time.sleep(5)


# @bot.message_handler(func=isSomeoneBirthdayToday)
# def sendBirthday(message):
#     bot.send_message(message.chat.id, "Today is someone's birthday")


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
    year = personBirthday.split(".")[2]
    print(year)
    personBirthdate = personBirthday.split(".")[0] + "." + personBirthday.split(".")[1]

    my_dict = {
        "user_id": message.chat.id,
        "name": personName,
        "birthday": personBirthdate,
        "year": year,
        "reminder": 0,
    }
    x = my_col.insert_one(my_dict)
    bot.send_message(message.chat.id, "Birthday added successfully")
    bot.send_message(message.chat.id, "Person's name is " + personName)
    bot.send_message(message.chat.id, "Person's birthday is " + personBirthday)


birthday_thread = threading.Thread(target=isSomeoneBirthdayToday)
birthday_thread.start()
bot.infinity_polling()

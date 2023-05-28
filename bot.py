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
        birthdayMap = {}
        for x in mydoc:
            if x["reminder"] == 0:
                uid = x["user_id"]
                if uid in birthdayMap:
                    birthdayMap[uid].append((x["name"], x["year"]))
                else:
                    birthdayMap[uid] = [(x["name"], x["year"])]
                my_col.update_one(x, {"$set": {"reminder": 1}})
        for uid, birthdayList in birthdayMap.items():
            wishingList = ""
            for name, year in birthdayList:
                wishingList += name + " (" + str(getAge(year)) + ") \n"
            print(wishingList)
            bot.send_message(uid, "Today is birthdays of \n" + wishingList)

        time.sleep(60)


def getAge(year):
    today = datetime.datetime.now()
    return today.year - int(year)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing? Type /help to know more")


@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(
        message.chat.id,
        "Some of the following commands are available:\n /start\n /help\n /about\n /addBirthday\n /addManyBirthdays \n /editBirthday \n /getList",
    )


@bot.message_handler(commands=["getList"])
def getListOfBirthdays(message):
    myquery = {"user_id": message.chat.id}
    mydoc = my_col.find(myquery, {})
    birthdayList = ""
    for x in mydoc:
        birthdayList += x["name"] + " (" + x["birthday"] + ") \n"
    bot.send_message(message.chat.id, "List of Birthdays \n" + birthdayList)


@bot.message_handler(commands=["addManyBirthdays"])
def add_Many_Birthdays(message):
    bot.send_message(
        message.chat.id,
        "Please send a CSV file with names and birthdays in format name,birthday",
    )
    bot.register_next_step_handler(message, handle_file)


def handle_file(message):
    file_info = bot.get_file(message.document.file_id)
    print(file_info)
    downloaded_file = bot.download_file(file_info.file_path)
    strForm = downloaded_file.decode("utf-8")
    listNames = strForm.split("\r\n")[1:]
    for name in listNames:
        n, b = name.split(",")
        my_dict = {
            "user_id": message.chat.id,
            "name": n,
            "birthday": b.split(".")[0] + "." + b.split(".")[1],
            "year": b.split(".")[2],
            "reminder": 0,
        }
        x = my_col.insert_one(my_dict)
    bot.send_message(message.chat.id, "Received file and Added Birthdays successfully")


@bot.message_handler(commands=["addBirthday", "editBirthday"])
def getBirthday(message):
    bot.send_message(message.chat.id, "Please enter Person's name")
    bot.register_next_step_handler(message, getPersonName, message)


def getPersonName(message, action):
    global personName
    personName = message.text
    action = action.text
    print(action)
    if action == "/addBirthday" and checkIfPersonExists(personName):
        bot.send_message(
            message.chat.id,
            "Person with name " + personName + " already exists.",
        )
        return
    else:
        bot.send_message(
            message.chat.id, "Please enter Person's birthday in format DD.MM.YYYY"
        )
        bot.register_next_step_handler(message, getPersonBirthday, action)


def getPersonBirthday(message, action):
    global personBirthday
    personBirthday = message.text
    year = personBirthday.split(".")[2]
    personBirthdate = personBirthday.split(".")[0] + "." + personBirthday.split(".")[1]
    if action == "/editBirthday":
        myquery = {"name": personName}
        newvalues = {"$set": {"birthday": personBirthdate, "year": year}}
        my_col.update_one(myquery, newvalues)
        bot.send_message(message.chat.id, "Birthday updated successfully")
        bot.send_message(message.chat.id, "Person's name is " + personName)
        bot.send_message(message.chat.id, "Person's birthday is " + personBirthday)
    else:
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


def checkIfPersonExists(name):
    myquery = {"name": name}
    num = my_col.count_documents(myquery)
    if num > 0:
        return True
    else:
        return False


@bot.message_handler(func=lambda message: True)
def invalid_command(message):
    bot.reply_to(message, "Invalid command")


birthday_thread = threading.Thread(target=isSomeoneBirthdayToday)
birthday_thread.start()
bot.infinity_polling()

# Birthday Reminder Bot
This is a Python script for a Birthday Reminder Bot. It uses the Telebot library to interact with users via the Telegram Bot API and MongoDB to store and retrieve birthday information.

NOTE: If you want to run your own instance of this bot, follow the subsequent instructions.
## Prerequisites
1. Clone this repository
2. Before running the script, make sure to download all the dependencies in the `requirements.txt` file
```
pip install -r requirements.txt
```

## Setup

1. Clone the repository and navigate to the project directory.
2. Create a new file named `.env` in the project directory.
3. Open the `.env` file and add the following environment variables:
```
MONGO_URI=<your_mongodb_uri>
BOT_TOKEN=<your_telegram_bot_token>
```
Replace `<your_mongodb_uri>` with the connection URI for your MongoDB database.
Replace `<your_telegram_bot_token>` with the token for your Telegram bot.

4. Save the `.env` file.

## Usage

1. Run the script using the following command:
```
python bot.py
```
2. Start a conversation with your Telegram bot.
3. Use the following commands to interact with the bot:

- `/start` - Start the conversation and receive a welcome message.
- `/help` - Get a list of available commands.
- `/about` - Learn more about the bot and its functionalities.
- `/addBirthday` - Add a new birthday.
- `/editBirthday` - Edit an existing birthday.
- `/getList` - Get a list of all added birthdays.
- `/addManyBirthdays` - Add multiple birthdays using a CSV file.

4. Follow the prompts and provide the necessary information to add or edit birthdays.

## Functionality

The Birthday Reminder Bot offers the following functionalities:

- Add a single birthday: Use the `/addBirthday` command to add a new birthday. You will be prompted to enter the person's name and birthday in the format DD.MM.YYYY.

- Edit a birthday: Use the `/editBirthday` command to edit an existing birthday. Enter the person's name and provide the updated birthday in the format DD.MM.YYYY.

- Add multiple birthdays: Use the `/addManyBirthdays` command to add multiple birthdays at once. Send a CSV file with names and birthdays in the format `name,birthday` to the bot.

- Get a list of birthdays: Use the `/getList` command to get a list of all the birthdays you have added.

- Help and information: Use the `/help` command to get a list of available commands. Use the `/about` command to learn more about the bot and its functionalities.

The bot also includes a background thread that checks for birthdays every minute. If there are birthdays on the current day, it sends notifications to the respective users.

## About

This bot is created by @prittamravi. It provides a convenient way to manage and get notified about birthdays of friends and family members. Feel free to reach out to the creator for any questions or feedback.

Please note that the bot requires a MongoDB database for storing birthday information and a Telegram bot token for interacting with users. Ensure you have these resources set up before running the bot.

## Moving Forward
- Deploy Telegram Bot
- Add more functionalities
- Improve User Interface, in terms of looks
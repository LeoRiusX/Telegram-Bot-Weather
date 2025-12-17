# Telegram-Wetterbot (aiogram)

Asynchronous Telegram bot for viewing weather using the OpenWeatherMap API.




## Features (The bot can display:):
-> Weather now (with date)\
-> Today's forecast (with date)\
-> Tomorrow's forecast (with date)\
-> Automatically determines the season (Winter / Spring / Summer / Autumn)\
-> Sends GIF animations depending on the season\
-> Stores users and their cities in SQLite\
-> Logs messages to a file\
-> Advertisement (automatic)

## Сode information:

Bot_Weather/\
#pack\
routers/\
**all_commands.py** --- *All bot commands*\
**database.py**     --- *Work with SQLite + logging*\
\
**config.py**       --- *logic of working with API Key, Bot Token (need .env)*\
**users.db**        --- *SQLite user database*\
**log.txt**         --- *Message log*\
**Bot_main.py**     --- *Bot launch*\
.env --- *(need to create)*\

## DB stucture
#log.txt\
All user messages are recorded in log.txt in the following format:\
[YYYY-MM-DD HH:MM:SS] user_id | @username | Full Name: message

users.db\
user_id     INTEGER (PRIMARY KEY)\
username    TEXT\
first_name  TEXT\
city        TEXT


## Requirements
Python 3.10+\
SQLite3\
Telegram Bot Token\
OpenWeather API Key\
Aiogram\
Aiohttp\
Python-dotenv

## Install all necessary libraries using pip:
pip install -r requirements.txt\
\
Please note that to use the bot, you need to create .env file.\
You need to write in it:\
BOT_TOKEN=telegram_bot_token\
API_KEY=openweather_api_key\
\
BOT_TOKEN — Telegram bot token (get from @BotFather)\
API_KEY — OpenWeather service API key (https://openweathermap.org/api)\

## Bot commands
Command --->   Description\
/start --->    User registration\
/help --->   List of all commands\
/setcity (city) --->   Set city\
/clearcity --->   Delete selected city\
/weather --->   Current weather\
/today --->   Forecast for today\
/tomorrow --->   Forecast for tomorrow

***Leorius**** *(Project for free use)* **GitHub: https://github.com/LeoRiusX**



## Launching
```bash
python BOT.py







from aiogram import types, Router, Bot, F
from aiogram.filters import Command, CommandStart
from datetime import datetime, timedelta
from aiogram.enums import ChatAction, ParseMode
from aiogram.utils import markdown
from aiogram.exceptions import TelegramForbiddenError
from .database import get_user_city, full_city, set_user_city
router = Router()
from config import API_KEY
import asyncio
import aiohttp




# Do not touch these links! -{
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
BASE2_URL = "http://api.openweathermap.org/data/2.5/forecast"
#}-

# GIFs for seasons.
GIFS = {
    "Winter": "https://i.pinimg.com/originals/86/ab/1f/86ab1f2cda716a89f0927bf0db5d07bb.gif",
    "Spring": "https://i.pinimg.com/originals/a5/d5/a1/a5d5a1849afcb19283e2d1848854399a.gif",
    "Summer": "https://i.redd.it/l12tolak94z01.gif",
    "Autumn": "https://i.pinimg.com/originals/83/a2/3f/83a23f69e15c54ae90883abb674c95f1.gif"
}

#main
@router.message(CommandStart())
async def command_start(message: types.Message):
    from Bot_Weather.routers.database import add_user, USERS
    bot = message.bot
    me = await bot.get_me()
    bot_name = me.first_name
    await message.answer(f"Hello, I am a bot for shows the weather, my name is {bot_name}.\nАnd your name is -> {message.from_user.full_name}?\nEnjoy using it.\n\nFull commands list -> /help")
    USERS.append(message.from_user.id)

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    add_user(user_id, username, first_name)

#ad scheduler
async def scheduler(bot: Bot):
    while True:
        from Bot_Weather.routers.database import USERS, delete_user
        for user_id in USERS:
            url = "https://pngimg.com/uploads/github/github_PNG65.png"
            url2 = "https://github.com/LeoRiusX"
            text = (
            f"{markdown.hide_link(url)}New Project! 🔥\n"
            "🍌Example advertising that will be in a bot 🍌\n"
            "💵For free$💵\n"
            f'My GitHub -> <a href="{url2}">👉See More👈</a>'
            )
            try:
                await bot.send_message(user_id, text=text, parse_mode=ParseMode.HTML)
            except TelegramForbiddenError:
                delete_user(user_id)
        await asyncio.sleep(10000)

#list commands
@router.message(Command("help"))
async def command_help(message: types.Message):
    text_m = markdown.text(markdown.bold("Commands list:"))
    text_note = markdown.text(markdown.bold("Attention: to receive any forecast, enter your city!!!"))
    text_list2 = markdown.text(markdown.underline("Set the selected city ->"), "/setcity \\_\\_\\_\\_\\_")
    text_list3 = markdown.text(markdown.bold("Remove the selected city ->"), "/clearcity")
    text_list4 = markdown.text(markdown.bold("Show weather for now in your city ->"), "/weather")
    text_list5 = markdown.text(markdown.bold("Weather for today ->"), "/today")
    text_list6 = markdown.text(markdown.bold("Weather for tomorrow ->"), "/tomorrow")
    text_last = markdown.text(
        markdown.italic("If something is not displayed (or you have blocked the bot earlier), use the command again ->"), "/start")
    text_main = (
        f"{text_m}\n\n"
        f"{text_note}\n\n"
        f"{text_list2}\n"
        f"{text_list3}\n"
        f"{text_list4}\n"
        f"{text_list5}\n"
        f"{text_list6}\n\n"
        f"{text_last}\n"
    )
    await message.answer(text=text_main,  parse_mode=ParseMode.MARKDOWN_V2)

#setcity
@router.message(Command("setcity"))
async def set_city(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please specify the city. Example: /setcity Los Angeles")
        return

    city = args[1].strip()
    user_id = message.from_user.id

    set_user_city(user_id, city)
    await message.answer(f"The city has been set successfully: {city}")

#funcs for get data weather
#get info weather now
async def get_weather(city: str) -> str:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "en"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as resp:
            data = await resp.json()

            if resp.status != 200:
                return "❌Unable to retrieve weather information.❌\n Please check the city name!"

            date_str = datetime.now().strftime("%d.%m.%Y")
            temp = data["main"]["temp"]
            dweather = data["weather"][0]["description"]
            season = get_season()

            text = (
                f"Season: {season}\n\n"
                f"⛱️ Weather now in {city}:\n"
                f"🌡️ Temperature: {temp}°C\n"
                f"🌥️ In detail: {dweather}\n\n"
                f"Date: {date_str} \n"
            )
            return text

#get info weather today
async def get_weather_today(city: str) -> dict:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "en"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE2_URL, params=params) as resp:
            data = await resp.json()

            if resp.status != 200:
                return {"text": "❌No forecast data available❌"}

            today = datetime.now().date()
            today_forecast = []
            season = get_season()
            date_str = datetime.now().strftime("%d.%m.%Y")

            for item in data["list"]:
                dt = datetime.fromtimestamp(item["dt"])

                if dt.date() == today:
                    temp = item["main"]["temp"]
                    desc = item["weather"][0]["description"]
                    time = dt.strftime("%H:%M")

                    today_forecast.append(f"◼️{time} — {temp}°C, {desc}◼️")

            if not today_forecast:
                return {"text": "❌No forecast data available for today❌"}


            result = (

                f"Season: {season}\n\n"
                f"Weather forecast for today ({date_str}) in {city}:\n\n"

            )

            result += "\n".join(today_forecast)

            return {"text": result}

#get info weather tomorrow
async def get_weather_tomorrow(city: str) -> dict:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "en"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE2_URL, params=params) as resp:
            data = await resp.json()

            if resp.status != 200:
                return {"text": "❌No forecast data available❌"}

            tomorrow = (datetime.now() + timedelta(days=1)).date()
            forecast = []

            season = get_season()
            date_str = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
            for item in data["list"]:
                dt = datetime.fromtimestamp(item["dt"])

                if dt.date() == tomorrow:
                    temp = item["main"]["temp"]
                    desc = item["weather"][0]["description"]
                    time = dt.strftime("%H:%M")

                    forecast.append(
                        f"◼️{time} — {temp}°C, {desc}◼️"
                    )

            if not forecast:
                return {"text": "❌No forecast data available for tomorrow❌"}

            result = (
                f"Season: {season}\n\n"
                f"Weather forecast for tomorrow ({date_str}) in {city}:\n\n"

            )
            result += "\n".join(forecast)

            return {"text": result}

#get season for gif
def get_season():
    month = datetime.now().month
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"

#weather NOW!
@router.message(Command("weather"))
async def command_now(message: types.Message):

    user_id = message.from_user.id
    city = get_user_city(user_id)
    season = get_season()
    gif = GIFS[season]

    if not city:
        await message.answer(
            "❗You did not specify the city❗\n"
            "Use command:\n"
            "/setcity <city>"
        )
        return
    await message.chat.do(ChatAction.FIND_LOCATION)
    weather_text = await get_weather(city)
    await message.answer_animation(gif, caption=weather_text)

#weather TODAY!
@router.message(Command("today"))
async def command_today(message: types.Message):

    user_id = message.from_user.id
    city = get_user_city(user_id)
    season = get_season()
    gif = GIFS[season]

    if not city:
        await message.answer(
            "❗You did not specify the city❗\n"
            "Use command:\n"
            "/setcity <city>"
        )
        return
    weather = await get_weather_today(city)
    await message.answer_animation(
        gif,
        caption=weather["text"]
    )

#weather TOMORROW!
@router.message(Command("tomorrow"))
async def command_tomorrow(message: types.Message):

    user_id = message.from_user.id
    city = get_user_city(user_id)
    season = get_season()
    gif = GIFS[season]

    if not city:
        await message.answer(
            "❗You did not specify the city❗\n"
            "Use command:\n"
            "/setcity <city>"
        )
        return
    weather = await get_weather_tomorrow(city)
    await message.answer_animation(
        gif,
        caption=weather["text"]
    )



#clear data city
@router.message(Command("clearcity"))
async def clear_city(message: types.Message):
    from Bot_Weather.routers.database import clear_user_city

    if not full_city(message.from_user.id):
        await message.answer("You don't have a city set yet.")
        return

    clear_user_city(message.from_user.id)
    await message.answer("City removed successfully.")

#other messages ->
@router.message(F.photo | F.video | F.audio | F.file | F.document | F.location | F.contact | F.sticker | F.voice |F.text)
async def more_messages(message: types.Message):

    urlV ="https://animesher.com/orig/1/105/1051/10519/animesher.com_japanese-animation-weather-1051998.gif"
    await message.reply(text=f"{markdown.hide_link(urlV)}I would like to talk with you, but I can only show the weather...", parse_mode=ParseMode.HTML )


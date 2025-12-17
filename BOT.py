from aiogram import Bot, Dispatcher
from routers.database import LoggerMiddleware
import asyncio
from routers import commands_router
from routers.all_commands import scheduler
import logging



from config import BOT_TOKEN






async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    #Time task
    asyncio.create_task(scheduler(bot))


    #DB log
    dp.message.middleware(LoggerMiddleware())
    logging.basicConfig(level=logging.INFO)

    #all routers
    dp.include_router(commands_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())























#Исправить UTC


# простой бот для
# логирования данных (система готова)
# (показ погоды по расписанию)
# (показ командой сейчас) (выбранный город) +
# несколько команд для простых ответов -














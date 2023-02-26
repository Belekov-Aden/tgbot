from aiogram import Dispatcher, Bot, executor
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


if __name__ == '__main__':
    from handlers import dp, on_startapp
    executor.start_polling(skip_updates=True, dispatcher=dp, on_startup=on_startapp)

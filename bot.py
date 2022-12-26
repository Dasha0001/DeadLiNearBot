from aiogram import Bot, Dispatcher, executor, types
import re
import logging
from db import BotDB
from aiogram import Bot, Dispatcher
import config

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

BotDB = BotDB('DeadLine.db')


from bot import BotDB

@dp.message_handler(commands="start")
async def start(message: types.Message):
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    keyboard = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton(text="Начать")
    keyboard.add(button_1)
    button_2 = "Возможности"
    keyboard.add(button_2)
    button_3 = "Все задания"
    keyboard.add(button_3)
    await message.bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text =="Начать")
async def start(message: types.Message):
    if (not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    keyboard = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton(text="Начать")
    keyboard.add(button_1)
    button_2 = "Возможности"
    keyboard.add(button_2)
    button_3 = "Все задания"
    keyboard.add(button_3)
    await message.bot.send_message(message.from_user.id, "Это Дедлайнер Бот! Тут можно записать дедлайны!", reply_markup=keyboard)



@dp.message_handler(lambda message: message.text =="Возможности")
async def start(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Дедлайнер имеет команды /add - добавить дедлайн , /delete - удалить дедлайн, а так же кнопки посмотреть все задания и возможности")


@dp.message_handler(commands=("add", "delete", "s", "e"), commands_prefix="/!")
async def start(message: types.Message):
    cmd_variants = (('/add', '/a', '!add', '!a'), ('/delete', '/d', '!delete', '!d'))
    operation = '-' if message.text.startswith(cmd_variants[0]) else '+'

    value = message.text
    for i in cmd_variants:
        for j in i:
            value = value.replace(j, '').strip()

    if (len(value)):
        x =value
        if (len(x)):

            if (operation == '-'):
                await message.reply("✅ Добавление  <u><b> - данного дедлайна</b></u> успешно выполнено!")
                BotDB.add_record(message.from_user.id, operation, value)
            else:
                BotDB.delete_record(message.from_user.id, operation, value)
                await message.reply( "➖ Удаление   <u><b> - данного дедлайна</b></u>  успешно выполнено!")


        else:
            await message.reply("Не удалось определить дедлайн!")
    else:
        await message.reply("Не введена информация о дедлайне!")


@dp.message_handler(lambda message: message.text =="Все задания")
async def start(message: types.Message):

    records = BotDB.get_records(message.from_user.id)

    if (len(records)):
        answer = f"🕘 Все дедлайны \n"

        for r in records:
            answer +=  ("➖ Осталось  " )+ r[0]+"\n"
        await message.reply(answer)
    else:
        await message.reply("Записей не обнаружено!")




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

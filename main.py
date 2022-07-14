from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from secret_token import TOKEN_ST
from pars_file import download, create_connection, DATABASE_PATH, url

bot = Bot(token=TOKEN_ST)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    await msg.answer('Здравствуйте, введите название города и я выведу его население и ссылку на старницу в википедии\n'
                     'Для более подробной информации воспользуйтесть командой /help')


@dp.message_handler(commands=['start'])
async def help(msg: types.Message):
    await msg.answer('Для старта введите /start\n'
                     'Для обновления информации /parse\n'
                     'Для получения информации о городе введите его название')


@dp.message_handler(commands=['parse'])
async def parsing(msg: types.Message):
    await download(url[0])
    await msg.answer('Информация успешно загружена в базу данных')


@dp.message_handler(content_types=['text'])
async def text(msg: types.Message):
    text_received = msg.text
    connection = create_connection(DATABASE_PATH)
    cursor = connection.cursor()
    res = cursor.execute("SELECT * FROM City WHERE name=?", (text_received,)).fetchone()
    if res:
        await msg.answer(f"Город: {res[1]}\n"
                         f"Население: {res[2]}\n"
                         f"{res[3]}"
                         )
    else:
        res1 = cursor.execute("SELECT * FROM City WHERE name LIKE ?", ('%' + text_received + '%',)).fetchall()
        res2 = cursor.execute("SELECT * FROM City WHERE name LIKE ?",
                              ('%' + text_received.capitalize() + '%',)).fetchall()
        is_printed = []
        answer = 'Возможно Вы имели ввиду один из этих городов:\n'
        for el in res1 + res2:
            if el[1] not in is_printed:
                is_printed.append(el[1])
        answer += '\n'.join(is_printed)
        await msg.answer(answer)


if __name__ == '__main__':
    executor.start_polling(dp)

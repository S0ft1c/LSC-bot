from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
import app.keyboard as kb
from app.LSCpub import lsc_check
import os
import time

router = Router()  # for the connection between files

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        'Для получения информации надо ввести данные: API_URL, API_KEY, MAX_PRICE',
        reply_markup=kb.cmd_start_kb
    )

@router.callback_query(F.data == 'edit_params')
async def edit_params(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        text='*Для ввода параметров напишите сообщение.*\n_Сообщение должно быть формата:_\n' + \
             """```
API_URL = "<ваша ссылка>"
API_KEY = "<ваш токен>"
SERVICE = "<нужный вам сервис: tg, wa, tik-tok>"
MAX_PRICE = 20
MAX_THREADS = 25
             ```""" + '\n' + \
             '_Угловые скобочки не нужно писать.\nКавычки писать *нужно* (Обязательно двойные)\n' + \
             'Обязательно пишите праметры с новой строки._\n' + \
             '_*Обязательно* писать именно ` = ` с всеми пробелами. Просто скопируется пример и подставьте свои данные!_\n' + \
             '_Обязательно в том порядке, который указан в примере!_',
        parse_mode='Markdown'
    )

@router.message(F.text.contains('API_URL'))
async def editin_params(message: Message):
    try:
        # check for validate info
        dt = message.text.split(' = ')
        ddt = []
        for el in dt:
            ddt.extend(el.split('\n'))
        api_url, api_key, service, max_price, max_threads = \
            ddt[1].strip('"'), ddt[3].strip('"'), ddt[5].strip('"'), int(ddt[7]), int(ddt[9])


        result, log_file = lsc_check(
            api_url=api_url,
            api_key=api_key,
            service=service,
            max_price=max_price,
            max_threads=max_threads
        )
        print('results', result, log_file)
        if result == 'bad':
            await message.answer(
                text='Ошибка BAD_SERVICE\nЭта ошибка значит что-то из:\n' +
                    '1) Сервис приема смс сломался или отказал в работе по введенному вами api\n' +
                    '2) Данные, что вы ввели некорректны.\n' +
                    'Лучший способ починить это подождать',
            )
        elif not log_file:
            await message.answer(text=result)
        else:
            try:
                await message.answer_document(
                    document=FSInputFile(path=log_file, filename='output.txt'),
                    caption=result
                )
            except Exception as e:
                await message.answer_document(
                    document=FSInputFile(path=log_file, filename='output.txt'),
                    caption='Номера получены. Все данные записаны в файл'
                )
            try:
                os.remove(log_file)  # delete noneeded file
            except: print('no file to remove')
    except Exception as e:
        await message.answer(text='Что-то пошло не так... Проверьте формат данных и их валидность.')
        print(e)
        try:
            os.remove(log_file)  # delete noneeded file
        except: print('no file to remove')
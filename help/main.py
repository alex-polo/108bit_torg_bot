from typing import List

from aiogram import types, Bot
from aiogram.dispatcher.filters import MediaGroupFilter
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import KeyboardButton, ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_media_group import *

from con import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

step = -1
post = []
back = KeyboardButton(text="⬅️ - Назад")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    query = "Привествую!\nЯ задам вам несколько вопросов и помогу правильно сформировать объявление."
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    reply.add(KeyboardButton(text="Поехали!"))
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)


async def country(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Из какого вы города"
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

async def task(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Какая у вас задача?"
    bottom_bay = KeyboardButton(text="Хочу купить")
    bottom_sell = KeyboardButton(text="Хочу продать")
    reply.add(bottom_bay, bottom_sell, back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)

async def type_product(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Какой тип оборудования/расходных материалов вы предлагаете/ищете?"
    sys_seq = KeyboardButton(text="Системы безопасности")
    auto_qp = KeyboardButton(text="Автоматика и КИПиА")
    smart_h = KeyboardButton(text="Умный дом")
    electro = KeyboardButton(text="Электрика")
    tele_nt = KeyboardButton(text="Телеком и связь")
    serv_pc = KeyboardButton(text="Сервера, ПК и комплектующие")
    reply.add(sys_seq, auto_qp, smart_h, electro, tele_nt, serv_pc, back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)

async def manufacture(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Укажите производителя."
    reply.add(back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)
async def amount(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Укажите количество единиц (число)."
    reply.add(back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)

async def status(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Укажите состояние."
    new = KeyboardButton(text="Новое")
    bu = KeyboardButton(text="Б/У")
    reply.add(new, bu, back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)

async def company_or_fiz(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Вы представитель компании или частное лицо?"
    fiz = KeyboardButton(text="Частное лицо")
    company = KeyboardButton(text="Компания")
    reply.add(fiz, company, back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)

async def sale(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Укажите стоимость (число в рублях)."
    other = KeyboardButton(text="По договорённости")
    reply.add(other, back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)

async def type_pay(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Укажите тип оплаты."
    nal = KeyboardButton(text="Нал")
    beznal = KeyboardButton(text="Безнал")
    reply.add(nal, beznal, back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)

async def delivery(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Есть ли отправка в другой город?"
    yes = KeyboardButton(text="Да")
    no = KeyboardButton(text="Нет")
    reply.add(yes, no, back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)

async def mail(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Укажите электронную почту для связи."
    reply.add(back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)
async def phone(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Укажите контактный телефон для связи."
    reply.add(back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)

async def description(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = " Кратко опишите модель оборудования, условия оплаты, доставки и другую необходимую информацию."
    reply.add(back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)

async def photo(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Приложите фото."
    skip = KeyboardButton(text="Пропустить")
    next = KeyboardButton(text="Далее")
    reply.add(skip, next, back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)

async def price_list(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Если позиций много, приложите прайс-лист."
    skip = KeyboardButton(text="Пропустить")
    next = KeyboardButton(text="Далее")
    reply.add(skip, next, back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)

async def final(message):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    query = "Поздравляю! Вы сформировали объявление."
    publish = KeyboardButton(text="Опубликовать!")
    reply.add(publish, back)
    await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
                           reply_markup=reply)

functions = [country, task, type_product, manufacture, amount, status, company_or_fiz, sale, type_pay, delivery, mail, phone, description, photo, price_list, final]
bs, specific, country_h = "", "", ""
hashtags = []
photo_r, docs = types.MediaGroup(), types.MediaGroup()
docs_files, files = [], []

@dp.message_handler(content_types=ContentType.PHOTO)
async def album_handler(messages: List[types.Message]):
    global step, files
    print(step)
    if step==13:
        ph = messages
        p_res = ph.photo
        files.append(p_res[0])

@dp.message_handler(content_types=ContentType.DOCUMENT)
async def docs_handler(messages: List[types.Message]):
    global step
    print(step)
    if step==14:
        doc = messages
        d_res = doc.document
        print(d_res)
        docs_files.append(d_res)
#        await bot.send_document(messages.chat.id, document=d_res.file_id)


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    global step
    print(step)
    if message.text == back.text:
        step -= 1
        post.pop(-1)
        await functions[step](message)
    else:
        global hashtags, specific, bs
        if step==1:
            if message.text=="Хочу купить":
                bs = "#Куплю"
            else:
                bs = "#Продам"
        elif step==9 and message.text=="Да":
            message.text="Есть"
        elif step==2 or step==0 or step==1 or step==3:
            specific = "#"+ message.text.replace(" ", "_")
        hashtags = [specific, bs, specific, specific, "Количество: ", "Состояние: ", "Продавец: ", "Стоимость: ",
                    "Оплата: ", "Отправка: ", "E-mail: ", "Телефон: ", "Объявление: "]
        if step>=4:
            if step==15 and message.text=="Опубликовать!":
                global files, docs, docs_files
                post[0], post[1] = post[1], post[0]
                try:
                    for f in files[:-1]:
                        photo_r.attach_photo(f.file_id)
                    photo_r.attach_photo(files[-1].file_id, caption="".join(post))
                    await bot.send_media_group(message.chat.id, media=photo_r)
                    await bot.send_media_group("@jsjddfgyy", media=photo_r)
                except Exception:
                    await bot.send_message("@jsjddfgyy", text="".join(post))

                try:
                    for f in files[:-1]:
                        docs.attach_document(f.file_id)
                    docs.attach_document(docs_files[-1].file_id, caption="Прайс лист")
                    await bot.send_media_group(message.chat.id, media=docs)
                    await bot.send_media_group("@jsjddfgyy", media=docs)
                except Exception as e:
                    print(e)
                step = -1
                post.clear()
            elif message.text!="Пропустить" and message.text!="Далее":
                print(message.text)
                post.append(hashtags[step]+message.text+"\n")
            elif step==4:
                message.text = message.text + " шт"
        else:
            if step!=-1:
                post.append(str(hashtags[step])+"\n")
        print("".join(post))
        step += 1
        await functions[step](message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

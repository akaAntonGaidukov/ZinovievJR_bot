
# Not in use
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import random

import re

# Bot
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Methods
import pars
import config
import translators as ts
import translators.server as tss
API_TOKEN = config.TG_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Functions 
def translate_ru(wyw_text):
    from_language, to_language = 'en', 'ru'
    translated_text = tss.google(wyw_text, from_language, to_language)
    return translated_text


def dump_to_log(data):
    try:
        file = open("ER.txt", "x",encoding="utf-8")
        file.close()

    except Exception as err:
        print([err,"НУ НЕ МООООГУУУУ ЯЯЯЯЯЯЯ, все ок."])

    with open("ER.txt", "a",encoding="utf-8") as file:
        file.write(data)
        file.close()

def text_handler(text):
    
    if "!g" in text:
        return "good"


def keybord_answ(query, lang='en'):
    
    variants = pars.search_gl(query)
    
    
    rw = len(variants)%2
    ikm = InlineKeyboardMarkup(row_width=rw)

    if len(variants)>0:
        ib1 = InlineKeyboardButton(
            text=variants[0]["title"].replace("_"," "),
            callback_data=(variants[0]["link"]+";"+lang)
        )
        variants.pop(0)
        ikm.add(ib1)

    if len(variants)>0:
        ib2 = InlineKeyboardButton(
            text=variants[0]["title"].replace("_"," "),
            callback_data=(variants[0]["link"]+";"+lang)
        )
        variants.pop(0)
        ikm.insert(ib2)

    if len(variants)>0:
        ib3 = InlineKeyboardButton(
            text=variants[0]["title"].replace("_"," "),
            callback_data=(variants[0]["link"]+";"+lang)
        )
        variants.pop(0)
        ikm.insert(ib3)

    if len(variants)>0:
        ib4 = InlineKeyboardButton(
            text=variants[0]["title"].replace("_"," "),
            callback_data=(variants[0]["link"]+";"+lang)
        )
        variants.pop(0)
        ikm.insert(ib4)

    return ikm


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.answer(
        """Hi, i`m Zinoviev Jr. to your service!\n
I can search SLB Glossary for you with a \t /g 'you`r querry' command\t
To see additional functionality please run\t/help command
Also you can leave a enchancment request with a\t/er command."""
    )
@dp.message_handler(commands=["help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/help` command
    """
    await message.answer(
        """*\t\tHELP\t\t*
    /g [text] - Search SLB Glossary
    /gr [text] - Search SLB Glossary and translate article to Russian
    /er [text] - Enchancment request

        """
    )

@dp.message_handler(commands=["er"])
async def send_welcome(message: types.Message):
    """
    This handler will save ER message to the queue
    """
    dump_to_log(f"\n{message.text[4:]},{message.from_user.id},{message.from_user.first_name},{message.from_user.last_name}")

    await message.answer("Your ER has been added to queue")



@dp.message_handler(commands=["g"])
async def give_choice(message: types.Message):
    print(message.text)
    query = str(message.text[3:])
   
    
    await bot.send_message(
        chat_id = message.from_user.id,
        text="Please choose a sutable querry",
        reply_markup=keybord_answ(query)
        )


@dp.message_handler(commands=["gr"])
async def give_choice(message: types.Message):
    print(message.text)
    query = str(message.text[4:])
    
    await bot.send_message(
        chat_id = message.from_user.id,
        text="Пожалуйста выберите подходящий запрос",
        reply_markup=keybord_answ(query,"ru")
        )

@dp.callback_query_handler()
async def send_result(callback: types.CallbackQuery):
    link,_,lang = callback.data.partition(";")
    title,article,img_links = pars.get_content(link)
    if lang == 'ru':
        await callback.answer(text=f"Ищу {title}")
    
        if len(img_links)>0:
            await bot.send_photo(chat_id=callback.from_user.id,photo=img_links[0],caption=f"{title}\n{translate_ru(article)}\n{callback.data}")
        else:
            await bot.send_message(chat_id=callback.from_user.id,text=f"{title}\n{translate_ru(article)}\n{callback.data}")

    else:
        await callback.answer(text=f"One sec.. finding {title}")

        if len(img_links)>0:
            await bot.send_photo(chat_id=callback.from_user.id,photo=img_links[0],caption=f"{title}\n{article}\n{callback.data}")
        else:
            await bot.send_message(chat_id=callback.from_user.id,text=f"{title}\n{article}\n{callback.data}")



@dp.message_handler()
async def not_a_comand(message: types.Message):
    """
    This handler will handle all text exept 
    """

    await message.answer(f'Sorry, im working RN...')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
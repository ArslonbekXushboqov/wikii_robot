from logging import exception
from aiogram import types, Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from bot.dbcon import *
from bot.config import *
from bot.buttons import *
import wikipedia as w
import bot.send_to_alls as send_to_alls

langs = {
    "uz": "🇺🇿 Uzbekcha",
    "ru": "🇷🇺 Ruscha",
    "en": "🇺🇸 Inglizcha"
}
bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher(bot)

async def on_startup(_):
    print("Bot ishga tushdi!")

async def lang_edit_text(msg: Message):
    await msg.edit_text(f"Salom, ushbu bot orqali wikipediadan ma'lumot qidirsangiz bo'ladi.\n\n<b>Hozirgi qidiruv tili: {langs[detect_lang(msg.chat.id)]}\nQidiruv tilini o'zgartirishingiz mumkin</b>👇", reply_markup=til)

@dp.message_handler(text=['/send'], is_reply=True)
async def admin(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup()

    keyboard_markup.add(
        types.InlineKeyboardButton('Yuborish', callback_data='send-all'),
    )
    if message.from_user.id == admin_id:
        await message.reply_to_message.reply("Barchasi to'g'ri bo'lsa yuborish tugmasini bosing",
                                            reply_markup=keyboard_markup)
    else:
        pass

'''*********----------Admin buyruqlari---------*********'''

@dp.callback_query_handler(text=['send-all'])
async def answer_call(query: types.CallbackQuery):
    await query.message.edit_text("Yuborilmoqda...")
    send_wait = await send_to_alls.broadcaster(query.message.reply_to_message)
    await query.message.edit_text(str(send_wait))

@dp.message_handler(commands=['stat'])
async def _(message: types.Message):
    if message.from_user.id == admin_id:
        Stat = stat()
        await message.reply(f"Userlar: {Stat} ta.")
    else:
        pass
    
'''*********----------Admin buyruqlari---------*********'''
@dp.message_handler(commands=['start','lang'], chat_type='private')
async def start_msg(msg: Message):
    chat_id = msg.from_user.id
    name = msg.from_user.first_name
    lang = "uz"
    insert_user_data(name,chat_id,lang)
    await bot.send_message(chat_id, f"Salom, ushbu bot orqali wikipediadan ma'lumot qidirsangiz bo'ladi.\n\n<b>Hozirgi qidiruv tili: {langs[detect_lang(chat_id)]}\nQidiruv tilini o'zgartirishingiz mumkin</b>👇", reply_markup=til)
@dp.callback_query_handler(Text(startswith="lang"))
async def change_lang(call: types.CallbackQuery):
    lan=call.data.split("_")[1]
    w.set_lang(lan)
    chatid = call.message.chat.id
    uplang(lan, chatid)
    await call.answer(text = f"Til {langs[lan]} ga o'zgartirildi!", show_alert=False)
    await lang_edit_text(call.message)

@dp.message_handler()
async def search(msg: Message):
    chat_id = msg.from_user.id
    try:
        w.set_lang(detect_lang(chat_id))
        m=w.summary(msg.text)
        if len(m) > 4095:
            for x in range(0, len(m), 4095):
                await msg.answer(text=m[x:x+4095])
        else:
            await msg.answer(m)
    except Exception as ex:
        await msg.answer("Sizning so'rovingiz bo'yicha hech narsa topilmadi! 🥲")


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


til = InlineKeyboardMarkup(row_with=3)
til_key = [        
    InlineKeyboardButton('πΊπΏ UZ', callback_data='lang_uz'),
    InlineKeyboardButton('π·πΊ RU', callback_data='lang_ru'),
    InlineKeyboardButton('πΊπΈ EN', callback_data='lang_en')
    ]
til.add(*til_key)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


til = InlineKeyboardMarkup(row_with=3)
til_key = [        
    InlineKeyboardButton('🇺🇿 UZ', callback_data='lang_uz'),
    InlineKeyboardButton('🇷🇺 RU', callback_data='lang_ru'),
    InlineKeyboardButton('🇺🇸 EN', callback_data='lang_en')
    ]
til.add(*til_key)

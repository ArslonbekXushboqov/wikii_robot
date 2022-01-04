import asyncio
import logging
from aiogram.utils import exceptions
from bot.dbcon import *

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')



async def send_message(user_id: int, msg) -> bool:

    try:
        await msg.copy_to(chat_id=user_id, reply_markup=msg.reply_markup)
    except exceptions.BotBlocked:
        pass
    except exceptions.ChatNotFound:
        pass
    except exceptions.RetryAfter as e:
        await asyncio.sleep(e.timeout)
        await msg.copy_to(chat_id=user_id, reply_markup=msg.reply_markup)
    except exceptions.UserDeactivated:
        pass
    except exceptions.MigrateToChat as e:
        try:
            await msg.copy_to(chat_id=e.migrate_to_chat_id, reply_markup=msg.reply_markup)
        except:
            pass
    except exceptions.TelegramAPIError:
        pass
    else:
        pass
        return True
    return False


async def broadcaster(msg) -> str:
    cur.execute("SELECT chat_id FROM user")
    usersid = cur.fetchall()
    sends = 0
    error_sends = 0
    try:
        for user_id in usersid:
            user_id = user_id[0]
            if await send_message(user_id=user_id, msg=msg):
                sends += 1
            else:
                error_sends += 1
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        log.info(f"{sends} messages successful sent.\n{error_sends} messages notsuccessful sent.")

    return f"Yuborildi: {sends}\nYuborilmadi: {error_sends}"

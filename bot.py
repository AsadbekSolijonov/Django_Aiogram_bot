import asyncio
import logging
import sys
import os
import django

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

# Django ORM bilan asinxron ishlash uchun juda muhim.
from asgiref.sync import sync_to_async

# Django'ni sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django.setup()

# Django modelni import qilish
from account.models import User

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7002206053:AAFpnCELhTXBAmktLT_xta21TAUDxnRLN_c"

dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

    user, created = await sync_to_async(User.objects.get_or_create)(
        telegram_id=message.from_user.id,
        defaults={'username': message.from_user.username}
    )

    users = await sync_to_async(lambda: list(User.objects.all()))()
    user_list = "\n".join([f"{u.username}: chat_id: {u.telegram_id}" for u in users])

    if created:
        await message.answer(f"Xush kelibsiz, yangi foydalanuvchi!")
    else:
        date_time = user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        await message.answer(f"Siz {date_time} sanada ro'yxatdan o'tgansiz!")
        await message.answer(f"{user_list}")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

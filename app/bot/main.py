import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.adapters.registry import build_adapters
from app.config import settings


dp = Dispatcher()
SOURCE_NAMES = ", ".join(sorted(adapter.source_name for adapter in build_adapters()))


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        "Привет! Я ScriptBot. Используйте /search <название>, чтобы найти мангу по всем источникам."
    )


@dp.message(Command("sources"))
async def sources_handler(message: Message) -> None:
    await message.answer(f"Подключенные источники: {SOURCE_NAMES}")


async def run_bot() -> None:
    bot = Bot(token=settings.telegram_bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())

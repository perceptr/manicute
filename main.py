from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.dispatcher.filters import Text
from handlers import *
import logging
import asyncio


# API_TOKEN = '5944070095:AAF3q6ctOAVCBw8FY9JvGsAmskuKAELz6_A'
API_TOKEN = '5768637891:AAFXvKfqu0Dip25TnKs06ZeQx0Rt8_etizs'
logger = logging.getLogger(__name__)


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Подобрать подходящий маникюр: (/manicure) ...",
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено",
                         reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена",
                                                 ignore_case=True), state="*")


def register_handlers_manicure(dp: Dispatcher):
    dp.register_message_handler(start, commands="manicure", state="*")
    dp.register_message_handler(size_chosen,
                                state=Manicure.waiting_for_size)
    dp.register_message_handler(color_type_chosen,
                                state=Manicure.waiting_for_color_type)
    dp.register_message_handler(color_chosen,
                                state=Manicure.waiting_for_color)
    dp.register_message_handler(form_chosen,
                                state=Manicure.waiting_for_form)
    dp.register_message_handler(top_chosen,
                                state=Manicure.waiting_for_top)
    dp.register_message_handler(small_volume_chosen,
                                state=Manicure.waiting_for_small_volume)
    dp.register_message_handler(big_volume_chosen,
                                state=Manicure.waiting_for_big_volume)
    dp.register_message_handler(drawing_chosen,
                                state=Manicure.waiting_for_drawing)
    dp.register_message_handler(classic_chosen,
                                state=Manicure.waiting_for_classic)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/manicure", description="Подобрать маникюр"),
        # BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_common(dp)
    register_handlers_manicure(dp)

    await set_commands(bot)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())

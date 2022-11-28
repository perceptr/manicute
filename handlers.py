from aiogram import types
from aiogram.dispatcher import FSMContext
from available_options import *
from aiogram.dispatcher.filters.state import State, StatesGroup
from db_handler import DBHandler
from ya_translator import Translator
from yandex_image_getter import YandexImageGetter
import logging
from token_manager import CredentialsTable
from pinterester import Pinterester
from new_ya_parser import NewYandexSearcher

creds = CredentialsTable('credentials.db')
db_handler = DBHandler(creds.get_last_created_cred("user"),
                       creds.get_last_created_cred("password"),
                       creds.get_last_created_cred("host"),
                       creds.get_last_created_cred("port"),
                       creds.get_last_created_cred("database"))
pinterester = Pinterester()

prepare_string = lambda input_string: f"= '{input_string}'" if input_string != 'NULL' else 'IS NULL'
check_nd_in_color = lambda color: True if color.endswith('_nd') else False
manage_color_shades_for_translation = lambda color: (get_reversed_dict(available_colors)[color[:-3]], "") \
    if check_nd_in_color(color) else (get_reversed_dict(available_colors)[color], "")
manage_if_skip_included = lambda msg: "" if "Пропустить" in msg else msg


def get_translated_query_from_yandex(query: str) -> list[str]:
    # translated_query = Translator(creds.get_last_created_cred('IAM_TOKEN'),
    #                               creds.get_last_created_cred('folder_id')) \
    #     .translate(query)

    # logging.info(f"Translated query: {translated_query}")
    # result = YandexImageGetter(query).search()
    result = NewYandexSearcher(query).search()
    return result


class Manicure(StatesGroup):
    waiting_for_size = State()
    waiting_for_color_type = State()
    waiting_for_color = State()
    waiting_for_form = State()
    waiting_for_top = State()
    waiting_for_small_volume = State()
    waiting_for_big_volume = State()
    waiting_for_drawing = State()
    waiting_for_classic = State()


async def start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_sizes:
        keyboard.add(size)
    await message.answer("Какого размера?", reply_markup=keyboard)
    await state.set_state(Manicure.waiting_for_size.state)


async def size_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_sizes:
        await message.answer("Пожалуйста, выберите длину, "
                             "используя клавиатуру ниже.")
        return
    await state.update_data(chosen_size=available_sizes[message.text])
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    colors = list(available_colors)
    for i in range(4):
        keyboard.add(*colors[i * 4:(i + 1) * 4])
    await state.set_state(Manicure.waiting_for_color.state)
    await message.answer("Какого цвета?", reply_markup=keyboard)


async def color_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_colors:
        await message.answer("Пожалуйста, выберите цвет, "
                             "используя клавиатуру ниже.")
        return
    await state.update_data(chosen_color=available_colors[message.text])
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for color_type in available_color_types:
        keyboard.add(color_type)
    await state.set_state(Manicure.waiting_for_color_type.state)
    await message.answer("Нюдовые или яркие?", reply_markup=keyboard)


async def color_type_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_color_types:
        await message.answer("Пожалуйста, выберите тип, "
                             "используя клавиатуру ниже.")
        return

    user_data = await state.get_data()
    if message.text == "Нюдовые":
        await state.update_data(chosen_color=user_data['chosen_color'])
        await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())

    user_data = await state.get_data()
    query = "SELECT photo_url FROM photos WHERE size %s AND color %s" % (prepare_string(user_data['chosen_size']),
                                                                         prepare_string(user_data['chosen_color']))
    logging.info(f"PHOTO QUERY: {query}")
    links = db_handler.execute_where_query(query)
    if not links:
        await message.answer("Извините, такой конфигурации в нашей базе нет, ищем в Яндексе")
        await message.reply("Хм", reply_markup=types.ReplyKeyboardRemove())

        # nude is banned in yandex, so we need to delete it from query anyway when we send it to yandex

        query_to_translate = f"{get_reversed_dict(available_sizes)[user_data['chosen_size']]} " \
                             f"{' '.join(manage_color_shades_for_translation(user_data['chosen_color']))} ногти"
        logging.info(f"query to translate: {query_to_translate}")
        yandex_search_result = get_translated_query_from_yandex(query_to_translate)
        # pinterest_search_result = pinterester.search(query_to_translate)
        result = yandex_search_result
        await message.answer("Вот, что нашлось в интернете:")
        for link in result:
            await message.answer_photo(link)
    else:
        await message.answer("Вот фото, которые мы нашли:")
        sent_photos = []
        for link in links:
            await message.answer_photo(link[0])
            sent_photos.append(link[0])

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for form in available_forms:
        keyboard.add(form)
    await state.set_state(Manicure.waiting_for_form.state)
    await message.answer("Какой формы?", reply_markup=keyboard)


async def form_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_forms:
        await message.answer("Пожалуйста, выберите форму, "
                             "используя клавиатуру ниже.")
        return
    await state.update_data(chosen_form=available_forms[message.text])
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for top in available_tops:
        keyboard.add(top)
    await state.set_state(Manicure.waiting_for_top.state)
    await message.answer("Какой топ?", reply_markup=keyboard)


async def top_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_tops:
        await message.answer("Пожалуйста, выберите топ, "
                             "используя клавиатуру ниже.")
        return
    await state.update_data(chosen_top=available_tops[message.text])
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_data = await state.get_data()

    query = "SELECT photo_url FROM photos WHERE size %s AND color %s AND form %s " \
            "AND (photos.design).top %s" \
            % (prepare_string(user_data['chosen_size']),
               prepare_string(user_data['chosen_color']),
               prepare_string(user_data['chosen_form']),
               prepare_string(user_data['chosen_top']))
    logging.info(f"PHOTO QUERY: {query}")
    links = db_handler.execute_where_query(query)
    if not links:
        await message.answer("Извините, такой конфигурации в нашей базе нет(")
        await message.reply("Хм", reply_markup=types.ReplyKeyboardRemove())

        query_to_translate = f"{get_reversed_dict(available_sizes)[user_data['chosen_size']]} " \
                             f"{' '.join(manage_color_shades_for_translation(user_data['chosen_color']))}" + \
                             f" {get_reversed_dict(available_forms)[user_data['chosen_form']]} " \
                             f"{get_reversed_dict(available_tops)[user_data['chosen_top']]} ногти"
        logging.info(f"query to translate: {query_to_translate}")
        yandex_search_result = get_translated_query_from_yandex(query_to_translate)
        # pinterest_search_result = pinterester.search(query_to_translate)
        result = yandex_search_result
        await message.answer("Вот, что нашлось в интернете:")
        for link in result:
            await message.answer_photo(link)

    else:
        await message.answer("Вот фото, которые мы нашли:")
        for link in links:
            await message.answer_photo(link[0])

    for small_volume in available_small_volume:
        keyboard.add(small_volume)
    await state.set_state(Manicure.waiting_for_small_volume.state)
    await message.answer("Небольшие элементы?", reply_markup=keyboard)


async def small_volume_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_small_volume:
        await message.answer("Пожалуйста, выберите элемент, "
                             "используя клавиатуру ниже.")
        return

    await state.update_data(chosen_small_volume=available_small_volume[message.text])
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for big_volume in available_big_volume:
        keyboard.add(big_volume)
    await state.set_state(Manicure.waiting_for_big_volume.state)
    await message.answer("Элементы побольше?", reply_markup=keyboard)


async def big_volume_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_big_volume:
        await message.answer("Пожалуйста, выберите элемент, "
                             "используя клавиатуру ниже.")
        return
    await state.update_data(
        chosen_big_volume=available_big_volume[message.text])

    user_data = await state.get_data()

    query = "SELECT photo_url FROM photos WHERE size %s AND color %s AND form %s " \
            "AND (photos.design).top %s AND (photos.design).volume_small %s " \
            "AND (photos.design).volume_big %s" \
            % (prepare_string(user_data['chosen_size']),
               prepare_string(user_data['chosen_color']),
               prepare_string(user_data['chosen_form']),
               prepare_string(user_data['chosen_top']),
               prepare_string(user_data['chosen_small_volume']),
               prepare_string(user_data['chosen_big_volume']))

    links = db_handler.execute_where_query(query)
    if not links:
        await message.answer("Извините, такой конфигурации в нашей базе нет(")
        await message.reply("Хм", reply_markup=types.ReplyKeyboardRemove())

        query_to_translate = \
            f"{get_reversed_dict(available_sizes)[user_data['chosen_size']]} " \
            f"{' '.join(manage_color_shades_for_translation(user_data['chosen_color']))}" + \
            f" {get_reversed_dict(available_forms)[user_data['chosen_form']]} " \
            f"{get_reversed_dict(available_tops)[user_data['chosen_top']]} ногти" + \
            f" {manage_if_skip_included(get_reversed_dict(available_small_volume)[user_data['chosen_small_volume']])} " \
            f" {manage_if_skip_included(get_reversed_dict(available_big_volume)[user_data['chosen_big_volume']])}"

        logging.info(f"query to translate: {query_to_translate}")
        yandex_search_result = get_translated_query_from_yandex(query_to_translate)
        # pinterest_search_result = pinterester.search(query_to_translate)
        result = yandex_search_result
        for link in result:
            await message.answer_photo(link)
    else:
        await message.answer("Вот фото, которые мы нашли:")
        for link in links:
            await message.answer_photo(link[0])

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for drawing in available_drawings:
        keyboard.add(drawing)
    await state.set_state(Manicure.waiting_for_drawing.state)
    await message.answer("Рисунок?", reply_markup=keyboard)


async def drawing_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_drawings:
        await message.answer("Пожалуйста, выберите рисунок, "
                             "используя клавиатуру ниже.")
        return
    await state.update_data(chosen_drawing=available_drawings[message.text])
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for classic in available_classics:
        keyboard.add(classic)
    await state.set_state(Manicure.waiting_for_classic.state)
    await message.answer("Классические варианты?", reply_markup=keyboard)


async def classic_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_classics:
        await message.answer("Пожалуйста, выберите вариант, "
                             "используя клавиатуру ниже.")
        return
    await state.update_data(chosen_classic=available_classics[message.text])
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())

    user_data = await state.get_data()

    query = "SELECT photo_url FROM photos WHERE size %s AND color %s AND form %s " \
            "AND (photos.design).top %s AND (photos.design).volume_small %s " \
            "AND (photos.design).volume_big %s AND (photos.design).drawing %s " \
            "AND (photos.design).classic %s" \
            % (prepare_string(user_data['chosen_size']),
               prepare_string(user_data['chosen_color']),
               prepare_string(user_data['chosen_form']),
               prepare_string(user_data['chosen_top']),
               prepare_string(user_data['chosen_small_volume']),
               prepare_string(user_data['chosen_big_volume']),
               prepare_string(user_data['chosen_drawing']),
               prepare_string(user_data['chosen_classic']))

    links = db_handler.execute_where_query(query)
    if not links:
        await message.answer("Извините, такой конфигурации в нашей базе нет(")

        await message.answer("Смотрите, что мы нашли в Яндексе:")
        await message.reply("Хм", reply_markup=types.ReplyKeyboardRemove())
        user_data = await state.get_data()

        query_to_translate \
            = f"{get_reversed_dict(available_sizes)[user_data['chosen_size']]} " \
              f"{' '.join(manage_color_shades_for_translation(user_data['chosen_color']))}" + \
              f" {get_reversed_dict(available_forms)[user_data['chosen_form']]} " \
              f"{get_reversed_dict(available_tops)[user_data['chosen_top']]} ногти" + \
              f" {manage_if_skip_included(get_reversed_dict(available_small_volume)[user_data['chosen_small_volume']])} " \
              f" {manage_if_skip_included(get_reversed_dict(available_big_volume)[user_data['chosen_big_volume']])}" + \
              f" {manage_if_skip_included(get_reversed_dict(available_drawings)[user_data['chosen_drawing']])} " \
              f"{manage_if_skip_included(get_reversed_dict(available_classics)[user_data['chosen_classic']])}"

        logging.info(f"query to translate: {query_to_translate}")
        yandex_search_result = get_translated_query_from_yandex(query_to_translate)
        # pinterest_search_result = pinterester.search(query_to_translate)
        result = yandex_search_result
        for link in result:
            await message.answer_photo(link)
    else:
        await message.answer("Вот фото, которые мы нашли:")
        for link in links:
            await message.answer_photo(link[0])

    # offer to start again
    await state.set_state(Manicure.waiting_for_size.state)
    # await message.answer("Хотите начать сначала?", reply_markup=types.ReplyKeyboardRemove())
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Да")
    keyboard.add("Нет")
    await state.set_state(Manicure.waiting_for_classic.state)
    await message.answer("Хуярим заново?", reply_markup=keyboard)

    # await message.answer(
    #     f"{user_data['chosen_size']} {user_data['chosen_color']} "
    #     f"{user_data['chosen_form']} {user_data['chosen_top']} "
    #     f"{user_data['chosen_small_volume']} {user_data['chosen_big_volume']} "
    #     f"{user_data['chosen_drawing']} {user_data['chosen_classic']}\n",
    #     reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

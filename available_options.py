def get_reversed_dict(dictionary: dict) -> dict:
    return {v: k for k, v in dictionary.items()}


available_sizes = {"Короткие": 'small',
                   "Средние": 'medium',
                   "Длинные": 'large',
                   "Очень длинные": 'xlarge'}

available_color_types = ["Нюдовые", "Яркие"]

available_colors = {"Черные": 'black',
                    "Белые": 'white',
                    "Розовые": 'pink',
                    "Красные": 'red',
                    "Зеленые": 'green',
                    "Синие": 'dark_blue',
                    "Голубой": 'light_blue',
                    "Желтые": 'yellow',
                    "Оранжевые": 'orange',
                    "Фиолетовые": 'purple',
                    "Коричневые": 'brown',
                    "Серые": 'grey',
                    "Золотые": 'gold',
                    "Серебряные": 'silver',
                    "Бронзовые": 'bronze',
                    "Разноцветные": 'multicolor',
                    "Бежевые": 'beige'}


available_forms = {"Квадрат": 'square',
                   "Миндаль": 'almond',
                   "Овал": 'ellipse',
                   "Стилет": 'stylet',
                   "Балерина": 'ballerina'}

available_tops = {"Матовый": 'matte',
                  "Глянцевый": 'glossy'}

available_small_volume = {"Стразы": 'rhinestones',
                          "Бусины": 'beads',
                          "Бульонки": 'broths',
                          "Пропустить": "NULL"}

available_big_volume = {"Цепочки": 'chains',
                        "Пирсинг": 'piercing',
                        "Фигурки": 'figures',
                        "Пропустить": "NULL"}

available_drawings = {"От руки": 'by_hand',
                      "Стемпинг": 'stamping',
                      "Слайдеры": 'sliders',
                      "Пропустить": "NULL"}

available_classics = {"Френч": 'french',
                      "Лунка": 'cuticle',
                      "Пропустить": "NULL"}

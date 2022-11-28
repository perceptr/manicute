from enum import Enum


class ColorShades(Enum):
    NUDE = "Нюдовые"
    SATURATED = "Яркие"


class Color(Enum):
    BLACK = "Чёрный"
    WHITE = "Белый"
    RED = "Красный"
    ORANGE = "Оранжевый"
    YELLOW = "Жёлтый"
    GREEN = "Зелёный"
    LIGHT_BLUE = "Голубой"
    DARK_BLUE = "Синий"
    PURPLE = "Фиолетовый"
    PINK = "Розовый"
    BROWN = "Коричневый"
    BRONZE = "Бронзовый"
    SILVER = "Серебряный"
    GOLD = "Золотой"
    GRAY = "Серый"
    BEIGE = "Бежевый"
    MULTICOLOR = "Цветной"


class Size(Enum):
    SMALL = "Короткие"
    MEDIUM = "Средние"
    LARGE = "Длинные"
    XLARGE = "Очень длинные"


class Form(Enum):
    SQUARE = "Квадрат"
    ELLIPSE = "Овал"
    ALMOND = "Миндаль"
    STYLET = "Стилет"
    BALLERINA = "Балерина"


class Top(Enum):
    MATTE = "Матовый"
    GLOSSY = "Глянцевый"


class Classic(Enum):
    FRENCH = "Френч"
    CUTICLE = "ЛУНКА"


class Drawing(Enum):
    BY_HAND = "От руки"
    STAMPING = "Стемпинг"
    SLIDERS = "Слайдеры"


class VolumeBig(Enum):
    CHAINS = "Цепочки"
    PIERCING = "Пирсинг"
    FIGURES = "Фигурки"


class VolumeSmall(Enum):
    GLITTER = "Глиттер"
    RHINESTONES = "Стразы"
    BEADS = "Бусины"
    BROTHS = "Бульонки"
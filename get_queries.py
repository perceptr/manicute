from itertools import product
from new_ya_parser import NewYandexSearcher
from get_images_for_db import save_image

color = ['red', 'green', 'dark_blue', 'light_blue', 'yellow', 'orange',
         'purple', 'pink', 'black', 'white', 'brown', 'grey', 'gold',
         'silver', 'bronze', 'multicolor', 'red_nd', 'green_nd',
         'dark_blue_nd', 'light_blue_nd', 'yellow_nd', 'orange_nd',
         'purple_nd', 'pink_nd', 'black_nd', 'white_nd', 'brown_nd',
         'grey_nd', 'gold_nd', 'silver_nd', 'bronze_nd', 'multicolor_nd',
         'beige', 'beige_nd']
drawings = ['by_hand', 'stamping', 'sliders']
forms = ['square', 'ellipse', 'almond', 'stylet', 'ballerina']
size = ['small', 'medium', 'large', 'xlarge']
tops = ['matte', 'glossy']
volume_small = ['glitter', 'rhinestones', 'beads', 'broths']
volume_big = ['chains', 'piercing', 'figures']

queries = set()

for perm in product(color, size, tops):

    queries.add(' '.join(str(perm)[2:-2].split('\', \'')))

count_q = len(queries)
for i in range(5):
    query = queries.pop() + ' manicure'
    print(query)
    searcher = NewYandexSearcher(query)
    request = searcher.search()
    for request in request:
        save_image('additional_base/',
                   f'{request}', request)
    # /Users/glebkochergin/Desktop/Python/manicure_base/addit_base






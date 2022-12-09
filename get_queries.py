from itertools import product
from new_ya_parser import NewYandexSearcher

classic = ['cuticle', 'french']
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

queries = [' '.join(str(perm)[2:-2].split('\', \''))
           for perm in product(classic, color, size)]
print(*queries, sep='\n')
print(len(queries))


for perm in product(classic, color, drawings, forms, size, tops,
                    volume_small, volume_big):

    queries.append(' '.join(str(perm)[2:-2].split('\', \'')))

for i in range(10):
    query = queries[i]
    print(query)
    searcher = NewYandexSearcher(query)
    request = searcher.search()[:5]
    print(query)
    print(*request, sep='\n')
    break






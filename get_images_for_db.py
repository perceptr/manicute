import requests as rq
import os
import pathlib
from bing_image_urls import bing_image_urls


def save_image(folder: str, name: str, url: str):
    # Get the data from the url
    image_source = rq.get(url)

    # If there's a suffix, we will grab that
    suffix = pathlib.Path(url).suffix

    # Check if the suffix is one of the following
    if suffix not in ['.jpg', '.jpeg', '.png', '.gif']:
        # Default to .png
        output = name + '.png'
    else:
        output = name + suffix

    # Check first if folder exists, else create a new one
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Create our output in the specified folder (wb = write bytes)
    with open(f'{folder}{output}', 'wb') as file:
        file.write(image_source.content)
        print(f'Successfully downloaded: {output}')


i = 1

if __name__ == '__main__':
    keyword = input('Enter word: ')
    count = int(input('Count: '))
    urls = bing_image_urls(keyword, limit=count)
    for url in urls:
        save_image('manicure_base/white/', f'{keyword}' + str(i), url)
        i += 1

import requests
import time
import concurrent.futures
import os

img_urls = [
    'https://images.pexels.com/photos/67636/rose-blue-flower-rose-blooms-67636.jpeg?cs=srgb&dl=nature-red-love-romantic-67636.jpg&fm=jpg'
]


def download_image(img_url):
    img_bytes = requests.get(img_url).content
    img_name = ''.join(e for e in img_url.split('/')[-1] if e.isalnum())
    img_name = f'{img_name}.jpg'
    with open('downloads/'+img_name, 'wb') as img_file:
        img_file.write(img_bytes)
        print(f'{img_name} was downloaded...')


def main():
    try:
        t1 = time.perf_counter()

        if not os.path.exists('downloads'):
            os.mkdir('downloads')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(download_image, img_urls)
        t2 = time.perf_counter()

        print(f'Finished in {t2-t1} seconds')
    except Exception as e:
        raise e


if __name__ == "__main__":
    main()

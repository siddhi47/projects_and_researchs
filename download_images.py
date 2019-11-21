import requests
import time
import concurrent.futures
import os
import json


def download_image(img_url):
    try:
        img_bytes = requests.get(img_url).content
        img_name = ''.join(e for e in img_url.split('/')[-1] if e.isalnum())
        img_name = f'{img_name}.jpg'
        with open('downloads/'+img_name, 'wb') as img_file:
            img_file.write(img_bytes)
    except Exception as e:
        raise e


def main():
    try:
        t1 = time.perf_counter()
        with open('urls.json') as urls:
            url_list = json.load(urls)
            img_urls = url_list["url"]

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

import time
from datetime import date
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from platform import system


headers = {
    'authority': 'volsu.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'volsu_GUEST_ID=11300294; PHPSESSID=yHnDGDWD2J5Z2yg7iaWtNFIhiR5d05bC; volsu_LAST_VISIT=18.02.2023%2010%3A15%3A34',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

result = []
confer = []
def get_volsu_conf_data(driver, url, page, filter_date):
    start_date = f'{filter_date.day}.{filter_date.month}.{filter_date.year}'
    end_date = f'{date.today().day}.{date.today().month}.{date.today().year + 1}'
    try:
        url_ = url + f'?sort=asc&arrFilter_ff%5BTAGS%5D=&arrFilter_DATE_CREATE_1=' \
                     f'{start_date}&arrFilter_DATE_CREATE_2={end_date}&set_filter=Y&PAGEN_1={page}'
        driver.get(url=url_)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # print(soup)
        main_container = soup.find('div', class_='main__content', id='work_area').find('div', class_='main__grid')
        # print(main_container)
        for conf in main_container.find_all('a'):
            link = f"https://volsu.ru{conf.get('href')}"
            title = normalise_str(conf.find(class_='card__title').get_text(separator=" "))
            if 'конфер' in title.lower():
                # print(title, link)
                confer.append(
                    {
                        'title': title,
                        'link': link,
                     }
                    )
            # print(confer)
    except TimeoutError as e:
        print(f'Отказ по таймауту, {page}, по {url_}', e)
    except Exception as e:
        raise Exception(f'Нарушена структура ответа с {url_} на странице {page}\n{e}')


def make_queue_volsu(driver, un_id, url, filter_date):

    start_date = f'{filter_date.day}.{filter_date.month}.{filter_date.year}'
    end_date = f'{date.today().day}.{date.today().month}.{date.today().year+1}'

    try:
        url_ = url + f'?sort=asc&arrFilter_ff%5BTAGS%5D=&arrFilter_DATE_CREATE_1={start_date}&arrFilter_DATE_CREATE_2={end_date}&set_filter=Y&PAGEN_1=1'
        driver.get(url=url_)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # print(soup)
        main_container = soup.find('div', class_='main__content', id='work_area')
        # print(main_container)
        pages = int(main_container.find('div', id='pagin_list').find_all('li', class_='pagination__item')[-3].text) if \
                                                    main_container.find('div', id='pagin_list') else 1

        for page in range(1, pages+1):
            print(f'Запрос данных со страницы {page}')
            get_volsu_conf_data(driver, url, page, filter_date)
            time.sleep(1)

    except TimeoutError as e:
        print(f'Отказ по таймауту {url_}', e)
    except Exception as e:
        raise Exception(f'Не удалось обработать ссылку в {__name__} для {url_}\n{e}')


def parser_volsu_pages(driver, un_id):
    try:
        for n, conf in enumerate(confer):
            print(f"Обработка конференции {n + 1} из {len(confer)}, {conf['link']}")
            driver.get(url=conf['link'])
            soup = BeautifulSoup(driver.page_source, 'lxml')
            conf_block = soup.find('div', class_='main__content')
            if not conf_block:
                print(f"Блок описания конференции {conf['link']} отсутствует.")
                return

            un_name = 'Волгоградский государственный университет'
            conf_name = conf['title']
            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{conf['link'].split('=')[-1]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            conf_card_href = conf['link']

            lines = conf_block.find('div', class_='news-detail').find_all(['div', 'p', 'ul'])
            # print(lines)

            themes = ''
            conf_s_desc = ''
            conf_date_begin = ''  # conf_block.find('span', class_='news-date-time mark').text
            conf_date_end = ''
            reg_date_begin = ''
            reg_date_end = ''
            reg_href = ''
            conf_desc = ''
            org_name = ''

            online = False
            conf_href = ''
            offline = False
            conf_address = ''
            contacts = ''
            rinc = False

            for line in lines:
                # print(line)
                if conf_s_desc == '':
                    conf_s_desc = normalise_str(line.text)

                if ('состоится' in line.text.lower() or 'открытие' in line.text.lower()
                        or 'проведен' in line.text.lower() or 'пройдет' in line.text.lower()
                        or 'прошла' in line.text.lower()) and conf_date_begin == '':
                        conf_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                            list(find_date_in_string(line.text.lower())) else ''
                        conf_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                            len(list(find_date_in_string(line.text.lower()))) > 1 else ''

                if ('заявк' in line.text.lower() or 'принимаютс' in line.text.lower() or 'регистрац' in line.text.lower() or
                    'регистрир' in line.text.lower()) and reg_date_begin == '':
                    reg_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                        list(find_date_in_string(line.text.lower())) else ''
                    reg_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                        len(list(find_date_in_string(line.text.lower()))) > 1 else ''

                if reg_href == '' and ('регистрац' in line.text.lower() or 'зарегистр' in line.text.lower()
                                   or 'заявк' in line.text.lower()):
                    reg_href = line.find('a').get('href') if line.find('a') \
                                                         and ('http:' in line.find('a').get('href') or
                                                              'https:' in line.find('a').get('href')) and \
                                                         ('.pdf' not in line.find('a').get('href') or
                                                          '.doc' not in line.find('a').get('href') or
                                                          '.xls' not in line.find('a').get('href')) else 'отсутствует'

                conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

                if org_name == '' and 'организатор' in line.text.lower():
                    org_name = normalise_str(line.get_text(separator=" "))

                if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                    online = True
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

                if not offline and ('город' in line.text.lower() or 'адрес' in line.text.lower() or 'место проведен' in line.text.lower()):
                    offline = True
                    conf_address = normalise_str(line.get_text(separator=" "))

                if ('тел.' in line.text.lower() or 'контакт' in line.text.lower() or 'mail' in line.text.lower()
                        or 'почта' in line.text.lower() or 'почты' in line.text.lower()):
                    contacts = contacts + ' ' + normalise_str(line.text)

                if line.find('a') and 'mailto' in line.find('a').get('href'):
                    contacts = contacts + ' ' + normalise_str(line.find('a').text)

                if not rinc:
                    rinc = True if 'ринц' in line.text.lower() else False

            result.append(
                    {'conf_id': conf_id,
                     'hash': hash_,
                     'un_name': un_name,
                     'local': local,
                     'reg_date_begin': reg_date_begin,
                     'reg_date_end': reg_date_end,
                     'conf_date_begin': conf_date_begin,
                     'conf_date_end': conf_date_end,
                     'conf_card_href': conf_card_href,
                     'reg_href': reg_href,
                     'conf_name': conf_name.strip(),
                     'conf_s_desc': conf_s_desc.strip(),
                     'conf_desc': conf_desc.strip(),
                     'org_name': org_name.strip(),
                     'themes': themes.strip(),
                     'online': online,
                     'conf_href': conf_href,
                     'offline': offline,
                     'conf_address': conf_address.strip(),
                     'contacts': contacts.strip(),
                     'rinc': rinc,
                     }
                )

    except asyncio.TimeoutError as e:
        print(f"Отказ по таймауту, {n + 1} из {len(confer)}, {conf['link']}", e)

def get_griver_path():
    path = 'chromedriver/'
    if system() == 'Windows':
        path = f'{path}win/chromedriver.exe'
    if system() == 'Linux':
        path = f'{path}linux/chromedriver'
    if system() == 'Darwin':
        path = f'{path}darwin/chromedriver'
    return path

def parser_volsu(un_id, url, date_):
    try:
        options = webdriver.ChromeOptions()
        service = Service(executable_path=get_griver_path())
        driver = webdriver.Chrome(service=service, options=options)
        # driver.minimize_window()

        make_queue_volsu(driver, un_id, url, date_)
        parser_volsu_pages(driver, un_id)

        driver.close()
        driver.quit()

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_volsu('volsu', 'https://volsu.ru/archive_ad.php', datetime.strptime('2023.01.01', '%Y.%m.%d')))

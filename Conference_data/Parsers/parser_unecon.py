from datetime import date
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime

headers = {
    'authority': 'unecon.ru',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': 'https://unecon.ru/announcements/',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'x-kl-ajax-request': 'Ajax_Request',
}

result = []
confer = []


async def get_unecon_conf_data(session, url, page):
    params = {
        'page': page,
        'category': '212',
    }
    try:
        async with session.get(url, params=params, headers=headers, timeout=20) as response:
            if response.status == 404:
                print(f'{response.status} - Нет такой страницы {url}')
                return
            print(f'{response.status} Запрос данных со страницы {page}.')
            resp = await response.json()
            if resp['list']:
                try:
                    for _ in resp['list']:
                        confer.append(
                            {'category': _['category'],
                             'title': _['title'],
                             'link': _['link'],
                             'date_start': _['date_start'],
                             'date_end': _['date_end']
                             }
                        )
                except Exception as e:
                    raise Exception(f'Нарушена структура ответа API с {url} на странице {page}\n{e}')

                return True
            else:
                return False
    except asyncio.TimeoutError as e:
        print(f'Отказ по таймауту {url}', e)


async def make_queue_unecon(un_id, url, filter_date):
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            page = 1
            while True:
                if await get_unecon_conf_data(session, url, page):
                    page += 1
                else:
                    print(f'Страница {page} отсутствует, данные закончились. Обрабатываем.')
                    break
            try:
                for n, conf in enumerate(confer):
                    print(f'Кладем в очередь конференцию {n + 1} из {len(confer)}')
                    task = asyncio.create_task(parser_unecon_pages(session, un_id, conf, filter_date, n, len(confer)))
                    tasks.append(task)

                await asyncio.gather(*tasks)
            except Exception as e:
                raise Exception(f'Не удалось обработать очередь в {__name__} для {url}\n{e}')
    except Exception as e:
        raise Exception(f'Не удалось открыть сессию для {__name__}\n{e}')


async def parser_unecon_pages(session, un_id, conf, filter_date, n, confs):
    def convert_date(string):
        string = string.split()
        if len(string[1]) == 1:
            string[1] = f"0{string[1]}"
        return '-'.join(string[::-1])

    try:
        async with session.get(url=conf['link'], headers=headers, timeout=20) as response:
            if response.status == 404:
                print(f"{response.status} - Нет такой страницы {conf['link']}")
                return
            print(f"{response.status} Обработка конференции {n + 1} из {confs}, {conf['link']}")
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'lxml')
            conf_block = soup.find('div', class_='col-xl-8 offset-xl-2')
            un_name = soup.find('div', class_='main-header__inner').find('a').get('title').strip()
            conf_name = normalise_str(conf['title'])

            conf_id = f"{un_id}_{conf['link'].split('/')[-2]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            conf_card_href = conf['link']

            lines = conf_block.find('div', class_='post_content').find_all(['p'])

            themes = ''
            for _ in soup.find('ul', class_='page-news_category_list').find_all('li'):
                themes = themes + normalise_str(_.text) + ', '

            conf_date_begin = convert_date(conf['date_start'])
            conf_date_end = convert_date(conf['date_end'])

            conf_s_desc = ''
            reg_date_begin = ''
            reg_date_end = ''
            reg_href = ''
            conf_desc = ''
            org_name = ''
            local = True
            online = False
            conf_href = ''
            offline = False
            conf_address = ''
            contacts = ''
            rinc = False

            for line in lines:

                if conf_s_desc == '':
                    conf_s_desc = normalise_str(line.text)

                if ('заявк' in line.text.lower() or 'принимаютс' in line.text.lower() or 'регистрац' in line.text.lower() or
                    'регистрир' in line.text.lower()) and reg_date_begin == '':
                    reg_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                        list(find_date_in_string(line.text.lower())) else ''
                    reg_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                        len(list(find_date_in_string(line.text.lower()))) > 1 else ''

                if reg_href == '' and ('регистрац' in line.text.lower() or 'зарегистр' in line.text.lower()
                                       or 'участия' in line.text.lower() or 'заявк' in line.text.lower()):
                    reg_href = line.find('a').get('href') if line.find('a') \
                                                             and ('http:' in line.find('a').get('href') or
                                                                  'https:' in line.find('a').get('href')) and \
                                                             ('.pdf' not in line.find('a').get('href') or
                                                              '.doc' not in line.find('a').get('href') or
                                                              '.xls' not in line.find('a').get('href')) else 'отсутствует'

                conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

                if org_name == '' and 'организатор' in line.text.lower():
                    org_name = normalise_str(line.get_text(separator=" "))

                local = False if 'международн' in line.text.lower() else True

                if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                    online = True
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

                if not offline and ('место' in line.text.lower() or 'адрес' in line.text.lower()):
                    offline = True
                    conf_address = normalise_str(line.get_text(separator=" "))

                if ('тел.' in line.text.lower() or 'контакт' in line.text.lower() or 'mail' in line.text.lower()
                        or 'почта' in line.text.lower() or 'почты' in line.text.lower()):
                    contacts = contacts + ' ' + normalise_str(line.text)

                if line.find('a') and 'mailto' in line.find('a').get('href'):
                    contacts = contacts + ' ' + normalise_str(line.find('a').text)

                if not rinc:
                    rinc = True if 'ринц' in line.text.lower() else False

            if (conf_date_begin != '' and datetime.strptime(conf_date_begin,
                                                            '%Y-%m-%d') >= filter_date) or conf_date_begin == '':
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
                     'conf_name': conf_name,
                     'conf_s_desc': conf_s_desc,
                     'conf_desc': conf_desc,
                     'org_name': org_name,
                     'themes': themes.strip(),
                     'online': online,
                     'conf_href': conf_href,
                     'offline': offline,
                     'conf_address': conf_address,
                     'contacts': contacts,
                     'rinc': rinc,
                     }
                )
    except asyncio.TimeoutError as e:
        print(f"Отказ по таймауту, конференция {n + 1} из {confs}, {conf['link']}", e)


def parser_unecon(un_id, url, date_):
    try:
        asyncio.run(make_queue_unecon(un_id, url, date_))
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_unecon('unecon', 'https://unecon.ru/wp-json/unecon/v1/announcements',
                        datetime.strptime('2023.01.01', '%Y.%m.%d')))

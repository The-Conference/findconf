from datetime import date
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime

headers = {
    'authority': 'feeds.tildacdn.com',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://pimunn.ru',
    'referer': 'https://pimunn.ru/',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

result = []
confer = []


async def get_pimunn_conf_data(session, url, page):

    params = {
        'feeduid': '5da0b30957567621136849-830127464577',
        'recid': '134097321',
        'c': '1676878449022',
        'size': '10',  # больше 10 за 1 раз бессмысленно, мало конференций
        'slice': f'{page}',
        'sort[date]': 'desc',
        'filters[date]': '',
        'getparts': 'true',
    }
    try:
        async with session.get(url, params=params, headers=headers, timeout=20) as response:
            if response.status == 404:
                print(f'{response.status} - Нет такой страницы {url}')
                return
            print(f'{response.status} Запрос данных со страницы {page}.')
            resp = await response.json()

            if resp['posts']:
                try:
                    for _ in resp['posts']:
                        confer.append(
                            {'desc': _['descr'],
                             'title': _['title'],
                             'url': _['url'],
                             'date_pub': _['date'].split()[0],
                             }
                        )
                except Exception as e:
                    raise Exception(f'Нарушена структура ответа API с {url} на странице {page}\n{e}')

                return True
            else:
                return False
    except asyncio.TimeoutError as e:
        print(f'Отказ по таймауту {url}', e)


async def make_queue_pimunn(un_id, url, filter_date):
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            page = 1  # дальше первого слайса нет необходимости ходить
            while page < 2:
                if await get_pimunn_conf_data(session, url, page):
                    page += 1
                else:
                    print(f'Страница {page} отсутствует, данные закончились. Обрабатываем.')
                    break
            try:
                for n, conf in enumerate(confer):
                    if datetime.strptime(conf['date_pub'], '%Y-%m-%d') >= filter_date:
                        print(f'Кладем в очередь конференцию {n + 1} из {len(confer)}')
                        task = asyncio.create_task(parser_pimunn_pages(session, un_id, conf, n, len(confer)))
                        tasks.append(task)
                    else:
                        print(f'Конференция {n + 1} старее {str(filter_date.date())}')

                await asyncio.gather(*tasks)
            except Exception as e:
                raise Exception(f'Не удалось обработать очередь в {__name__} для {url}\n{e}')
    except Exception as e:
        raise Exception(f'Не удалось открыть сессию для {__name__}\n{e}')


async def parser_pimunn_pages(session, un_id, conf, n, confs):
    try:
        async with session.get(url=conf['url'], headers=headers, timeout=20) as response:
            if response.status == 404:
                print(f"{response.status} - Нет такой страницы {conf['url']}")
                return
            print(f"{response.status} Обработка конференции {n + 1} из {confs}, {conf['url']}")
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'lxml')
            if soup.find('div', class_='t-redactor__text'):
                conf_block = normalise_str(soup.find('div', class_='t-redactor__text').get_text(separator=' '))
            else:
                print(f'Не найден блок описания конференции {n + 1}')

            un_name = 'Приволжский исследовательский медицинский университет Министерства здравоохранения Российской Федерации'
            conf_name = normalise_str(conf['title'])
            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{conf['url'].split('/')[-1]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            conf_card_href = conf['url']

            themes = ''

            conf_date_begin = ''
            conf_date_end = ''

            conf_desc = conf_block
            conf_s_desc = conf['desc']
            reg_date_begin = ''
            reg_date_end = ''
            reg_href = ''

            org_name = ''

            online = False
            conf_href = ''
            offline = False
            conf_address = ''
            contacts = ''
            rinc = False

            if ('состоится' in conf_block.lower() or 'открытие' in conf_block.lower()
                or 'проведен' in conf_block.lower() or 'пройдет' in conf_block.lower()
                or 'прошла' in conf_block.lower()) and conf_date_begin == '':
                conf_date_begin = str(list(find_date_in_string(conf_block.lower()))[0].date()) if \
                    list(find_date_in_string(conf_block.lower())) else ''
                conf_date_end = str(list(find_date_in_string(conf_block.lower()))[1].date()) if \
                    len(list(find_date_in_string(conf_block.lower()))) > 1 else ''

            if ('заявк' in conf_block.lower() or 'принимаютс' in conf_block.lower() or 'регистрац' in conf_block.lower() or
                'регистрир' in conf_block.lower()) and reg_date_begin == '':
                reg_date_begin = str(list(find_date_in_string(conf_block.lower()))[0].date()) if \
                    list(find_date_in_string(conf_block.lower())) else ''
                reg_date_end = str(list(find_date_in_string(conf_block.lower()))[1].date()) if \
                    len(list(find_date_in_string(conf_block.lower()))) > 1 else ''

            if not online and ('онлайн' in conf_block.lower() or 'трансляц' in conf_block.lower()):
                online = True

            if not offline and ('место' in conf_block.lower() or 'адрес' in conf_block.lower()):
                offline = True

            if not rinc:
                rinc = True if 'ринц' in conf_block.lower() else False

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


def parser_pimunn(un_id, url, date_):
    try:
        asyncio.run(make_queue_pimunn(un_id, url, date_))
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_pimunn('pimunn', 'https://feeds.tildacdn.com/api/getfeed/',
                        datetime.strptime('2023.01.01', '%Y.%m.%d')))

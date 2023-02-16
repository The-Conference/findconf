from datetime import date
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36'
}

result = []
confer = []
async def get_pstu_conf_data(session, url, page, filter_year):
    params = {
        'p': page,
        'tag': '14',
    }
    try:
        async with session.get(url, params=params, headers=headers, timeout=20) as response:
            if response.status == 404:
                print(f'{response.status} - Нет такой страницы {url}')
                return
            resp = await response.text()
            soup = BeautifulSoup(resp, 'lxml')
            main_container = soup.find('div', class_='all_news_contaner').find_all('div', class_='news_item')
            for conf in main_container:
                if conf.find('a'):
                    link = f"https://pstu.ru{conf.find('a').get('href')}"
                    if int(link.split('/')[-5]) < filter_year:
                        continue
                    title = normalise_str(conf.find('a').find('div', class_='title').text)
                    desc = normalise_str(conf.find('a').find('div', class_='small').text)
                    confer.append(
                        {
                            'title': title,
                            'link': link,
                            'desc': desc,
                         }
                        )
            # print(confer)
    except asyncio.TimeoutError as e:
        print(f'Отказ по таймауту, {page}, по {url}', e)
    except Exception as e:
        raise Exception(f'Нарушена структура ответа с {url} на странице {page}\n{e}')


async def make_queue_pstu(un_id, url, filter_date):
    params = {
        'p': '1',
        'tag': '14',
    }
    try:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, headers=headers, timeout=20) as response:
                    if response.status == 404:
                        print(f'{response.status} - Нет такой страницы {url}')
                        return
                    response_text = await response.text()
                    soup = BeautifulSoup(response_text, 'lxml')
                    main_container = soup.find('div', class_='content').find_all('div', class_='news')[-1]
                    pages = int(main_container.find_all('a')[-1].get('href').split('&')[0].split('=')[-1])
                    pages = 31 if pages > 31 else pages  # нет смысла дальше двух страниц заходить
                    tasks = []
                    page = 1
                    while page <= pages:
                        print(f'{response.status} Запрос данных со страницы {page}, по {url}')
                        await get_pstu_conf_data(session, url, page, filter_date.year)
                        page += 30

                    try:
                        for n, conf in enumerate(confer):
                            print(f'Кладем в очередь конференцию {n+1} из {len(confer)}')
                            task = asyncio.create_task(parser_pstu_pages(session, un_id, conf, n, len(confer)))
                            tasks.append(task)
                    except Exception as e:
                        raise Exception(f'Не удалось обработать очередь в {__name__} для {url}\n{e}')

                    await asyncio.gather(*tasks)

            except asyncio.TimeoutError as e:
                print(f'Отказ по таймауту, {page}, по {url}', e)
            except Exception as e:
                raise Exception(f'Не удалось обработать ссылку в {__name__} для {url}\n{e}')

    except Exception as e:
        raise Exception(f'Не удалось открыть сессию для {__name__}\n{e}')

async def parser_pstu_pages(session, un_id, conf, n, confs):
    try:
        async with session.get(url=conf['link'], headers=headers, timeout=20) as response:
            if response.status == 404:
                print(f"{response.status} - Нет такой страницы {conf['link']}")
                return
            print(f"{response.status} Обработка конференции {n + 1} из {confs}, {conf['link']}")
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'lxml')
            conf_block = soup.find('div', class_='news full_news')

            if not conf_block:
                print(f"Блок описания конференции {conf['link']} отсутствует.")
                return

            un_name = 'Пермский Национальный Исследовательский Политехнический Университет'
            conf_name = conf['title']
            conf_s_desc = conf['desc']
            local = False if 'международн' in conf_name.lower() or 'международн' in conf_s_desc.lower() else True

            conf_id = f"{un_id}_{conf['link'].split('/')[-2]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            conf_card_href = conf['link']

            lines = conf_block.find('div', class_='text').find_all(['p', 'ul'])

            themes = ''

            conf_date_begin = ''
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

                if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                    online = True
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

                if not offline and ('город' in line.text.lower() or 'адрес' in line.text.lower()):
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
                     'conf_name': conf_name,
                     'conf_s_desc': conf_s_desc,
                     'conf_desc': conf_desc,
                     'org_name': org_name,
                     'themes': themes.strip(),
                     'online': online,
                     'conf_href': conf_href,
                     'offline': offline,
                     'conf_address': conf_address,
                     'contacts': contacts.strip(),
                     'rinc': rinc,
                     }
                )

    except asyncio.TimeoutError as e:
        print(f"Отказ по таймауту, {n + 1} из {confs}, {conf['link']}", e)


def parser_pstu(un_id, url, date_):
    try:
        asyncio.run(make_queue_pstu(un_id, url, date_))
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_pstu('pstu', 'https://pstu.ru/tag_news/', datetime.strptime('2023.01.01', '%Y.%m.%d')))

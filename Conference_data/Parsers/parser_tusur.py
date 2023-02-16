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
async def get_tusur_conf_data(session, url, page, year):
    params = {
        'page': f'{page}',
        'parts_params[news_list][interval_year]': f'{year}',
    }
    try:
        async with session.get(url, params=params, headers=headers, timeout=20) as response:
            if response.status == 404:
                print(f'{response.status} - Нет такой страницы {url}')
                return

            print(f'{response.status} Запрос данных со страницы {page} за {year} год, по {url}')
            resp = await response.text()
            soup = BeautifulSoup(resp, 'lxml')
            main_container = soup.find('div', class_='col-lg-9 col-md-9 col-sm-8 col-xs-12 left-side')

            if normalise_str(main_container.find('div', class_='events').text[:23]).lower() == 'информация отсутствует':
                return False

            for conf in main_container.find('table').find_all('tr'):
                if conf.find('a'):
                    link = f"https://tusur.ru{conf.find('a').get('href')}"
                    title = normalise_str(conf.find('a').text)
                    if 'конфер' in title:
                        confer.append(
                            {
                                'title': title,
                                'link': link,
                                'year': year,
                             }
                            )
            # print(confer)
            return True
    except asyncio.TimeoutError as e:
        print(f'Отказ по таймауту, страницы {page} за {year} год, по {url}', e)
    except Exception as e:
        raise Exception(f'Нарушена структура ответа с {url} на странице {page}\n{e}')


async def make_queue_tusur(un_id, url, filter_date):
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            try:
                year = filter_date.year
                if year < 2023:
                    raise Exception(f'Для {year} года ответ сервера нарушен, данные не могут быть получены, для {url}\n')
                page = 1
                while year <= date.today().year:
                    while True:
                        if await get_tusur_conf_data(session, url, page, year):
                            page += 1
                        else:
                            print(f'Нет данных на странице {page} за {year} год.')
                            break
                    year += 1

                try:
                    for n, conf in enumerate(confer):
                        print(f'Кладем в очередь конференцию {n + 1} из {len(confer)}')
                        task = asyncio.create_task(parser_tusur_pages(session, un_id, conf, n, len(confer)))
                        tasks.append(task)
                except Exception as e:
                    raise Exception(f'Не удалось обработать очередь в {__name__} для {url}\n{e}')

                await asyncio.gather(*tasks)

            except Exception as e:
                raise Exception(f'Не удалось обработать ссылку в {__name__} для {url}\n{e}')

    except Exception as e:
        raise Exception(f'Не удалось открыть сессию для {__name__}\n{e}')

async def parser_tusur_pages(session, un_id, conf, n, confs):
    try:
        async with session.get(url=conf['link'], headers=headers, timeout=20) as response:
            if response.status == 404:
                print(f"{response.status} - Нет такой страницы {conf['link']}")
                return

            response_text = await response.text()
            print(f"{response.status} Обработка конференции {n + 1} из {confs}, {conf['link']}")
            soup = BeautifulSoup(response_text, 'lxml')
            conf_block = soup.find('div', class_='content index')
    
            if not conf_block:
                print(f"Блок описания конференции {conf['link']} отсутствует.")
                return

            un_name = 'Томский государственный университет систем управления и радиоэлектроники'
            conf_name = conf['title']
            conf_s_desc = normalise_str(
                conf_block.find('div', class_='news-item').find('div', class_='annotation-text').text)

            local = False if 'международн' in conf_name.lower() or 'международн' in conf_s_desc.lower() else True

            conf_id = f"{un_id}_{conf['link'].split('/')[-1]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            conf_card_href = conf['link']

            lines = conf_block.find('div', class_='news-item').find_all(['p', 'li'])

            themes = ''

            conf_date_begin = ''
            conf_date_end = ''

            if ('состоится' in conf_s_desc.lower() or 'открытие' in conf_s_desc.lower()
                or 'проведен' in conf_s_desc.lower() or 'пройдет' in conf_s_desc.lower()
                or 'прошла' in conf_s_desc.lower() or 'пройдёт' in conf_s_desc.lower()):
                conf_date_begin = str(list(find_date_in_string(conf_s_desc.lower()))[0].date()) if \
                    list(find_date_in_string(conf_s_desc.lower())) else ''
                conf_date_end = str(list(find_date_in_string(conf_s_desc.lower()))[1].date()) if \
                    len(list(find_date_in_string(conf_s_desc.lower()))) > 1 else ''

            reg_date_begin = ''
            reg_date_end = ''
            reg_href = ''
            conf_desc = ''
            org_name = ''

            try:
                place = normalise_str(
                    conf_block.find('div', class_='event-header').find('div', class_='location').find('span',
                                                                                        itemprop='address').text)
            except:
                place = ''

            online = True if ('онлайн' in place.lower() or 'смешан' in place.lower()) else False
            if 'город' in place.lower() or 'адрес' in place.lower() or 'смешан' in place.lower():
                offline = True
                conf_address = place
            else:
                offline = False
                conf_address = ''


            conf_href = ''
            contacts = ''
            rinc = False

            for line in lines:
                # print(line)

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
        print(f"Отказ по таймауту, конференция {n + 1} из {confs}, {conf['link']}", e)


def parser_tusur(un_id, url, date_):
    try:
        asyncio.run(make_queue_tusur(un_id, url, date_))
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_tusur('tusur', 'https://tusur.ru/ru/novosti-i-meropriyatiya/anonsy-meropriyatiy',
                       datetime.strptime('2023.01.01', '%Y.%m.%d')))

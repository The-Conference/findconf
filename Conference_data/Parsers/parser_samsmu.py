from datetime import date
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime


result = []

cookies = {
    'psy': 'x.yz',
    'mtc_id': '60377',
    'mtc_sid': '4xjaspryvv17l6lw75fg3hz',
    'mautic_device_id': '4xjaspryvv17l6lw75fg3hz',
    'PHPSESSID': '6tdthu4aoht9dppfinmjtoaih4',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    # 'Cookie': 'psy=x.yz; mtc_id=60377; mtc_sid=4xjaspryvv17l6lw75fg3hz; mautic_device_id=4xjaspryvv17l6lw75fg3hz; PHPSESSID=6tdthu4aoht9dppfinmjtoaih4',
    'Referer': 'https://samsmu.ru/events/2023/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

async def make_queue_samsmu(un_id, url, filter_date):
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            try:
                year = filter_date.year - 1
                while True:
                    year += 1
                    if year > date.today().year:
                        break
                    url_ = f'{url}/{year}/'
                    try:
                        async with session.get(url=url_, cookies=cookies, headers=headers, timeout=20) as response:
                            if response.status == 404:
                                print(f'{response.status} - Нет такой страницы {url_}')
                                return
                            response_text = await response.text()
                            soup = BeautifulSoup(response_text, 'lxml')
                            main_container = soup.find('section', class_='pb-40 text_section').find('div', class_='row')

                            if not main_container.find('div', class_='feature_46 row justify-content-start w-full pt-25 pb-20 px-0'):
                                print(f'Конференции за {year} год отсутствуют.')
                                continue

                            print(f'{response.status} Обрабатываем страницу {year} года, {url_}')
                            # print(main_container)
                            conf_block = main_container.find(
                                'div', class_='feature_46 row justify-content-start w-full pt-25 pb-20 px-0').find_all(
                                'div', class_='col-lg-4 col-md-6 col-sm-12 mb-30')

                            for n, conf in enumerate(conf_block):
                                title = normalise_str(conf.find('div', class_='f-16 bold').text)
                                # print(title)
                                if 'конфер' in title:
                                    conf_url = f"https://www.samsmu.ru{conf.find('a').get('href').strip()}"
                                    # print(title, conf_url)
                                    task = asyncio.create_task(parser_samsmu_pages(session, un_id, conf_url, filter_date, n, year))
                                    tasks.append(task)
                                    # break

                    except asyncio.TimeoutError as e:
                        print(f'Отказ по таймауту, страница {year} года, {url_}', e)
                    except Exception as e:
                        raise Exception(f'Не удалось обработать ссылку {n} года {year} в {__name__} для {url_}\n{e}')

                await asyncio.gather(*tasks)

            except Exception as e:
                raise Exception(f'Не удалось получить данные в {__name__} для {url}\n{e}')
    except Exception as e:
        raise Exception(f'Не удалось обработать очередь для {__name__}\n{e}')


async def parser_samsmu_pages(session, un_id, url, filter_date, n, year):
    try:
        async with session.get(url=url, cookies=cookies, headers=headers, timeout=20) as response:
            if response.status == 404:
                print(f'{response.status} - Нет такой страницы {url}')
                return
            response_text = await response.text()

            print(f'Выполняется ссылка {n + 1} года {year}, {url}')
            soup = BeautifulSoup(response_text, 'lxml')
            try:
                conf_block = soup.find('section', class_='pb-40 text_section').find('div', class_='row')
            except:
                print(f'Не найден нужный блок в html, не обработана ссылка {url}')
                return

            un_name = 'СамГМУ'

            conf_name = normalise_str(conf_block.find('h1', class_='gradient-heading').text)
            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{url.split('/')[-2]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            conf_card_href = url

            lines = conf_block.find_all('div', class_='col-xl-12 col-lg-12')[-1]
            tag = lines.p
            tag.clear()
            lines = conf_block.find_all('div', class_='col-xl-12 col-lg-12')[-1].find_all(['p'])

            conf_s_desc = ''
            reg_date_begin = ''
            reg_date_end = ''
            conf_date_begin = ''
            conf_date_end = ''
            reg_href = ''
            conf_desc = ''
            org_name = ''
            themes = ''
            online = False
            conf_href = ''
            offline = False
            conf_address = ''
            contacts = ''
            rinc = False

            for line in lines:
                # print(line.text)
                if conf_s_desc == '':
                    conf_s_desc = normalise_str(line.text)

                if ('заявк' in line.text.lower() or 'принимаютс' in line.text.lower() or 'участи' in line.text.lower()
                            or 'регистрац' in line.text.lower() or 'регистрир' in line.text.lower()) and reg_date_begin == '':
                    reg_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                        list(find_date_in_string(line.text.lower())) else ''
                    reg_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                        len(list(find_date_in_string(line.text.lower()))) > 1 else ''

                if ('состоится' in line.text.lower() or 'открытие' in line.text.lower()
                    or 'проведен' in line.text.lower()) and conf_date_begin == '':
                    conf_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                        list(find_date_in_string(line.text.lower())) else ''
                    conf_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                        len(list(find_date_in_string(line.text.lower()))) > 1 else ''

                if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                    online = True
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'
                if not offline and ('место' in line.text.lower() or 'адрес' in line.text.lower()):
                    offline = True
                    conf_address = normalise_str(line.get_text(separator=" "))

                conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

                if reg_href == '' and ('регистрац' in line.text.lower() or 'зарегистр' in line.text.lower()
                                       or 'участия' in line.text.lower() or 'заявк' in line.text.lower()):
                    reg_href = line.find('a').get('href') if line.find('a') \
                                                             and ('http:' in line.find('a').get('href') or
                                                                  'https:' in line.find('a').get('href')) and\
                                                             ('.pdf' not in line.find('a').get('href') or
                                                              '.doc' not in line.find('a').get('href') or
                                                              '.xls' not in line.find('a').get('href')) else 'отсутствует'

                if org_name == '' and 'организатор' in line.text.lower():
                    org_name = normalise_str(line.get_text(separator=" "))

                if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower() or
                                   'ссылка' in line.text.lower()):
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'
                    online = True

                if not offline and ('место' in line.text.lower() or 'адрес' in line.text.lower() or
                                    'очно' in line.text.lower()):
                    conf_address = normalise_str(line.text)
                    offline = True

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
                         'themes': themes,
                         'online': online,
                         'conf_href': conf_href,
                         'offline': offline,
                         'conf_address': conf_address,
                         'contacts': contacts.strip(),
                         'rinc': rinc,
                         }
                    )

    except asyncio.TimeoutError as e:
        print(f'Отказ по таймауту, ссылка {n + 1} года {year}, {url}', e)


def parser_samsmu(un_id, urls, date_):
    try:
        for url in urls:
            asyncio.run(make_queue_samsmu(un_id, url, date_))
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_samsmu('samsmu', ['https://samsmu.ru/events'], datetime.strptime('2023.01.01', '%Y.%m.%d')))

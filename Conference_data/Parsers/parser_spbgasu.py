from datetime import date
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime


result = []

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'PHPSESSID=hpc0qinbi1gqhi47lchsjavl95; anniversary-edge=dismiss; PHPSESSID=hpc0qinbi1gqhi47lchsjavl95; cookieconsent_status=dismiss',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

async def make_queue_spbgasu(un_id, url, filter_date):
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            try:
                year = filter_date.year - 1
                while True:
                    year += 1
                    if year > date.today().year:
                        break
                    url_ = f'{url}Arhiv_{year}/' if year < date.today().year else url
                    try:
                        async with session.get(url=url_, headers=headers) as response:
                            if response.status == 404:
                                print(f'{response.status} - Нет такой страницы {url}')
                                return
                            response_text = await response.text()
                            soup = BeautifulSoup(response_text, 'lxml')
                            # print(soup)
                            main_container = soup.find('table')

                            print(f'{response.status} Обрабатываем {year} год, {url_}')
                            # # print(main_container)
                            conf_block = main_container.find_all('tr')

                            for n, conf in enumerate(conf_block):
                                fields = conf.find_all('td')
                                for field in fields:
                                    if field.find('a') and 'mailto:' not in field.find('a').get('href'):
                                        conf_line = []
                                        title = normalise_str(field.find('a').text)
                                        if 'конфер' in title:
                                            conf_line.append(
                                                {
                                                    'dates': normalise_str(field.find_previous_sibling().text),
                                                    'title': title,
                                                    'status': normalise_str(field.find_next_sibling().text),
                                                    'base': normalise_str(field.find_next_sibling().find_next_sibling().
                                                                          find_next_sibling().text),
                                                    'contacts': normalise_str(field.find_next_sibling().find_next_sibling().
                                                                          find_next_sibling().find_next_sibling().text),
                                                }
                                            )
                                            conf_url = f"https://www.spbgasu.ru{conf.find('a').get('href').strip()}" if \
                                                'http' not in conf.find('a').get('href') else f"{conf.find('a').get('href').strip()}"

                                            task = asyncio.create_task(parser_spbgasu_pages(session, un_id,
                                                                                conf_url, url, conf_line, filter_date, n, year))
                                            tasks.append(task)
                                        #     # break

                    except asyncio.TimeoutError as e:
                        print(f'Отказ по таймауту, {year} год, {url_}', e)

                    except Exception as e:
                        raise Exception(f'Не удалось обработать ссылку {n} года {year} в {__name__} для {url_}\n{e}')

                    await asyncio.gather(*tasks)

            except Exception as e:
                raise Exception(f'Не удалось получить данные в {__name__} для {url}\n{e}')
    except Exception as e:
        raise Exception(f'Не удалось обработать очередь для {__name__}\n{e}')


async def parser_spbgasu_pages(session, un_id, url, source_url, conf_line, filter_date, n, year):
    try:
        un_name = 'СПбГАСУ'
        conf_name = conf_line[0]['title']
        local = False if 'международн' in conf_line[0]['status'].lower() else True

        conf_date_begin = str(list(find_date_in_string(conf_line[0]['dates']))[0].date()) if \
            list(find_date_in_string(conf_line[0]['dates'])) else ''
        conf_date_end = str(list(find_date_in_string(conf_line[0]['dates']))[1].date()) if \
            len(list(find_date_in_string(conf_line[0]['dates']))) > 1 else ''

        contacts = conf_line[0]['contacts']
        rinc = True if conf_line[0] and 'ринц' in conf_line[0]['base'].lower() else False

        conf_id = f"{un_id}_{url.split('/')[-2]}" if source_url in url else f"{un_id}_{url}"
        hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
        conf_card_href = url

        conf_s_desc = ''
        reg_date_begin = ''
        reg_date_end = ''
        reg_href = ''
        conf_desc = ''
        org_name = ''
        themes = ''
        online = False
        conf_href = ''
        offline = False
        conf_address = ''
        themes = ''

        if source_url in url:
            async with session.get(url=url, headers=headers) as response:
                if response.status == 404:
                    print(f'{response.status} - Нет такой страницы {url}')
                    return
                response_text = await response.text()

                print(f'{response.status} Выполняется ссылка {n + 1} года {year}, {url}')
                soup = BeautifulSoup(response_text, 'lxml')
                try:
                    conf_block = soup.find('div', class_='maintext')
                except:
                    print(f'Не найден нужный блок в html, не обработана ссылка {url}')
                    return

                lines = conf_block.find_all(['p', 'ul', 'h2', 'section'])

                for line in lines:
                    # print(line.text)

                    if conf_s_desc == '' and ('цель меропр' in line.text.lower() or 'цели меропр' in line.text.lower()):
                        conf_s_desc = normalise_str(line.text)

                    conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

                    if ('заявк' in line.text.lower() or 'принимаютс' in line.text.lower() or 'участи' in line.text.lower()
                                or 'регистрац' in line.text.lower() or 'регистрир' in line.text.lower()) and reg_date_begin == '':
                        reg_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                            list(find_date_in_string(line.text.lower())) else ''
                        reg_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                            len(list(find_date_in_string(line.text.lower()))) > 1 else ''

                    if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower() or
                                       'на платформе' in line.text.lower() or 'дистанционном' in line.text.lower()):
                        online = True
                        conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

                    if not offline and ('место' in line.text.lower() or 'адрес' in line.text.lower()):
                        offline = True
                        conf_address = normalise_str(line.get_text(separator=" "))

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


def parser_spbgasu(un_id, urls, date_):
    try:
        for url in urls:
            asyncio.run(make_queue_spbgasu(un_id, url, date_))
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_spbgasu('spbgasu',
                         ['https://www.spbgasu.ru/Nauchnaya_i_innovacionnaya_deyatelnost/Konferencii_i_seminary/'],
                         datetime.strptime('2023.01.01', '%Y.%m.%d')))

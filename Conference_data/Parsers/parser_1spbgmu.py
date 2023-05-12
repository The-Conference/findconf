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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36'
}


async def make_queue_1spbgmu(un_id, url, filter_date):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            tasks = []
            try:
                async with session.get(url=url, headers=headers, timeout=20) as response:
                    response_text = await response.text()
                    soup = BeautifulSoup(response_text, 'lxml')
                    pages = int(soup.find('div', class_='pagination').find('p', class_='counter pull-right').
                                text.split(' ')[-1])

                    # for page in range(1, pages+1):
                    for page in range(1, 2):  # чтобы не парсить вообще все, там старье.
                        url_ = f'{url}?start={(page - 1) * 30}' if page > 1 else url
                        try:
                            async with session.get(url=url_, headers=headers) as response:
                                response_text = await response.text()

                                print(f'{response.status} Обрабатываем страницу {page} из {pages}, {url_}')
                                soup = BeautifulSoup(response_text, 'lxml')
                                conf_block = soup.find('div', class_='content-category').find('tbody').find_all('tr')
                                for n, conf in enumerate(conf_block):
                                    title = conf.find('a').text.lower().strip()
                                    if 'конфер' in title:
                                        conf_url = f"{url}{conf.find('a').get('href')}"
                                        task = asyncio.create_task(
                                            parser_1spbgmu_pages(session, un_id, conf_url, filter_date, n, page)
                                        )
                                        tasks.append(task)
                                    # break
                        except Exception as e:
                            raise Exception(
                                f'Не удалось обработать ссылку {n} на странице {page} в {__name__} для {url_}\n{e}')

                        await asyncio.gather(*tasks)
            except Exception as e:
                raise Exception(f'Не удалось получить данные в {__name__} для {url}\n{e}')
    except Exception as e:
        raise Exception(f'Не удалось обработать очередь для {__name__}\n{e}')


async def parser_1spbgmu_pages(session, un_id, url, filter_date, n, page):
    try:
        async with session.get(url=url, headers=headers, timeout=20) as response:
            if response.status == 404:
                print(f'{response.status} - Нет такой страницы {url}')
                return
            print(f'{response.status} Выполняется ссылка {n + 1} на странице {page}, {url}')
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'lxml')
            conf_block = soup.find('div', class_='item-page')
            conf_name = normalise_str(conf_block.find('div', class_='page-header').get_text(separator=" "))
            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{url.split('/')[-1]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            un_name = normalise_str(
                soup.find('div', id='header').find_all('div', class_='custom')[-1].get_text(separator=" "))
            conf_card_href = url
            reg_date_begin = ''
            reg_date_end = ''
            conf_date_begin = ''
            conf_date_end = ''
            lines = conf_block.find('div', itemprop='articleBody').find_all('p')
            prev_text = ''
            conf_s_desc = ''
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
            scopus = False
            vak = False
            wos = False

            for line in lines:
                # print(line.text)
                if conf_s_desc == '' and 'коллеги' in prev_text.lower():
                    conf_s_desc = normalise_str(line.get_text(separator=" "))
                if reg_href == '' and 'регистрац' in line.text.lower():
                    reg_href = line.find('a').get('href') if line.find('a') else 'отсутствует'
                conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))
                if org_name == '' and 'организатор' in line.text.lower():
                    org_name = normalise_str(line.get_text(separator=" "))
                if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                    online = True
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'
                if not offline and ('место' in line.text.lower() or 'адрес' in line.text.lower()):
                    offline = True
                    conf_address = normalise_str(line.get_text(separator=" "))
                if ('телеф' in line.text.lower() or 'контакт' in line.text.lower() or 'mail' in line.text.lower()
                        or 'почта' in line.text.lower() or 'почты' in line.text.lower()):
                    contacts = contacts + ' ' + normalise_str(line.get_text(separator=" "))
                if line.find('a'):
                    for a in line.find_all('a'):
                        if 'mailto' in a.get('href'):
                            contacts = contacts + ' ' + normalise_str(a.text)
                if ('состоится' in line.text.lower() or 'открытие' in line.text.lower()
                    or 'проведен' in line.text.lower()) and conf_date_begin == '':
                    conf_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                        list(find_date_in_string(line.text.lower())) else ''
                    conf_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                        len(list(find_date_in_string(line.text.lower()))) > 1 else ''
                if ('заявки' in line.text.lower() or 'принимаютс' in line.text.lower()
                    or 'участие' in line.text.lower()) and reg_date_begin == '':
                    reg_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                        list(find_date_in_string(line.text.lower())) else ''
                    reg_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                        len(list(find_date_in_string(line.text.lower()))) > 1 else ''

                if not rinc:
                    rinc = True if 'ринц' in line.text.lower() else False
                if not scopus:
                    scopus = True if 'scopus' in line.text.lower() else False
                if not vak:
                    vak = True if 'ВАК' in line.text else False
                if not wos:
                    wos = True if 'wos' in line.text.lower() else False

                prev_text = line.text


            if (conf_date_begin != '' and datetime.strptime(conf_date_begin,
                                                            '%Y-%m-%d') >= filter_date) or conf_date_begin == '':
                # print(conf_date_begin)
                # print('---------->', datetime.strptime(conf_date_begin, '%Y-%m-%d'))
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
                     'scopus': scopus,
                     'vak': vak,
                     'wos': wos
                     }
                )
    except asyncio.TimeoutError as e:
        print(f'Отказ по таймауту, ссылка {n + 1} на странице {page}, {url}', e)


def parser_1spbgmu(un_id, url, date_):
    try:
        asyncio.run(make_queue_1spbgmu(un_id, url, date_))
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_1spbgmu('1spbgmu', 'https://www.1spbgmu.ru/nauka/konferentsii',
                         datetime.strptime('2023.01.01', '%Y.%m.%d')))

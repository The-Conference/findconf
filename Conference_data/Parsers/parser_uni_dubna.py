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
    # 'Cookie': 'qtrans_front_language=ru; _ga=GA1.2.1607995547.1675767069; _gid=GA1.2.1267382621.1675767069; showPopup=true',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}


async def make_queue_uni_dubna(un_id, url, filter_date):
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            try:
                async with session.get(url=url, headers=headers, timeout=20) as response:
                    if response.status == 404:
                        print(f'{response.status} - Нет такой страницы {url}')
                        return
                    response_text = await response.text()
                    soup = BeautifulSoup(response_text, 'lxml')
                    main_container = soup.find('div', class_='main main-raised')
                    confs = main_container.find_all('div', class_='section')

                    for conf_ in confs:
                        if conf_.find('div', class_='container').find('h1').text == 'Ближайшие конференции':
                            conf_block = conf_.find('div', class_='container').find_all('div', class_='col-lg-12 col-md-9')
                            for n, conf in enumerate(conf_block):
                                block = conf.find('div', class_='card-body')
                                # print(block)
                                title = normalise_str(block.find(class_='card-title cardSize').text)
                                if 'конфер' in title.lower():
                                    data = {
                                        'title': title,
                                        'url': f"https://conf.uni-dubna.ru{block.find('a').get('href').strip()}",
                                        'dates': normalise_str(block.find('a').find('h5').text),
                                        'desc': normalise_str(block.find('p', class_='card-description').text),
                                    }
                                    # print(data)
                                    task = asyncio.create_task(
                                        parser_uni_dubna_pages(session, un_id, data, filter_date, n))
                                    tasks.append(task)
                    # # break

            except asyncio.TimeoutError as e:
                print(f'Отказ по таймауту при подготовке очереди {url}', e)
            except Exception as e:
                raise Exception(f'Не удалось обработать ссылку {n} в {__name__} для {url}\n{e}')

            await asyncio.gather(*tasks)

    except Exception as e:
        raise Exception(f'Не удалось обработать очередь для {__name__}\n{e}')


async def parser_uni_dubna_pages(session, un_id, data, filter_date, n):
    try:
        async with session.get(url=data['url'], headers=headers, timeout=20) as response:
            if response.status == 404:
                print(f"{response.status} - Нет такой страницы {data['url']}")
                return

            response_text = await response.text()

            print(f"{response.status} Выполняется ссылка {n + 1}, {data['url']}")
            soup = BeautifulSoup(response_text, 'lxml')
            try:
                header_block = soup.find('div', class_='page-header header-filter header-small').find('div', class_='col-md-12 ml-auto mr-auto text-center')
                conf_block = soup.find('div', class_='main main-raised').find('div', class_='container')
            except:
                print(f"Не найден нужный блок в html, не обработана ссылка {data['url']}")
                return

            conf_id = f"{un_id}_{data['url'].split('=')[-1]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())

            un_name = 'Государственный университет "Дубна"'
            conf_name = data['title']
            local = False if 'международн' in conf_name.lower() else True

            conf_s_desc = data['desc']
            conf_card_href = data['url']

            conf_date_begin = str(list(find_date_in_string(data['dates']))[0].date()) if \
                list(find_date_in_string(data['dates'])) else ''
            conf_date_end = str(list(find_date_in_string(data['dates']))[1].date()) if \
                len(list(find_date_in_string(data['dates']))) > 1 else ''

            reg_href = ''

            reg_date_begin = ''
            reg_date_end = ''
            conf_desc = ''

            themes = ''
            online = False
            conf_href = ''
            offline = False
            org_name = ''
            conf_address = normalise_str(header_block.find('h4', class_='hero-text-small').text)
            themes = ''
            contacts = ''
            rinc = False

            try:
                lines = conf_block.find_all(['h2', 'h3', 'h5', 'p'])
            except:
                lines = []

            for line in lines:
                # print(line.text)

                conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

                if ('заявк' in line.text.lower() or 'принимаютс' in line.text.lower() or 'участи' in line.text.lower()
                    or 'регистрац' in line.text.lower() or 'регистрир' in line.text.lower()) and reg_date_begin == '':
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

                if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower() or
                                   'на платформе' in line.text.lower() or 'дистанционном' in line.text.lower()):
                    online = True
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

                if not offline and ('место' in line.text.lower() or 'места' in line.text.lower() or
                                    'ждем вас в' in line.text.lower() or 'адрес' in line.text.lower()):
                    offline = True

                if org_name == '' and 'организатор' in line.text.lower():
                    org_name = normalise_str(line.get_text(separator=" "))

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
        print(f"Отказ по таймауту, ссылка {n + 1}, {data['url']}", e)


def parser_uni_dubna(un_id, urls, date_):
    try:
        for url in urls:
            asyncio.run(make_queue_uni_dubna(un_id, url, date_))
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_uni_dubna('uni_dubna', ['https://conf.uni-dubna.ru/Home/Conferences'],
                               datetime.strptime('2023.01.01', '%Y.%m.%d')))

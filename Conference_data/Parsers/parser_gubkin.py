import time
from datetime import date
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime
import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36'
}

result = []
confer = []

def make_queue_gubkin(session, url, filter_date):

    start_date = f'{filter_date.day}.{filter_date.month}.{filter_date.year}'
    end_date = f'{date.today().day}.{date.today().month}.{date.today().year+1}'
    params = {
        's_dateFrom': f'{start_date}',
        's_dateTo': f'{end_date}',
        's_org': '',
        's_place': '',
        's_text': '',
    }

    try:
        resp = session.get(url=url, params=params, headers=headers, timeout=20)
        if resp.status_code == 404:
            print(f'{resp.status_code} - Нет такой страницы {url}')
            return
        soup = BeautifulSoup(resp.text, 'lxml')
        # print(soup)
        main_container = soup.find('table', class_='table schedule').find_all('tr')
        # print(main_container)
        for conf in main_container:
            if conf.find('td', class_='name'):
                title = normalise_str(conf.find('td', class_='name').find('a').get_text(separator=" "))
                if 'конфер' in title.lower():
                    confer.append(
                        {
                            'title': title,
                            'link': f"{url}short/{conf.find('td', class_='name').find('a').get('href')}",
                            'place': normalise_str(conf.find('td', class_='place').get_text(separator=" ")),
                            'dates': normalise_str(conf.find('td', class_='date1').get_text(separator=" ")),
                        }
                    )
        # print(confer)

    except TimeoutError as e:
        print(f'Отказ по таймауту {url}', e)
    except Exception as e:
        raise Exception(f'Не удалось обработать ссылку в {__name__} для {url}\n{e}')


def parser_gubkin_pages(session, un_id):

    def date_str_prep(str):
        names = [' january ', ' february ', ' march ', ' april ', ' may ', ' june ',
                 ' july ', ' august ', ' september ', ' october ', ' november ', ' december ']
        nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        months = dict(zip(nums, names))
        for k, v in months.items():
            if f'.{k}.' in str:
                str = str.replace(f'.{k}.', f'{v}')
        if '-' in str:
            str = str.replace('-', ' - ')
        return str


    try:
        for n, conf in enumerate(confer):
            print(f"Обработка конференции {n + 1} из {len(confer)}, {conf['link']}")
            resp = session.get(url=conf['link'], headers=headers, timeout=20)
            if resp.status_code == 404:
                print(f"{resp.status_code} - Нет такой страницы {conf['link']}")
                return
            soup = BeautifulSoup(resp.text, 'lxml')
            # print(soup)
            conf_block = soup.find('div', class_='modal-body')
            header_block = soup.find('div', class_='modal-body').find('ul', class_='add-info')
            if not conf_block:
                print(f"Блок описания конференции {conf['link']} отсутствует.")
                return

            un_name = 'Российский государственный университет нефти и газа (национальный исследовательский университет) имени И.М. Губкина'
            conf_name = conf['title']
            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{conf['link'].split('/')[-1]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            conf_card_href = conf['link']
            conf_s_desc = conf_name

            dates = find_date_in_string(date_str_prep(conf['dates']))
            conf_date_begin = str(dates[0].date()) if len(dates) > 0 else ''
            conf_date_end = str(dates[1].date()) if len(dates) > 1 else ''
            # print(conf['dates'], date_str_prep(conf['dates']), dates)
            # print(conf_date_begin, conf_date_end)

            reg_date_begin = ''
            reg_date_end = ''
            for li in header_block.find_all('li', class_='date-short'):
                reg_date_end = str(find_date_in_string(date_str_prep(li.text))[0].date()) if reg_date_end == '' and\
                                    'Прием заявок' in li.text and len(li.text) > 15 else ''
            # print(reg_date_begin, reg_date_end)

            org_name = normalise_str(header_block.find('li', class_='host-short').get_text(separator=' '))
            conf_address = normalise_str(header_block.find('li', class_='geo-short').get_text(separator=' '))

            tag = conf_block.ul
            tag.clear()

            themes = ''
            reg_href = ''
            conf_desc = normalise_str(conf_block.get_text(separator=' '))
            online = False
            conf_href = ''
            offline = True

            contacts = ''
            rinc = True if 'ринц' in conf_desc.lower() else False

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
            # break
    except asyncio.TimeoutError as e:
        print(f"Отказ по таймауту, {n + 1} из {len(confer)}, {conf['link']}", e)

def parser_gubkin(un_id, url, date_):
    try:
        session = requests.session()

        make_queue_gubkin(session, url, date_)
        parser_gubkin_pages(session, un_id)

        session.close()

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_gubkin('gubkin', 'https://conf.gubkin.ru/conferences/', datetime.strptime('2023.01.01', '%Y.%m.%d')))

import time
from datetime import date
from bs4 import BeautifulSoup
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

def parser_rzgmu_pages(un_id, url, date_):
    year = date_.year
    month = date_.month - 1
    try:
        session = requests.session()
        while year <= date.today().year + 1:
            while True:
                if month == 12:
                    month = 0
                    break
                else:
                    month += 1
                url_ = f'{url}{year}/{month}/'
                try:
                    time.sleep(0.5)
                    resp = session.get(url=url_, headers=headers, timeout=20)
                    if resp.status_code == 404:
                        print(f'{resp.status_code} - Нет такой страницы {url}')
                        return

                    soup = BeautifulSoup(resp.text, 'lxml')
                    if soup.find('div', class_='events_list').find('article'):
                        print(f'{resp.status_code} - Обработка {month} месяц {year} года')
                        main_containers = soup.find('div', class_='events_list').find_all('article')
                    else:
                        print(f'Нет событий в {month} месяце {year} года.')
                        continue

                    un_name = 'Рязанский государственный медицинский университет имени академика И.П. Павлова'
                    for conf in main_containers:
                        # print(conf)
                        conf_name = normalise_str(conf.find('a', class_='title').find('span', class_='title').text)
                        if 'конфер' in conf_name:
                            get_rzgmu_page_data(session, un_id,
                                                f"https://rzgmu.ru{conf.find('a', class_='title').get('href')}", date_)
                except Exception as e:
                    print(f'Ошибка загрузки данных для {month} месяца {year} года.')

            year += 1

    except Exception as e:
        raise Exception(f'Не удалось открыть сессию для {__name__}\n{e}')

def get_rzgmu_page_data(session, un_id, url, date_):
    try:
        resp = session.get(url=url, headers=headers, timeout=20)
        if resp.status_code == 404:
            print(f'{resp.status_code} - Нет такой страницы {url}')
            return
        print(f'{resp.status_code} - Обработка конференции {url}')
        soup = BeautifulSoup(resp.text, 'lxml')
        main_containers = soup.find('main', id='internal')

        un_name = 'Северо-Западный государственный медицинский университет имени И.И. Мечникова'
        conf_name = normalise_str(main_containers.find('h1').text)

        conf_s_desc = conf_name
        local = False if 'международн' in conf_name.lower() or 'международн' in conf_s_desc.lower() else True
        conf_id = f"{un_id}_{url.split('/')[-2]}"
        hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
        conf_card_href = url

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

        lines = main_containers.find('div', class_='text').find_all(['p', 'ul'])

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

            if not offline and ('город' in line.text.lower() or 'адрес' in line.text.lower()
                                or 'место' in line.text.lower()):
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
             'conf_s_desc': conf_s_desc.strip(),
             'conf_desc': conf_desc.strip(),
             'org_name': org_name,
             'themes': themes.strip(),
             'online': online,
             'conf_href': conf_href,
             'offline': offline,
             'conf_address': conf_address.strip(),
             'contacts': contacts.strip(),
             'rinc': rinc,
             }
        )
    except Exception as e:
        print(f'Ошибка загрузки данных для {url}.\n{e}')


def parser_rzgmu(un_id, url, date_):
    try:
        parser_rzgmu_pages(un_id, url, date_)
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_rzgmu('rzgmu', 'https://rzgmu.ru/actions/',
                       datetime.strptime('2023.01.01', '%Y.%m.%d')))

import time
from datetime import date
from bs4 import BeautifulSoup
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime
import requests
from urllib3 import exceptions


cookies = {
    '_ga': 'GA1.2.1401653974.1676468815',
    'BITRIX_SM_GUEST_ID': '51181620',
    '_gid': 'GA1.2.135708177.1676616166',
    'BITRIX_SM_LAST_VISIT': '17.02.2023+09%3A48%3A07',
    'PHPSESSID': 'DErlXtBhKBZSXt1OxuH8hb4b0SxD0GR7',
    '_gat_UA-52001436-2': '1',
}

headers = {
    'authority': 'donstu.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': '_ga=GA1.2.1401653974.1676468815; BITRIX_SM_GUEST_ID=51181620; _gid=GA1.2.135708177.1676616166; BITRIX_SM_LAST_VISIT=17.02.2023+09%3A48%3A07; PHPSESSID=DErlXtBhKBZSXt1OxuH8hb4b0SxD0GR7; _gat_UA-52001436-2=1',
    'referer': 'https://donstu.ru/events/afishi/vserossiyskaya-nauchno-prakticheskaya-konferentsiya-aktualnye-problemy-nauki-i-tekhniki-2022/',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

result = []
confer = []

def parser_donstu_pages(un_id, url, date_):
    try:
        session = requests.session()
        try:
            count = 1
            while count <= 5:
                try:
                    resp = session.get(url=url, headers=headers, cookies=cookies, timeout=20)
                    break
                except:
                    print(f'Попытка {count} получить данные со страницы {url}')
                    count += 1
                    time.sleep(2)
                    if count > 3:
                        raise Exception('Не удалось загрузить данные с основной страницы')

            if resp.status_code == 404:
                print(f'{resp.status_code} - Нет такой страницы {url}')
                return

            soup = BeautifulSoup(resp.text, 'lxml')
            if soup.find('div', class_='event-box main-event-list'):
                main_containers = soup.find('div', class_='event-box main-event-list')
                # print(main_containers)
                conf_name = normalise_str(main_containers.find('div', class_='title').text)
                if 'конфер' in conf_name:
                    confer.append(
                        [
                            {
                                'title': conf_name,
                                'desc': normalise_str(main_containers.find('div', class_='desc').text),
                                'place': normalise_str(main_containers.find('div', class_='mark').text),
                                'date': normalise_str(main_containers.find('div', class_='date').text),
                                'url': f"https://donstu.ru{main_containers.find('a').get('href')}"
                            }
                        ]
                    )

            if soup.find('div', class_='event-block-content'):
                main_containers = soup.find('div', class_='event-block-content')
                if main_containers.find('div', class_='event-box big-event-list'):
                    conf = main_containers.find('div', class_='event-box big-event-list')
                    # print(conf)
                    conf_name = normalise_str(conf.find('div', class_='title').text)
                    if 'конфер' in conf_name:
                        confer.append(
                            [
                                {
                                    'title': conf_name,
                                    'desc': normalise_str(conf.find('div', class_='desc').text),
                                    'place': normalise_str(conf.find('div', class_='mark').text),
                                    'date': normalise_str(conf.find('div', class_='date').text),
                                    'url': f"https://donstu.ru{conf.find('a').get('href')}"
                                }
                            ])
                if main_containers.find('div', class_='event-box small-event-list'):
                    confs = main_containers.find_all('div', class_='event-box small-event-list')
                    for conf in confs:
                        if conf.find('div', class_='past-event-box'):
                            break
                        conf_name = normalise_str(conf.find('div', class_='title').text)
                        if 'конфер' in conf_name:
                            confer.append(
                                [
                                    {
                                        'title': conf_name,
                                        'desc': normalise_str(conf.find('div', class_='desc').text),
                                        'place': normalise_str(conf.find('div', class_='mark').text),
                                        'date': normalise_str(f"{conf.find('div', class_='date date-last').find(class_='day').text} "
                                                              f"{conf.find('div', class_='date date-last').find(class_='month').text} "
                                                              f"{date.today().year}"),
                                        'url': f"https://donstu.ru{conf.find('a').get('href')}"
                                    }
                                ]
                            )

            for conf in confer:
                get_donstu_page_data(session, un_id, conf[0], date_)

        except Exception as e:
            print(f'Ошибка загрузки данных для {url}')

    except Exception as e:
        raise Exception(f'Не удалось открыть сессию для {__name__}\n{e}')

def get_donstu_page_data(session, un_id, conf, date_):
    try:
        count = 1
        # print(conf)
        while count <= 5:
            try:
                resp = session.get(url=conf["url"], headers=headers, cookies=cookies, timeout=20)
                break
            except:
                print(f'Попытка {count} получить данные со страницы {conf["url"]}')
                count += 1
                time.sleep(2)
                if count > 3:
                    raise Exception('Не удалось загрузить данные с основной страницы')

        if resp.status_code == 404:
            print(f'{resp.status_code} - Нет такой страницы {conf["url"]}')
            return
        print(f'{resp.status_code} - Обработка конференции {conf["url"]}')

        soup = BeautifulSoup(resp.text, 'lxml')

        main_containers = soup.find('div', class_='event-container')

        un_name = 'Донской государственный технический университет'
        conf_name = conf['title']

        conf_s_desc = conf['desc']
        local = False if 'международн' in conf_name.lower() or 'международн' in conf_s_desc.lower() else True

        conf_id = f"{un_id}_{conf['url'].split('/')[-1]}"
        hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
        conf_card_href = conf['url']

        conf_date_begin = str(list(find_date_in_string(conf['date']))[0].date()) if \
            list(find_date_in_string(conf['date'])) else ''
        conf_date_end = str(list(find_date_in_string(conf['date']))[1].date()) if \
            len(list(find_date_in_string(conf['date']))) > 1 else ''

        conf_address = conf['place']

        reg_date_begin = ''
        reg_date_end = ''
        reg_href = ''
        conf_desc = ''
        org_name = ''
        themes = ''

        online = True if 'онлайн' in conf_address.lower() else False
        offline = not online

        conf_href = ''
        contacts = ''
        rinc = False

        lines = main_containers.find('div', class_='text-block')

        if lines.find('p'):
            lines = lines.find_all(['p', 'ul'])

        for line in lines:
            conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

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

            if org_name == '' and 'организатор' in line.text.lower():
                org_name = normalise_str(line.get_text(separator=" "))

            if online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

            if offline and ('место' in line.text.lower() or 'адрес' in line.text.lower()):
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
        print(f'Ошибка загрузки данных для {conf["url"]}.\n{e}')


def parser_donstu(un_id, url, date_):
    try:
        parser_donstu_pages(un_id, url, date_)
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_donstu('donstu', 'https://donstu.ru/events/',
                       datetime.strptime('2023.01.01', '%Y.%m.%d')))

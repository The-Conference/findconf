from datetime import date
from bs4 import BeautifulSoup
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
import requests
import urllib3
from datetime import datetime


result = []
confer = []

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36'
}

def make_queue_kbsu(session, url, filter_date):
    try:
        resp = session.get(url=url, headers=headers, verify=False, timeout=20)
        if resp.status_code == 404:
            print(f'{resp.status_code} - Нет такой страницы {url}')
            return
        soup = BeautifulSoup(resp.text, 'lxml')
        # print(soup)
        main_container = soup.find('div', class_='single__content content').find('div', id='post-112269')

        year = 0
        if 'научные конференции' in main_container.find('h2').text.lower():
            year = int(main_container.find('h2').text.split()[-1])
            if year < filter_date.year:
                print(f'Не найдено данных за {filter_date.year()} год')
                return

        main_container = main_container.find('table').find_all('tr')
        # print(main_container)
        for conf in main_container:
            if conf.find_all('td')[0].text == conf.find_all('td')[-1].text:
                continue

            title = normalise_str(conf.find_all('td')[1].text)
            if 'конфер' in title.lower():
                url_ = ''
                dates_ = normalise_str(f"{conf.find_all('td')[0].text} {year}") if \
                                                        conf.find_all('td')[0].text != '' else ''

                if conf.find('a'):
                    url_ = conf.find('a').get('href')

                confer.append(
                    {
                        'title': title,
                        'link': url_,
                        'dates': dates_,
                    }
                )
        # print(confer)
    except TimeoutError as e:
        print(f'Отказ по таймауту, {url}', e)
    except Exception as e:
        raise Exception(f'Не удалось обработать ссылку в {__name__} для {url}\n{e}')


def make_parse_kbsu(session, un_id, filter_date):
    un_name = 'Кабардино-Балкарский государственный университет им. Х. М. Бербекова'

    for n, conf in enumerate(confer):
        print(f'Обрабатываем запись {n+1} из {len(confer)}')
        conf_name = conf['title']
        local = False if 'международн' in conf_name.lower() else True
        dates = find_date_in_string(conf['dates']) if conf['dates'] != '' else []

        conf_date_begin = str(dates[0].date()) if len(dates) > 0 else ''
        conf_date_end = str(dates[1].date()) if len(dates) > 1 else ''

        conf_card_href = ''
        conf_address = ''

        conf_s_desc = ''
        conf_desc = ''

        reg_date_begin = ''
        reg_date_end = ''
        reg_href = ''

        org_name = ''
        contacts = ''

        themes = ''
        online = False
        conf_href = ''
        offline = True
        themes = ''
        rinc = False

        try:

            if conf['link'] != '':
                resp = session.get(url=conf['link'], headers=headers, verify=False, timeout=20)
                if resp.status_code == 404:
                    print(f"{resp.status_code} - Нет такой страницы {conf['link']}")
                    return
                soup = BeautifulSoup(resp.text, 'lxml')
                # print(soup)
                main_container = soup.find('div', class_='single__content content')
                # print(main_container)

                conf_id = f"{un_id}_{conf['link'].split('/')[-2]}"
                conf_card_href = conf['link']
                lines = main_container.find_all(['p', 'ul', 'ol'])

                for line in lines:
                    # print(line)
                    if conf_s_desc == '':
                        conf_s_desc = normalise_str(line.text)

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
                                           or 'заявк' in line.text.lower()):
                        reg_href = line.find('a').get('href') if line.find('a') \
                                                                 and ('http:' in line.find('a').get('href') or
                                                                      'https:' in line.find('a').get('href')) and \
                                                                 ('.pdf' not in line.find('a').get('href') or
                                                                  '.doc' not in line.find('a').get('href') or
                                                                  '.xls' not in line.find('a').get(
                                                                             'href')) else 'отсутствует'

                    conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

                    if org_name == '' and 'организатор' in line.text.lower():
                        org_name = normalise_str(line.get_text(separator=" "))

                    if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                        online = True
                        conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

                    if not offline and (
                            'город' in line.text.lower() or 'адрес' in line.text.lower() or 'место проведен' in line.text.lower()):
                        offline = True
                        conf_address = normalise_str(line.get_text(separator=" "))

                    if ('тел.' in line.text.lower() or 'контакт' in line.text.lower() or 'mail' in line.text.lower()
                            or 'почта' in line.text.lower() or 'почты' in line.text.lower()):
                        contacts = contacts + ' ' + normalise_str(line.text)

                    if line.find('a') and 'mailto' in line.find('a').get('href'):
                        contacts = contacts + ' ' + normalise_str(line.find('a').text)

                    if not rinc:
                        rinc = True if 'ринц' in line.text.lower() else False

            else:
                conf_id = f"{un_id}_{''.join(conf['title'].split())}"


            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())

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

        except Exception as e:
            raise Exception(f"Не удалось получить данные в {__name__} для {conf['link']}\n{e}")

def parser_kbsu(un_id, urls, date_):
    try:
        session = requests.session()
        urllib3.disable_warnings()
        try:
            for url in urls:
                make_queue_kbsu(session, url, date_)
                make_parse_kbsu(session, un_id, date_)

            with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)
            return result
        except Exception as e:
            print(e)

    except Exception as e:
        raise Exception(f'Не удалось открыть сессию для {__name__}\n{e}')


if __name__ == '__main__':
    print(parser_kbsu('kbsu', ['https://kbsu.ru/nauchnye-konferencii/'], datetime.strptime('2023.01.01', '%Y.%m.%d')))

from datetime import date
from bs4 import BeautifulSoup
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
import requests
import urllib3
from datetime import datetime


result = []

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36'
}

def make_parse_unitech_mo_1(un_id, url, filter_date):
    try:
        session = requests.session()
        try:
            urllib3.disable_warnings()
            resp = session.get(url=url, headers=headers, verify=False, timeout=20)
            if resp.status_code == 404:
                print(f'{resp.status_code} - Нет такой страницы {url}')
                return
            soup = BeautifulSoup(resp.text, 'lxml')
            # print(soup)
            main_container = soup.find('div', class_='content col-12 col-sm-12 col-md-12 col-lg-9')
            # print(main_container)
            year = int(main_container.find('h3').text.split()[-2])
            # print(year)
            if year < filter_date.year:
                raise Exception(f'Не найден год конференций >= {year}.')

            un_name = 'Технологический университет имени дважды Героя Советского Союза, летчика-космонавта А.А. Леонова'

            table = main_container.find('table')
            for line in table.find_all('tr'):
                if normalise_str(line.find('td').text) == 'МЕСЯЦ':
                    continue
                if 'конфер' in line.find_all('td')[-2].text.lower():
                    dates_ = normalise_str(line.find_all('td')[-1].text)
                    conf_name = normalise_str(line.find_all('td')[-2].text)
                    dates = find_date_in_string(dates_)
                    local = False if 'международн' in conf_name.lower() else True

                    conf_date_begin = str(dates[0].date()) if len(dates) > 0 else ''
                    conf_date_end = str(dates[1].date()) if len(dates) > 1 else ''

                    conf_id = f"{un_id}_{''.join(normalise_str(line.find_all('td')[-2].text).split())}_{conf_date_begin}_{conf_date_end}"
                    hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
                    conf_card_href = ''
                    conf_address = dates_

                    conf_s_desc = conf_name
                    conf_desc = conf_name

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

                    if 'онлайн' in conf_name or 'интернет' in conf_name:
                        online = True

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
            raise Exception(f'Не удалось получить данные в {__name__} для {url}\n{e}')
    except Exception as e:
        raise Exception(f'Не удалось обработать очередь для {__name__}\n{e}')

def make_parse_unitech_mo_2(un_id, url, filter_date):
    try:
        session = requests.session()
        try:
            urllib3.disable_warnings()
            resp = session.get(url=url, headers=headers, verify=False, timeout=20)
            if resp.status_code == 404:
                print(f'{resp.status_code} - Нет такой страницы {url}')
                return
            soup = BeautifulSoup(resp.text, 'lxml')
            # print(soup)
            main_container = soup.find_all('div', class_='container')[-3].find('div', class_='content col-12 col-sm-12 col-md-12 col-lg-9')
            # print(main_container)

            un_name = 'Технологический университет имени дважды Героя Советского Союза, летчика-космонавта А.А. Леонова'

            line = main_container.find_next('h4', class_=None)
            while True:
                if 'конфер' in line.text.lower():
                    dates_ = normalise_str(line.find_next('p').text)
                    conf_name = normalise_str(line.text)
                    dates = find_date_in_string(dates_)
                    local = False if 'международн' in conf_name.lower() else True

                    conf_date_begin = str(dates[0].date()) if len(dates) > 0 else ''
                    conf_date_end = str(dates[1].date()) if len(dates) > 1 else ''

                    conf_id = f"{un_id}_{''.join(normalise_str(conf_name).split())}_{conf_date_begin}_{conf_date_end}"
                    hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
                    conf_card_href = ''
                    conf_address = ''

                    conf_s_desc = normalise_str(line.find_next('p').find_next('p').text)
                    conf_desc = conf_s_desc

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

                    if 'онлайн' in conf_name or 'интернет' in conf_name:
                            online = True

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

                try:
                    line = line.find_next('h4')
                    if line.find('a'):
                        break
                except:
                    break

        except Exception as e:
            raise Exception(f'Не удалось получить данные в модуле 2 {__name__} для {url}\n{e}')
    except Exception as e:
        raise Exception(f'Не удалось открыть сессию в модуле 2 для {__name__}\n{e}')

def make_parse_unitech_mo_3(un_id, url, filter_date):
    confer = []
    try:
        session = requests.session()
        try:
            urllib3.disable_warnings()
            resp = session.get(url=url, headers=headers, verify=False, timeout=20)
            if resp.status_code == 404:
                print(f'{resp.status_code} - Нет такой страницы {url}')
                return
            soup = BeautifulSoup(resp.text, 'lxml')
            # print(soup)
            main_container = soup.find('div', class_='content-wrap').find('div', class_='row u-timeline-v1-wrap g-mx-minus-15')
            # print(main_container)
            confs = main_container.find_all('div', class_='col-md-6 g-orientation-right g-pl-60 g-pl-15--md g-pr-40--md g-mb-60 g-mb-0--md')
            for conf in confs:
                if conf.find('a'):
                    title = normalise_str(conf.find('a').text)
                    url = f"https://unitech-mo.ru{conf.find('a').get('href')}"

                    if 'конфер' in title:
                        confer.append(
                            {
                                'title': title,
                                'url': url,
                            }
                        )

        except Exception as e:
            raise Exception(f'Не удалось обработать конференции в модуле 3 {__name__} для {url}\n{e}')

        try:
            for conf in confer:
                resp = session.get(url=conf['url'], headers=headers, verify=False)
                soup = BeautifulSoup(resp.text, 'lxml')
                # print(soup)
                main_container = soup.find('div', class_='content-wrap').find('div', class_='col-md-12')
                # print(main_container)
                un_name = 'Технологический университет имени дважды Героя Советского Союза, летчика-космонавта А.А. Леонова'
                conf_name = conf['title']

                conf_id = f"{un_id}_{conf['url'].split('=')[-1]}"
                hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
                conf_card_href = conf['url']

                conf_s_desc = ''
                themes = ''
                conf_date_begin = ''
                conf_date_end = ''
                reg_date_begin = ''
                reg_date_end = ''
                reg_href = ''
                conf_desc = ''
                org_name = ''
                conf_href = ''
                contacts = ''
                rinc = False
                local = True
                online = False
                offline = True
                conf_address = ''

                lines = main_container.find_all(['p'])

                for line in lines:
                    # print(line)
                    if ('заявк' in line.text.lower() or 'принимаютс' in line.text.lower() or 'участи' in line.text.lower()
                            or 'регистрац' in line.text.lower() or 'регистрир' in line.text.lower()) and reg_date_begin == '':
                        reg_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                            list(find_date_in_string(line.text.lower())) else ''
                        reg_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                            len(list(find_date_in_string(line.text.lower()))) > 1 else ''

                    if ('состоится' in line.text.lower() or 'открытие' in line.text.lower()
                        or 'проведен' in line.text.lower() or 'пройдет' in line.text.lower()) and conf_date_begin == '':
                        conf_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                            list(find_date_in_string(line.text.lower())) else ''
                        conf_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                            len(list(find_date_in_string(line.text.lower()))) > 1 else ''

                    conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

                    if reg_href == '' and ('регистрац' in line.text.lower() or 'зарегистр' in line.text.lower()
                                           or 'участия' in line.text.lower() or 'заявк' in line.text.lower()):
                        reg_href = 'https://unitech-mo.ru' + line.find('a').get('href') if line.find('a') \
                                                                 and ('http:' in line.find('a').get('href') or
                                                                      'https:' in line.find('a').get('href')) and \
                                                                 ('.pdf' not in line.find('a').get('href') or
                                                                  '.doc' not in line.find('a').get('href') or
                                                                  '.xls' not in line.find('a').get(
                                                                             'href')) else 'отсутствует'

                    if org_name == '' and 'организатор' in line.text.lower():
                        org_name = normalise_str(line.get_text(separator=" "))

                    if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower() or
                                       'ссылка' in line.text.lower()):
                        conf_href = 'https://unitech-mo.ru' + line.find('a').get('href') if line.find('a') else 'отсутствует'
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
                             'conf_desc': conf_desc.strip(),
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


        except Exception as e:
            raise Exception(f'Не удалось обработать конференцию в модуле 3 {__name__} для {url}\n{e}')

    except Exception as e:
        raise Exception(f'Не удалось открыть сессию в модуле 3 для {__name__}\n{e}')


def parser_unitech_mo(un_id, urls, date_):
    try:
        make_parse_unitech_mo_1(un_id, urls[0], date_)
        make_parse_unitech_mo_2(un_id, urls[1], date_)
        make_parse_unitech_mo_3(un_id, urls[2], date_)

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_unitech_mo('unitech_mo',
                      ['https://unitech-mo.ru/science/research-activities-/youth-science/calendar-of-scientific-events/',
                       'https://unitech-mo.ru/science/postgraduate-study/scientific-practical-conference/',
                       'https://unitech-mo.ru/announcement/'],
                      datetime.strptime('2023.01.01', '%Y.%m.%d')))

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

def make_queue_mpgu(session, url, filter_date):

    page = 0
    while True:
        page += 1
        url_ = f"{url}/page/{page}/" if page > 1 else url
        print(page, url_)
        try:
            resp = session.get(url=url_, headers=headers, timeout=20)
            if resp.status_code == 404:
                print(f'{resp.status_code} - Нет такой страницы {url_}')
                return
            soup = BeautifulSoup(resp.text, 'lxml')
            # print(soup)
            main_container = soup.find_all('div', class_='media announcement')
            if not main_container:
                break

            # print(main_container)
            for conf in main_container:
                tag = conf.h5
                tag.clear()
                title = normalise_str(conf.find('div', class_='media-body').find('a').text)
                if 'конфер' in title.lower():
                    confer.append(
                        {
                            'title': title,
                            'link': f"{conf.find('div', class_='media-body').find('a').get('href')}",
                        }
                    )
            # print(confer)

        except TimeoutError as e:
            print(f'Отказ по таймауту {url}', e)
        except Exception as e:
            raise Exception(f'Не удалось обработать ссылку в {__name__} для {url}\n{e}')


def parser_mpgu_pages(session, un_id, filter_date):
    def date_str_prep(str):
        names = [' january ', ' february ', ' march ', ' april ', ' may ', ' june ',
                 ' july ', ' august ', ' september ', ' october ', ' november ', ' december ']
        nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        months = dict(zip(nums, names))
        for k, v in months.items():
            if f'/{k}/' in str:
                str = str.replace(f'/{k}/', f'{v}')
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
            conf_block = soup.find('div', class_='col-xs-12 col-sm-6 col-md-8').find('div', class_='content')
            if not conf_block:
                print(f"Блок описания конференции {conf['link']} отсутствует.")
                return
            # print(conf_block)

            un_name = 'Московский педагогический государственный университет'
            conf_name = conf['title']
            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{conf['link'].split('/')[-2]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            conf_card_href = conf['link']
            conf_s_desc = ''

            lines = conf_block.find_all(['p', 'ul', 'ol', 'h6'])
            # print(lines)

            themes = ''

            dates = find_date_in_string(
                date_str_prep(normalise_str(soup.find('div', class_='col-xs-12 col-sm-6 col-md-8').find('h3').text)))
            conf_date_begin = str(dates[0].date()) if len(dates) > 0 else ''
            conf_date_end = str(dates[1].date()) if len(dates) > 1 else ''

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
                                                          '.xls' not in line.find('a').get('href')) else 'отсутствует'

                conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

                if org_name == '' and 'организатор' in line.text.lower():
                    org_name = normalise_str(line.get_text(separator=" "))

                if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                    online = True
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

                if not offline and ('город' in line.text.lower() or 'адрес' in line.text.lower() or 'место проведен' in line.text.lower()):
                    offline = True
                    conf_address = normalise_str(line.get_text(separator=" "))

                if ('тел.' in line.text.lower() or 'контакт' in line.text.lower() or 'mail' in line.text.lower()
                        or 'почта' in line.text.lower() or 'почты' in line.text.lower()):
                    contacts = contacts + ' ' + normalise_str(line.text)

                if line.find('a'):
                    try:
                        if 'mailto' in line.find('a').get('href'):
                            contacts = contacts + ' ' + normalise_str(line.find('a').text)
                    except:
                        contacts = contacts

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
    except asyncio.TimeoutError as e:
        print(f"Отказ по таймауту, {n + 1} из {len(confer)}, {conf['link']}", e)

def parser_mpgu(un_id, url, date_):
    try:
        session = requests.session()

        make_queue_mpgu(session, url, date_)
        parser_mpgu_pages(session, un_id, date_)

        session.close()

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_mpgu('mpgu', 'http://mpgu.su/category/anonsyi', datetime.strptime('2023.01.01', '%Y.%m.%d')))

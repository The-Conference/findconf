from datetime import date
from bs4 import BeautifulSoup
import json
import requests
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

def make_parse_bstu(un_id, url, filter_date):
    session = requests.session()
    year = date.today().year
    un_name = 'БГТУ им. В.Г. Шухова'
    while True:
        if year < filter_date.year:    # дальше в дебри нет смысла лезть
            break
        url_ = f'{url}/{year}' if year < date.today().year else url
        resp = session.get(url=url_, headers=headers, timeout=20)
        if resp.status_code == 404:
            print(f'{resp.status_code} - Нет такой страницы {url_}')
            return
        soup = BeautifulSoup(resp.text, 'lxml')
        main_container = soup.find('article', class_='content').find_all(['li'])
        # print(main_container)
        for line in main_container:
            conf_name = f"{line.find('a').get_text(separator=' ')} {line.text}" if line.find('a') else line.text
            conf_name = f'{normalise_str(conf_name)} {year}' if 'года' not in conf_name else normalise_str(conf_name)
            conf_s_desc = conf_name
            conf_desc = conf_name

            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{conf_name.replace(' ', '')}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())

            dates = list(find_date_in_string(conf_name[len(conf_name)-30:]))
            conf_date_begin = str(dates[0].date()) if dates else ''
            conf_date_end = str(dates[1].date()) if len(dates) > 1 else ''

            reg_date_begin = ''
            reg_date_end = ''

            reg_href = ''
            pre_ref = 'https://conf.bstu.ru' if line.find('a') and line.find('a').get('href').split('/')[1] == 'shared' else ''
            conf_card_href = f"{pre_ref}{line.find('a').get('href')}" if line.find('a') else ''
            org_name = ''
            themes = ''
            online = False
            conf_href = ''
            offline = False
            conf_address = ''
            contacts = ''
            rinc = False

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
        year -= 1
        # break

def parser_bstu(un_id, urls, date_):
    try:
        for url in urls:
            make_parse_bstu(un_id, url, date_)

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_bstu('bstu', ['https://conf.bstu.ru/conf_bstu'], datetime.strptime('2023.01.01', '%Y.%m.%d')))

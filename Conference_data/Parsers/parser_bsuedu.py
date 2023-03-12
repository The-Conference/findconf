import time
from datetime import date
from bs4 import BeautifulSoup
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime
from platform import system
import requests
import urllib3

headers = {
    'authority': 'www.bsuedu.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'BITRIX_SM_GUEST_ID=4478564; PHPSESSID=Dcz9HiamegrCO77xaxjIlU3p1nJC64y2; BITRIX_SM_LAST_VISIT=03.03.2023%2008%3A26%3A02',
    'referer': 'https://www.bsuedu.ru/bsu/science/meropr/',
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

def make_queue_bsuedu(session, url, filter_date):

    def date_str_prep(str):
        names = [' january ', ' february ', ' march ', ' april ', ' may ', ' june ',
                 ' july ', ' august ', ' september ', ' october ', ' november ', ' december ']
        nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        months = dict(zip(nums, names))
        for k, v in months.items():
            if f'.{k}.' in str:
                str = str.replace(f'.{k}.', f'{v}')
        return str


    start_date = f'{filter_date.day}.{filter_date.month}.{filter_date.year}'
    end_date = f'{date.today().day}.{date.today().month}.{date.today().year+1}'
    url_ = url + f'?arrFilter_ff%5BNAME%5D=&arrFilter_DATE_ACTIVE_FROM_1_DAYS_TO_BACK=&arrFilter_DATE_ACTIVE_FROM_1={start_date}+12%3A00%3A00&arrFilter_DATE_ACTIVE_FROM_2={end_date}+12%3A00%3A00&arrFilter_pf%5Btype%5D=&arrFilter_pf%5Bkategoria%5D=&arrFilter_pf%5Bplace%5D=&set_filter=&set_filter=Y'

    try:
        resp = session.get(url=url, headers=headers, verify=False, timeout=20)
        if resp.status_code == 404:
            print(f'{resp.status_code} - Нет такой страницы {url}')
            return
        soup = BeautifulSoup(resp.text, 'lxml')
        # print(soup)
        main_container = soup.find('div', class_='typo-page').find('div', class_='news-list').find('table').find_all('td')
        # print(main_container)

        for conf_ in main_container:
            if not conf_.find('font', class_='detail_text'):
                continue
            conf = conf_.find('font', class_='detail_text')
            # print(conf)
            link = f"{url}{conf.find('a').get('href')}"
            title = normalise_str(conf.find('a').get_text(separator=" "))
            if 'конфер' in title.lower():
                # print(title, link)
                block_ = conf.find('div', class_='prop_block').find_all('div')
                begin, end, reg_end, format_, place, org, cont = '', '', '', '', '', '', ''
                for line in block_:
                    if begin == '' and 'Дата начала' in line.find('span', class_='param_tit').text:
                        begin = date_str_prep(normalise_str(line.find('font', class_='ogr_text').text))

                    if end == '' and 'Дата окончания' in line.find('span', class_='param_tit').text:
                        end = date_str_prep(normalise_str(line.find('font', class_='ogr_text').text))

                    if reg_end == '' and 'Срок окончания приёма заявок' in line.find('span',class_='param_tit').text:
                        reg_end = date_str_prep(normalise_str(line.find('font', class_='ogr_text').text))

                    if format_ == '' and 'Формат проведения' in line.find('span', class_='param_tit').text:
                        format_ = normalise_str(line.find('font', class_='ogr_text').text)

                    if place == '' and 'Место проведения' in line.find('span', class_='param_tit').text:
                        place = normalise_str(line.find('font', class_='ogr_text').text)

                    if org == '' and 'Организатор' in line.find('span', class_='param_tit').text:
                        org = normalise_str(line.find('font', class_='ogr_text').text)

                    if cont == '' and 'Контактная информация' in line.find('span', class_='param_tit').text:
                        cont = normalise_str(line.find('font', class_='ogr_text').text)

                confer.append(
                    {
                        'title': title,
                        'link': link,
                        'begin': begin,
                        'end': end,
                        'reg_end': reg_end,
                        'format': format_,
                        'place': place,
                        'org': org,
                        'cont': cont,
                    }
                )

    except TimeoutError as e:
        print(f'Отказ по таймауту {url_}', e)
    except Exception as e:
        raise Exception(f'Не удалось обработать ссылку в {__name__} для {url_}\n{e}')


def parser_bsuedu_pages(session, un_id):
    try:
        for n, conf in enumerate(confer):
            print(f"Обработка конференции {n + 1} из {len(confer)}, {conf['link']}")
            # print(conf)
            resp = session.get(url=conf['link'], headers=headers, verify=False, timeout=20)
            if resp.status_code == 404:
                print(f"{resp.status_code} - Нет такой страницы {conf['link']}")
                continue
            soup = BeautifulSoup(resp.text, 'lxml')
            conf_block = soup.find('div', class_='news-detail')
            if not conf_block:
                print(f"Блок описания конференции {conf['link']} отсутствует.")
                return

            un_name = 'Белгородский государственный национальный исследовательский университет'
            conf_name = conf['title']
            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{conf['link'].split('=')[-1]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            conf_card_href = conf['link']

            conf_date_begin = str(find_date_in_string(conf['begin'])[0].date()) if conf['begin'] else ''
            conf_date_end = str(find_date_in_string(conf['end'])[0].date()) if conf['end'] else ''
            reg_date_begin = ''
            reg_date_end = str(find_date_in_string(conf['reg_end'])[0].date()) if conf['reg_end'] else ''
            org_name = conf['org']
            conf_address = conf['place']
            contacts = conf['cont']
            online = True if 'онлайн' in conf['format'].lower() or 'видеоконф' in conf['format'].lower() or\
                             'комбинир' in conf['format'].lower() else False
            offline = True if 'очный' in conf['format'].lower() or 'комбинир' in conf['format'].lower() else False

            themes = ''
            conf_desc = ''
            conf_s_desc = ''
            reg_href = ''
            conf_href = ''
            rinc = False

            lines = conf_block.find_all(['p', 'ul'])

            for line in lines:
                # print(line)
                if conf_s_desc == '':
                    conf_s_desc = normalise_str(line.text)

                if reg_href == '' and ('регистрац' in line.text.lower() or 'зарегистр' in line.text.lower()
                                   or 'заявк' in line.text.lower()):
                    reg_href = line.find('a').get('href') if line.find('a') \
                                                         and ('http:' in line.find('a').get('href') or
                                                              'https:' in line.find('a').get('href')) and \
                                                         ('.pdf' not in line.find('a').get('href') or
                                                          '.doc' not in line.find('a').get('href') or
                                                          '.xls' not in line.find('a').get('href')) else 'отсутствует'

                conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

                if online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

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

    except TimeoutError as e:
        print(f"Отказ по таймауту, {n + 1} из {len(confer)}, {conf['link']}", e)


def parser_bsuedu(un_id, url, date_):
    try:
        session = requests.session()
        urllib3.disable_warnings()

        make_queue_bsuedu(session, url, date_)
        parser_bsuedu_pages(session, un_id)

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_bsuedu('bsuedu', 'https://www.bsuedu.ru/bsu/science/meropr/', datetime.strptime('2023.01.01', '%Y.%m.%d')))

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

def get_detail_data(session, url):
    desc = ''
    href = ''
    try:
        resp = session.get(url=url, headers=headers, verify=False, timeout=20)
        if resp.status_code == 404:
            print(f'{resp.status_code} - Нет такой страницы {url}')
            return
        soup = BeautifulSoup(resp.text, 'lxml')
        # print(soup)
        main_container = soup.find_all('div', class_='container container-mrsu-pad')[-1]
        # print(main_container)

        for line in main_container.find_all('div', class_='info__text'):
            desc = desc + ' ' + normalise_str(line.text)
            if 'регистрация' in line.text.lower() or 'заявк' in line.text.lower():
                conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

    except Exception as e:
        print(f'Не удалось получить детальные данные для {url}\n{e}')

    return desc.strip(), href


def make_parse_mrsu(un_id, url, filter_date):
    def date_str_prep(str):
        names = [' january ', ' february ', ' march ', ' april ', ' may ', ' june ',
                 ' july ', ' august ', ' september ', ' october ', ' november ', ' december ']
        nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        months = dict(zip(nums, names))
        for k, v in months.items():
            if f'.{k}.' in str:
                str = str.replace(f'-{k}-', f'{v}')
        return str

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
            main_container = soup.find_all('div', class_='container container-mrsu-pad')[-1]
            # print(main_container)

            #  Дальше первой страницы идти бессмысленно, порядок хронологический, все новые вначале
            un_name = 'Национальный исследовательский Мордовский государственный университет им. Н.П. Огарева'

            for n, conf in enumerate(main_container.find_all('div', class_='b-element')):
                print(f"Обработка конференции {n+1} из {len(main_container.find_all('div', class_='b-element'))}.")
                conf_name = normalise_str(conf.find('div', class_='head__local__institution_with_bread').text)

                reg_date_begin = ''
                reg_date_end = ''

                conf_card_href = f"https://mrsu.ru{conf.find('div', class_='head__local__institution_with_bread').find('a').get('href')}" if \
                    conf.find('div', class_='head__local__institution_with_bread').find('a') else ''

                local = False if 'международн' in conf_name.lower() else True

                conf_date_begin = ''
                conf_date_end = ''
                conf_s_desc = ''
                conf_desc = ''
                conf_address = ''
                online = False
                offline = True
                reg_href = ''
                org_name = ''
                contacts = ''
                conf_href = ''
                themes = ''
                rinc = False

                for line in conf.find_all('div', class_='info__text'):

                    if 'Дата начала' in line.text:
                        conf_date_begin = str(list(find_date_in_string(date_str_prep(line.text)))[0].date())
                    if 'Дата окончания' in line.text:
                        conf_date_end = str(list(find_date_in_string(date_str_prep(line.text)))[0].date())

                    if conf_s_desc == '':
                        conf_s_desc = normalise_str(line.text)

                    if conf_card_href != '':
                        conf_desc, conf_href = get_detail_data(session, conf_card_href)

                    if 'Место проведения конференции' in line.text:
                        conf_address = normalise_str(line.text)

                    online = True if not online and ('онлайн' in conf_address or 'смешанный' in conf_address) else False
                    offline = False if offline and 'онлайн' in conf_address else True

                    if 'Организатор' in line.text:
                        org_name = normalise_str(line.text)

                    if 'Исполнитель' in line.text:
                        contacts = contacts + normalise_str(line.text)
                    if 'Контакты' in line.text:
                        contacts = contacts + ' ' + normalise_str(line.text)

                conf_id = f"{un_id}_{''.join(conf_name.split())}_{conf_date_begin}_{conf_date_end}"
                hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())

                if 'ринц' in conf_desc:
                    rinc = True

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

def parser_mrsu(un_id, url, date_):
    try:
        make_parse_mrsu(un_id, url, date_)

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_mrsu('mrsu', 'https://mrsu.ru/ru/sci/conferences/', datetime.strptime('2023.01.01', '%Y.%m.%d')))

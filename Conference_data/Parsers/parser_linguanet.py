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


def make_parse_linguanet(un_id, urls, filter_date):
    session = requests.session()
    resp = session.get(url=urls[0], headers=headers, timeout=20)
    if resp.status_code == 404:
        print(f'{resp.status_code} - Нет такой страницы {urls[0]}')
        return
    print(f'Обработка ссылки {urls[0]}')
    soup = BeautifulSoup(resp.text, 'lxml')
    main_container = soup.find('div', class_='page col-xs-12 col-sm-9').find_all(['p', 'div'])
    un_name = normalise_str(soup.find('div', class_='headerLogo hidden-xs').find('a').text)
    # print(main_container)
    for line in main_container:
        conf_name = normalise_str(line.get_text(separator=" "))
        if 'конфер' in conf_name:
            # print(conf_name)
            if conf_name == 'Ссылка на официальный сайт конференции   Информационное письмо':
                continue
            conf_s_desc = conf_name
            conf_desc = conf_name

            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{conf_name.replace(' ', '')}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())

            reg_date_begin = ''
            reg_date_end = ''

            reg_href = ''
            conf_card_href = ''
            org_name = ''
            themes = ''
            online = False
            conf_href = ''
            offline = False
            conf_address = ''
            contacts = ''
            rinc = False

            txt_dates = conf_name.replace(' - ', '-')
            # print(txt_dates)
            dates = list(find_date_in_string(txt_dates[:25]))
            # print(dates)
            conf_date_begin = str(dates[0].date()) if dates else ''
            conf_date_end = str(dates[1].date()) if len(dates) > 1 else ''

            a_ = line.find_all('a')
            if reg_href == '':
                for _ in a_:
                    if 'регистрац' in _.text.lower():
                        reg_href = _.get('href')
                    if ('информационное' in _.text.lower() or 'подробнее' in _.text.lower()):
                        conf_card_href = 'https://www.linguanet.ru' + _.get('href')
                    if 'ссылка на официальный' in _.text.lower():
                        conf_card_href = _.get('href')

            # print(reg_href)
            # print(conf_card_href)
            # print('----------')
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
            # break

    session = requests.session()
    resp = session.get(url=urls[1], headers=headers, timeout=20)
    if resp.status_code == 404:
        print(f'{resp.status_code} - Нет такой страницы {urls[1]}')
        return
    print(f'Обработка ссылки {urls[1]}')
    soup = BeautifulSoup(resp.text, 'lxml')

    main_container = soup.find('div', class_='page col-xs-12 col-sm-9').find_all('div', class_='news-index clearfix')

    for line in main_container:
        conf_name = normalise_str(line.find('a').text)
        # print(conf_name)
        tag = line.div
        tag.clear()
        tag = line.a
        tag.clear()
        conf_s_desc = normalise_str(line.get_text(separator=" "))
        # print(conf_s_desc)
        if 'конфер' in conf_s_desc.lower():
            local = False if 'международн' in conf_s_desc.lower() else True

            conf_desc = ''
            reg_date_begin = ''
            reg_date_end = ''

            reg_href = ''
            conf_card_href = 'https://www.linguanet.ru' + line.find('a').get('href')
            conf_id = f"{un_id}_{conf_card_href.split('/')[-1].split('=')[-1]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            org_name = ''
            themes = ''
            online = False
            conf_href = ''
            offline = False
            conf_address = ''
            contacts = ''
            rinc = False

            dates = list(find_date_in_string(conf_s_desc))
            # print(dates)
            conf_date_begin = str(dates[0].date()) if len(dates) > 0 else ''
            conf_date_end = str(dates[1].date()) if len(dates) > 1 else ''
            # print(conf_date_begin, conf_date_end)

            if not conf_card_href == '':
                resp = session.get(url=conf_card_href, headers=headers)
                soup = BeautifulSoup(resp.text, 'lxml')
                main_container = soup.find('div', class_='news-detail')
                tag = main_container.div
                tag.clear()

                conf_desc = normalise_str(main_container.text)
                main_container = main_container.find_all(['div', 'p'])
                # print(main_container)

                for div in main_container:
                    # print(div.text)
                    if not ('class="date"' in str(div)):
                        conf_desc = conf_desc + ' ' + normalise_str(div.get_text(separator=" "))

                    if not online and ('онлайн' in div.text.lower() or 'трансляц' in div.text.lower()):
                        online = True
                        conf_href = div.find('a').get('href') if div.find('a') else 'отсутствует'
                    if not offline and ('место' in div.text.lower() or 'адрес' in div.text.lower()):
                        offline = True
                        conf_address = normalise_str(div.get_text(separator=" "))

                    if ('заявк' in div.text.lower() or 'принимаютс' in div.text.lower() or 'участи' in div.text.lower()
                                                or 'регистрац' in div.text.lower() or 'регистрир' in div.text.lower()) \
                                                and reg_date_begin == '':
                                        reg_date_begin = str(list(find_date_in_string(div.text.lower()))[0].date()) if \
                                            list(find_date_in_string(div.text.lower())) else ''
                                        reg_date_end = str(list(find_date_in_string(div.text.lower()))[1].date()) if \
                                            len(list(find_date_in_string(div.text.lower()))) > 1 else ''

                    if org_name == '' and 'организатор' in div.text.lower():
                        org_name = normalise_str(div.get_text(separator=" "))

                    if ('тел.' in div.text.lower() or 'контакт' in div.text.lower() or 'mail' in div.text.lower()
                            or 'почта' in div.text.lower() or 'почты' in div.text.lower() or '@' in div.text.lower()):
                        contacts = contacts + ' ' + normalise_str(div.text)

                    if div.find('a') and 'mailto' in div.find('a').get('href'):
                        contacts = contacts + ' ' + normalise_str(div.find('a').text)

                    if not rinc:
                        rinc = True if 'ринц' in div.text.lower() else False

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
            # break


def parser_linguanet(un_id, url, date_):
    try:
        make_parse_linguanet(un_id, url, date_)
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_linguanet('linguanet',
                           ['https://www.linguanet.ru/science/konferentsii-i-seminary/',
                            'https://www.linguanet.ru/science/konferentsii-i-seminary/konferentsii-v-drugikh-vuzakh/'],
                           datetime.strptime('2023.01.01', '%Y.%m.%d')))

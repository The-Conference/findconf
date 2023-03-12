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

def make_queue_timacad(session, url):
    try:
        resp = session.get(url=url, headers=headers, timeout=20)
        if resp.status_code == 404:
            print(f'{resp.status_code} - Нет такой страницы {url}')
            return
        soup = BeautifulSoup(resp.text, 'lxml')
        # print(soup)
        main_container = soup.find('div', class_='row mt20').find_all('div', class_='col-12')
        if not main_container:
            return

        # print(main_container)
        for conf in main_container:
            title = normalise_str(conf.find('h2', class_='announce-item__title').text)
            if 'конфер' in title.lower():
                confer.append(
                    {
                        'title': title,
                        'link': f"https://www.timacad.ru{conf.find('a').get('href')}",
                    }
                )
            # print(confer)

    except TimeoutError as e:
        print(f'Отказ по таймауту {url}', e)
    except Exception as e:
        raise Exception(f'Не удалось обработать ссылку в {__name__} для {url}\n{e}')


def parser_timacad_pages(session, un_id, filter_date):
    try:
        for n, conf in enumerate(confer):
            print(f"Обработка конференции {n + 1} из {len(confer)}, {conf['link']}")
            resp = session.get(url=conf['link'], headers=headers, timeout=20)
            if resp.status_code == 404:
                print(f"{resp.status_code} - Нет такой страницы {conf['link']}")
                return
            soup = BeautifulSoup(resp.text, 'lxml')
            # print(soup)
            conf_block = soup.find('div', class_='news-inner')
            if not conf_block:
                print(f"Блок описания конференции {conf['link']} отсутствует.")
                return
            # print(conf_block)

            un_name = 'Российский государственный аграрный университет - МСХА имени К.А. Тимирязева'
            conf_name = conf['title']
            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{conf['link'].split('/')[-1]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            conf_card_href = conf['link']
            conf_s_desc = normalise_str(conf_block.find('p', class_='news-inner__description').text)

            lines = conf_block.find('div', class_='news-inner__content').find_all(['p', 'ul', 'ol'])
            # print(lines)

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

            for line in lines:
                # print(line)
                if conf_s_desc == '':
                    conf_s_desc = normalise_str(line.text)

                if ('состоится' in line.text.lower() or 'открытие' in line.text.lower()
                        or 'проведен' in line.text.lower() or 'пройдет' in line.text.lower()
                        or 'пройдёт' in line.text.lower() or 'прошла' in line.text.lower()
                        or 'проводят' in line.text.lower()) and conf_date_begin == '':
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
    except TimeoutError as e:
        print(f"Отказ по таймауту, {n + 1} из {len(confer)}, {conf['link']}", e)

def parser_timacad(un_id, url, date_):
    try:
        session = requests.session()

        make_queue_timacad(session, url)
        parser_timacad_pages(session, un_id, date_)

        session.close()

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_timacad('timacad', 'https://www.timacad.ru/science/konferentsii', datetime.strptime('2023.01.01', '%Y.%m.%d')))

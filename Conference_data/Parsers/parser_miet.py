from datetime import date
from bs4 import BeautifulSoup
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
import time


result = []
confer = []

def make_queue_miet(driver, un_id, url):
    try:
        driver.get(url=url)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        main_container = soup.find('header', class_='site-header').find_all('div',
                                                            class_='header-menu__toggable-item__list-item')
        new_url = ''
        for main in main_container:
            if main.find('a').text == 'Конференции и семинары':
                new_url = url + main.find('a').get('href')

        if new_url == '':
            print(f'Не удалось найти ссылку на конференции в {url}')
            return

        print(new_url)
        tasks = []
        try:
            driver.get(url=new_url)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            main_container = soup.find('div', class_='site-sidebar site-sidebar__left')
            # print(main_container)
            confer.append(new_url)
            confs = main_container.find_all('a', class_='site-sidebar__item-link')
            for n, conf in enumerate(confs):
                # print(conf)
                if 'Архив конференций' not in conf.text:
                    confer.append(url + conf.get('href'))
        except:
            raise Exception(f'Облом с сайтом, защита. {new_url} ')
    except Exception as e:
        raise Exception(f'Не удалось открыть WebDriver в {__name__} для {url}\n{e}')


def parser_miet_pages(driver, un_id, filter_date):
    for n, conf in enumerate(confer):
        try:
            print(f"Обработка конференции {n+1} из {len(confer)}, {conf}")
            driver.get(url=conf)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            main_container = soup.find('div', class_='info-content')

            un_name = 'Национальный исследовательский университет «МИЭТ»'
            conf_name = normalise_str(main_container.find('div', class_='info-title').text)

            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{conf.split('/')[-1]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            conf_card_href = conf

            lines = main_container.find_all(['p'])

            themes = ''
            conf_s_desc = ''
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
            # print(len(lines))
            for line in lines:
                # print(line.text)
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
                                   or 'участия' in line.text.lower() or 'заявк' in line.text.lower()):
                    reg_href = line.find('a').get('href') if line.find('a') \
                                                         and ('http:' in line.find('a').get('href') or
                                                              'https:' in line.find('a').get('href')) and \
                                                         ('.pdf' not in line.find('a').get('href') or
                                                          '.doc' not in line.find('a').get('href') or
                                                          '.xls' not in line.find('a').get('href')) else 'отсутствует'

                conf_desc = conf_desc + ' ' + normalise_str(line.text)

                if org_name == '' and 'организатор' in line.text.lower():
                    org_name = normalise_str(line.text)

                if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                    online = True
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

                if not offline and ('город' in line.text.lower() or 'адрес' in line.text.lower()):
                    offline = True
                    conf_address = normalise_str(line.text)

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
                         'conf_desc': conf_desc,
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

        except TimeoutException as e:
            print(f"Отказ по таймауту, конференция {n+1} из {len(confer)}, {conf}", e)


def parser_miet(un_id, url, date_):
    try:
        options = webdriver.ChromeOptions()
        service = Service(executable_path='chromedriver/chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        # driver.minimize_window()

        make_queue_miet(driver, un_id, url)
        # print(confer)
        parser_miet_pages(driver, un_id, date_)

        driver.close()
        driver.quit()

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result

    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_miet('miet', 'https://miet.ru', datetime.strptime('2023.01.01', '%Y.%m.%d')))

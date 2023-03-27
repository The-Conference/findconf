from datetime import date
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
import time
from platform import system


result = []
confer = []
def get_sfu_kras_conf_data(driver, url, year):
    url_ = f'{url}confs/{year}'
    try:
        driver.get(url=url_)
        time.sleep(1)

        print(f'Запрос данных за {year} год, по {url_}')
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # print(soup)
        main_container = soup.find('div', class_='confs-container')
        # print(main_container)
        if 'ни одной конференции не найдено' in main_container.text.lower():
            return False

        for conf in main_container.find_all('div', class_='listItem'):
            if conf.find('a'):
                link = f"https://conf.sfu-kras.ru{conf.find('a').get('href')}"
                dates = normalise_str(conf.find('span', class_='date').text)
                tag = conf.span
                tag.clear()
                title = normalise_str(conf.text)
                if 'конфер' in title:
                    confer.append(
                        {
                            'title': title,
                            'link': link,
                            'dates': dates,
                         }
                        )
        return True
    except TimeoutException as e:
        print(f'Отказ по таймауту, {year} год, по {url_}', e)
    except Exception as e:
        raise Exception(f'Нарушена структура ответа с {url_} за {year} год\n{e}')


def make_queue_sfu_kras(driver, url, filter_date):
    year = filter_date.year
    while year <= date.today().year + 1:
        while True:
            if get_sfu_kras_conf_data(driver, url, year):
                year += 1
            else:
                print(f'Нет данных на странице за {year} год.')
                break
        year += 1

def parser_sfu_kras_pages(driver, un_id, filter_date):
    for n, conf in enumerate(confer):
        try:
            driver.get(url=conf['link'])
            time.sleep(1)
            print(f"Запрос данных {n+1} из {len(confer)}, {conf['link']}")
            soup = BeautifulSoup(driver.page_source, 'lxml')
            # print(soup)

            conf_block = soup.find('div', class_='confs-container')

            if not conf_block:
                print(f"Блок описания конференции {conf['link']} отсутствует.")
                return

            un_name = 'Сибирский федеральный университет'
            conf_name = conf['title']
            conf_s_desc = conf_name
            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{conf['link'].split('/')[-1]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            conf_card_href = conf['link']

            lines = conf_block.find_all('div', class_='row')

            themes = ''

            dates = find_date_in_string(conf['dates'])
            conf_date_begin = str(dates[0].date()) if len(dates) > 0 else ''
            conf_date_end = str(dates[1].date()) if len(dates) > 1 else ''

            reg_date_begin = ''
            reg_date_end = ''
            reg_href = ''
            conf_desc = ''
            org_name = ''
            online = False
            offline = True
            conf_address = ''
            conf_href = ''
            contacts = ''
            rinc = False

            for line in lines:

                try:
                    if line.find('div', class_='label').text == 'Дата окончания регистрации:':
                        reg_date_end = str(find_date_in_string(normalise_str(line.find('div', class_='field').text))[0].date())
                except:
                    reg_date_end == ''

                try:
                    if line.find('span', class_='button-title').text == 'Регистрация':
                        reg_href = f"https://conf.sfu-kras.ru{line.find('a').get('href')}"
                except:
                    reg_href == ''

                conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

                if org_name == '' and 'организатор' in line.text.lower():
                    org_name = normalise_str(line.get_text(separator=" "))

                if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                    online = True
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

                try:
                    if line.find('div', class_='label').text == 'Место проведения:':
                        conf_address = normalise_str(line.find('div', class_='field').text)
                except:
                    conf_address == ''

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

        except asyncio.TimeoutError as e:
            print(f"Отказ по таймауту, конференция {n + 1} из {len(confer)}, {conf['link']}", e)


def get_griver_path():
    path = 'chromedriver/'
    if system() == 'Windows':
        path = f'{path}win/chromedriver.exe'
    if system() == 'Linux':
        path = f'{path}linux/chromedriver'
    if system() == 'Darwin':
        path = f'{path}darwin/chromedriver'
    return path


def parser_sfu_kras(un_id, url, date_):
    try:
        options = webdriver.ChromeOptions()
        service = Service(executable_path=get_griver_path())
        driver = webdriver.Chrome(service=service, options=options)
        # driver.minimize_window()

        make_queue_sfu_kras(driver, url, date_)
        parser_sfu_kras_pages(driver, un_id, date_)

        driver.close()
        driver.quit()

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_sfu_kras('sfu-kras', 'https://conf.sfu-kras.ru/', datetime.strptime('2023.01.01', '%Y.%m.%d')))

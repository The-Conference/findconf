from datetime import date
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime
from platform import system
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
import time


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36'
}

result = []

async def make_queue_mgppu(driver, un_id, url, filter_date):
    page = 1  # дальше 1 страницы бессмысленно, уже тут 2022 год
    params = {
        'searchStr': '',
        'eventtype_conference': 'y',
        'page': f'{page}',
    }
    try:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, headers=headers, timeout=20) as response:
                    if response.status == 404:
                        print(f'{response.status} - Нет такой страницы {url}')
                        return
                    response_text = await response.text()
                    soup = BeautifulSoup(response_text, 'lxml')
                    main_container = soup.find('section', class_='module-index-news module-index-news-inner').find_all('div', class_='item-new')
                    # print(main_container)
                    print(f'{response.status} Запрос данных со страницы {page}, {url}')
                    tasks = []
                    for n, conf in enumerate(main_container):
                        if conf.find('a'):
                            link = f"https://mgppu.ru{conf.find('a', class_='new-link').get('href')}"
                            try:
                                # print(link)
                                task = asyncio.create_task(parser_mgppu_pages(driver, un_id, link, n, len(main_container), filter_date))
                                tasks.append(task)
                            except Exception as e:
                                raise Exception(f'Не удалось обработать очередь в {__name__} для {url}\n{e}')

                            await asyncio.gather(*tasks)

            except asyncio.TimeoutError as e:
                print(f'Отказ по таймауту, страница {page}, {url}', e)
            except Exception as e:
                raise Exception(f'Не удалось обработать ссылку в {__name__} для {url}\n{e}')

    except Exception as e:
        raise Exception(f'Не удалось открыть сессию для {__name__}\n{e}')

async def parser_mgppu_pages(driver, un_id, url, n, confs, filter_date):
    try:
        driver.get(url=url)
        time.sleep(1)
        print(f"Обработка конференции {n + 1} из {confs}, {url}")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # print(soup)
        conf_block = soup.find('div', class_='page container').find('div', class_='col-sm-12')
        # print(conf_block)

        if not conf_block:
            print(f"Блок описания конференции {url} отсутствует.")
            return

        un_name = 'Московский государственный психолого-педагогический университет'
        conf_name = normalise_str(conf_block.find('h1').get_text(separator=" "))
        local = False if 'международн' in conf_name.lower() else True

        conf_id = f"{un_id}_{url.split('/')[-1]}"
        hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
        conf_card_href = url

        dates = find_date_in_string(conf_block.find('div', class_='col-xs-6').find('time').text)

        conf_date_begin = str(list(dates)[0].date()) if list(dates) else ''
        conf_date_end = str(list(dates)[1].date()) if len(list(dates)) > 1 else ''
        # print(conf_block.find('div', class_='col-xs-6').find('time').text, dates)
        # print(conf_date_begin, conf_date_end)

        if (conf_date_begin != '' and datetime.strptime(conf_date_begin,
                                                        '%Y-%m-%d') >= filter_date) or conf_date_begin == '':

            lines = conf_block.find_all(['p', 'ul', 'ol'])

            themes = ''
            conf_s_desc = conf_name
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
                                                          '.xls' not in line.find('a').get('href')) else ''

                conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

                if org_name == '' and 'организатор' in line.text.lower():
                    org_name = normalise_str(line.get_text(separator=" "))

                if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                    online = True
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

                if not offline and ('город' in line.text.lower() or 'адрес' in line.text.lower()):
                    offline = True
                    conf_address = normalise_str(line.get_text(separator=" "))

                if ('тел.' in line.text.lower() or 'контакт' in line.text.lower() or 'mail' in line.text.lower()
                        or 'почта' in line.text.lower() or 'почты' in line.text.lower()):
                    contacts = contacts + ' ' + normalise_str(line.text)

                if line.find('a') and 'mailto' in line.find('a').get('href'):
                    contacts = contacts + ' ' + normalise_str(line.find('a').text)

                if not rinc:
                    rinc = True if 'ринц' in line.text.lower() else False

                if local and 'международн' in line.text.lower():
                    local = False

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
        print(f"Отказ по таймауту, конференция {n + 1} из {confs}, {url}", e)

def get_griver_path():
    path = 'chromedriver/'
    if system() == 'Windows':
        path = f'{path}win/chromedriver.exe'
    if system() == 'Linux':
        path = f'{path}linux/chromedriver'
    if system() == 'Darwin':
        path = f'{path}darwin/chromedriver'
    return path

def parser_mgppu(un_id, url, date_):
    try:
        options = webdriver.ChromeOptions()
        service = Service(executable_path=get_griver_path())
        driver = webdriver.Chrome(service=service, options=options)
        # driver.minimize_window()

        asyncio.run(make_queue_mgppu(driver, un_id, url, date_))

        driver.close()
        driver.quit()

        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_mgppu('mgppu', 'https://mgppu.ru/events', datetime.strptime('2023.01.01', '%Y.%m.%d')))

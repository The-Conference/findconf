from datetime import date
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
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


async def make_queue_msal(un_id, url, filter_date):
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            try:
                async with session.get(url=url, headers=headers, timeout=20) as response:
                    if response.status == 404:
                        print(f'{response.status} - Нет такой страницы {url}')
                        return
                    response_text = await response.text()
                    soup = BeautifulSoup(response_text, 'lxml')
                    # print(soup)
                    main_container = soup.find('div',
                                               class_='container mx-auto space-y-5 mb-5 md:space-y-5 xl:space-y-9 md:mb-5 '
                                                      'xl:mb-9 undefined')

                    pages = main_container.find('div', id='pagination').find_all('a')[-1].get('href').split('&')[-1] \
                        if main_container.find('div', id='pagination') else ''
                    pages = int(pages[pages.find('=') + 1:len(pages)]) if pages != '' else 1
                    pages = 2  # дальше второй страницы смысла идти нет
                    for page in range(1, pages + 1):
                        url_ = f'{url}&PAGEN_1={page}' if page > 1 else url
                        try:
                            async with session.get(url=url_, headers=headers) as response:
                                if response.status == 404:
                                    print(f'{response.status} - Нет такой страницы {url}')
                                    continue
                                response_text = await response.text()

                                print(f'{response.status} Обрабатываем страницу {page} из {pages}, {url_}')
                                soup = BeautifulSoup(response_text, 'lxml')
                                conf_block = soup.find('div',
                                                       class_='container mx-auto space-y-5 mb-5 md:space-y-5 xl:space-y-9 md:mb-5 '
                                                              'xl:mb-9 undefined').find_all('div',
                                                                                            class_='grid grid-cols-12 gap-5 md:gap-3 xl:gap-9')
                                for n, conf in enumerate(conf_block):
                                    title = conf.find('div',
                                                      class_='flex flex-col justify-between space-y-2 md:w-3/4').find(
                                        'a').get('title').strip()
                                    # print(title)
                                    conf_url = f"https://msal.ru{conf.find('div', class_='flex flex-col justify-between space-y-2 md:w-3/4').find('a').get('href').strip()}"
                                    # print(conf_url)
                                    task = asyncio.create_task(
                                        parser_msal_pages(session, un_id, conf_url, filter_date, n, page))
                                    tasks.append(task)
                                    # break
                        except asyncio.TimeoutError as e:
                            print(f'Отказ по таймауту, нет ответа {page} из {pages}, {url_}', e)
                        except Exception as e:
                            raise Exception(
                                f'Не удалось обработать ссылку {n} на странице {page} в {__name__} для {url_}\n{e}')

                    await asyncio.gather(*tasks)
            except asyncio.TimeoutError as e:
                print(f'Отказ по таймауту, нет ответа от {url}', e)
            except Exception as e:
                raise Exception(f'Не удалось получить данные в {__name__} для {url}\n{e}')
    except Exception as e:
        raise Exception(f'Не удалось обработать очередь для {__name__}\n{e}')


async def parser_msal_pages(session, un_id, url, filter_date, n, page):
    try:
        async with session.get(url=url, headers=headers, timeout=20) as response:
            if response.status == 404:
                print(f'{response.status} - Нет такой страницы {url}')
                return
            print(f'{response.status} Выполняется ссылка {n + 1} на странице {page}, {url}')
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'lxml')
            conf_block = soup.find('div', id='articleBody')
            conf_name = normalise_str(soup.find('h1', class_='font-medium text-2xl md:text-4xl lg:text-5xl md:w-3/4').text)
            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{url.split('/')[-2]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            un_name = normalise_str(
                soup.find('header', class_='md:sticky md:top-0 md:z-50').find('div', class_='text-xs pb-1 md:text-xl').text)
            un_name = un_name + ' ' + normalise_str(
                soup.find('header', class_='md:sticky md:top-0 md:z-50').find('div', class_='text-xs md:text-sm').text)
            conf_card_href = url

            lines = conf_block.find_all('p')
            conf_s_desc = normalise_str(lines[0].get_text(separator=" "))
            pre_header = soup.find('div', class_='flex items-center flex-wrap gap-2 pb-2').find_all('div',
                                                                                                    class_='text-sm mt-2')
            dates = list(find_date_in_string(pre_header[0].text))
            # print(dates)
            reg_date_begin = ''
            reg_date_end = ''

            conf_date_begin = str(dates[0].date()) if dates else ''
            conf_date_end = str(dates[-1].date()) if dates and dates[-1] else ''

            reg_href = ''
            conf_desc = ''
            org_name = ''
            themes = ''
            online = True if ('онлайн' in pre_header[1].text.lower() or 'гибридн' in pre_header[1].text.lower()) else False
            conf_href = ''
            offline = True if (
                        'оффлайн' in pre_header[1].text.lower() or 'гибридн' in pre_header[1].text.lower()) else False
            conf_address = ''
            contacts = ''
            rinc = False

            for line in lines:
                all_a = line.find_all('a')
                for a in all_a:
                    if reg_href == '' and ('регистрац' in a.text.lower() or 'регистр' in a.text.lower()):
                        reg_href = a.get('href')
                if reg_href == '' and ('регистрац' in line.text.lower() or 'зарегистр' in line.text.lower()):
                    reg_href = all_a[-1].get('href') if all_a else 'отсутствует'

                if org_name == '' and 'организатор' in line.text.lower():
                    org_name = normalise_str(line.get_text(separator=" "))
                if online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()
                               or 'ссылка' in line.text.lower()):
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'
                if offline and ('место' in line.text.lower() or 'адрес' in line.text.lower()):
                    conf_address = normalise_str(line.get_text(separator=" "))
                if ('телеф' in line.text.lower() or 'контакт' in line.text.lower() or 'mail' in line.text.lower()
                        or 'почта' in line.text.lower() or 'почты' in line.text.lower()):
                    contacts = contacts + ' ' + normalise_str(line.get_text(separator=" "))
                if line.find('a'):
                    for a in line.find_all('a'):
                        if 'mailto' in a.get('href'):
                            contacts = contacts + ' ' + normalise_str(a.text)

                if ('заявки' in line.text.lower() or 'принимаютс' in line.text.lower() or 'участие' in line.text.lower()
                    or 'регистрац' in line.text.lower() or 'регистрир' in line.text.lower()) and reg_date_begin == '':
                    reg_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                        list(find_date_in_string(line.text.lower())) else ''
                    reg_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                        len(list(find_date_in_string(line.text.lower()))) > 1 else ''

                if not rinc:
                    rinc = True if 'ринц' in line.text.lower() else False

            lines = conf_block.find('div',
                                    class_='space-y-1 flex flex-col text-xs md:text-base md:space-y-4 text-justify text-block').find_all()
            for line in lines:
                conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

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
                     'contacts': contacts.replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                     'rinc': rinc,
                     }
                )
    except asyncio.TimeoutError as e:
        print(f'Отказ по таймауту, ссылка {n + 1} на странице {page}, {url}', e)

def parser_msal(un_id, url, date_):
    try:
        asyncio.run(make_queue_msal(un_id, url, date_))
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_msal('msal', 'https://msal.ru/events/?arrFilter_182=34404265&arrFilter_67_MIN=1.01.2000'
                              '&arrFilter_67_MAX=28.02.2023&set_filter=%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C',
                      datetime.strptime('2023.01.01', '%Y.%m.%d')))

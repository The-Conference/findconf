from datetime import datetime
from celery import shared_task
import time

from .models import Conference
from .Parsers import parser_1spbgmu, parser_bstu, parser_linguanet, \
    parser_mgsu, parser_msal, parser_pstu, parser_s_vfu, parser_samsmu, \
    parser_spbgasu, parser_ssmu, parser_unecon, parser_almazovcentre, parser_kazangmu, \
    parser_gpmu, parser_mgou, parser_miet, parser_szgmu, parser_tusur, parser_uni_dubna, \
    parser_unitech_mo, parser_petrsu, parser_rzgmu


def save_conferences(lst):
    for conference in lst:
        if Conference.objects.filter(conf_id=conference["conf_id"]).exists():
            continue
        else:
            if conference["reg_date_begin"] == '':
                conference["reg_date_begin"] = None
            if conference["reg_date_end"] == '':
                conference["reg_date_end"] = None
            if conference["conf_date_begin"] == '':
                conference["conf_date_begin"] = None
            if conference["conf_date_end"] == '':
                conference["conf_date_end"] = None
            Conference.objects.create(
                conf_id=conference["conf_id"],
                hash=conference["hash"],
                un_name=conference["un_name"],
                local=conference["local"],
                reg_date_begin=datetime.strptime(conference["reg_date_begin"], '%Y-%m-%d') \
                if conference["reg_date_begin"] is not None else None,
                reg_date_end=datetime.strptime(conference["reg_date_end"], '%Y-%m-%d') \
                if conference["reg_date_end"] is not None else None,
                conf_date_begin=datetime.strptime(conference["conf_date_begin"], '%Y-%m-%d') \
                if conference["conf_date_begin"] is not None else None,
                conf_date_end=datetime.strptime(conference["conf_date_end"], '%Y-%m-%d') \
                if conference["conf_date_end"] is not None else None,
                conf_card_href=conference["conf_card_href"],
                reg_href=conference["reg_href"],
                conf_name=conference["conf_name"],
                conf_s_desc=conference["conf_s_desc"],
                conf_desc=conference["conf_desc"],
                org_name=conference["org_name"],
                themes=conference["themes"],
                online=conference["online"],
                conf_href=conference["conf_href"],
                offline=conference["offline"],
                conf_address=conference["conf_address"],
                contacts=conference["contacts"],
                rinc=conference["rinc"],
                data=conference
            )


def run_parser(func):
    parsing_results = []
    try:
        parsing_results.extend(func)
    except Exception as e:
        print(e)
    time.sleep(10)
    print(len(parsing_results))
    try:
        save_conferences(parsing_results)
    except Exception as e:
        print(e)


@shared_task
def parser1():
    run_parser(parser_1spbgmu.parser_1spbgmu(
        '1spbgmu', 'https://www.1spbgmu.ru/nauka/konferentsii',
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser2.apply_async()


@shared_task
def parser2():
    run_parser(parser_almazovcentre.parser_almazovcentre(
        'almazovcentre', ['http://www.almazovcentre.ru/?cat=5'],
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser3.apply_async()


@shared_task
def parser3():
    run_parser(parser_bstu.parser_bstu(
        'bstu', ['https://conf.bstu.ru/conf_bstu'], datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser4.apply_async()


@shared_task
def parser4():
    run_parser(parser_gpmu.parser_gpmu(
        'gpmu', ['https://gpmu.org/science/conference/'],
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser5.apply_async()


@shared_task
def parser5():
    run_parser(parser_kazangmu.parser_kazangmu(
        'kazangmu', ['https://kazangmu.ru/science-and-innovation/konferentsii-v-rossii'],
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser6.apply_async()


@shared_task
def parser6():
    run_parser(parser_linguanet.parser_linguanet(
        'linguanet',
        ['https://www.linguanet.ru/science/konferentsii-i-seminary/',
        'https://www.linguanet.ru/science/konferentsii-i-seminary/konferentsii-v-drugikh-vuzakh/'],
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser7.apply_async()


@shared_task
def parser7():
    run_parser(parser_mgou.parser_mgou(
        'mgou', ['https://mgou.ru/ru/rubric/science/organizatsiya-nauchno-issledovatelskoj-deyatelnosti-mgou-2'],
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser8.apply_async()


@shared_task
def parser8():
    run_parser(parser_mgsu.parser_mgsu(
        'mgsu', 'https://mgsu.ru/news/announce/',
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser9.apply_async()


@shared_task
def parser9():
    run_parser(parser_miet.parser_miet(
        'miet', 'https://miet.ru',
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser10.apply_async()


@shared_task
def parser10():
    run_parser(parser_msal.parser_msal(
        'msal', 'https://msal.ru/events/?arrFilter_182=34404265&arrFilter_67_MIN=1.01.2000&arrFilter_67_MAX=28.02.2023&set_filter=%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C',
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser11.apply_async()


@shared_task
def parser11():
    run_parser(parser_pstu.parser_pstu(
        'pstu', 'https://pstu.ru/tag_news/', datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser12.apply_async()


@shared_task
def parser12():
    run_parser(parser_s_vfu.parser_s_vfu(
        's-vfu', ['https://www.s-vfu.ru/conference/'],
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser13.apply_async()


@shared_task
def parser13():
    run_parser(parser_samsmu.parser_samsmu(
        'samsmu', ['https://samsmu.ru/events'],
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser14.apply_async()


@shared_task
def parser14():
    run_parser(parser_spbgasu.parser_spbgasu(
        'spbgasu',
        ['https://www.spbgasu.ru/Nauchnaya_i_innovacionnaya_deyatelnost/Konferencii_i_seminary/'],
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser15.apply_async()


@shared_task
def parser15():
    run_parser(parser_ssmu.parser_ssmu(
        'ssmu', ['https://ssmu.ru/ru/nauka/activity/'],
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser16.apply_async()


@shared_task
def parser16():
    run_parser(parser_szgmu.parser_szgmu(
        'szgmu', 'https://szgmu.ru/modules/ev/index.php',
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser17.apply_async()


@shared_task
def parser17():
    run_parser(parser_tusur.parser_tusur(
        'tusur', 'https://tusur.ru/ru/novosti-i-meropriyatiya/anonsy-meropriyatiy',
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser18.apply_async()


@shared_task
def parser18():
    run_parser(parser_unecon.parser_unecon(
        'unecon', 'https://unecon.ru/wp-json/unecon/v1/announcements',
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser19.apply_async()


@shared_task
def parser19():
    run_parser(parser_uni_dubna.parser_uni_dubna(
        'uni_dubna', ['https://conf.uni-dubna.ru/Home/Conferences'],
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser20.apply_async()


@shared_task
def parser20():
    run_parser(parser_unitech_mo.parser_unitech_mo(
        'unitech_mo',
        ['https://unitech-mo.ru/science/research-activities-/youth-science/calendar-of-scientific-events/',
        'https://unitech-mo.ru/science/postgraduate-study/scientific-practical-conference/',
        'https://unitech-mo.ru/announcement/'],
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser21.apply_async()


@shared_task
def parser21():
    run_parser(parser_petrsu.parser_petrsu(
        'petrsu', ['https://conf.petrsu.ru/index.php',
        'https://petrsu.ru/page/education/school/project/konferentsii-i-konkursy'],
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser22.apply_async()


@shared_task
def parser22():
    run_parser(parser_rzgmu.parser_rzgmu(
        'rzgmu', 'https://rzgmu.ru/actions/',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    # parser23.apply_async()

from datetime import datetime
from celery import shared_task
import time

from .models import Conference
from .Parsers import parser_1spbgmu, parser_bstu, parser_linguanet, \
    parser_mgsu, parser_msal, parser_pstu, parser_s_vfu, parser_samsmu, \
    parser_spbgasu, parser_ssmu, parser_unecon, parser_almazovcentre, parser_kazangmu, \
    parser_gpmu, parser_mgou, parser_miet, parser_szgmu, parser_tusur, parser_uni_dubna, \
    parser_unitech_mo, parser_petrsu, parser_rzgmu, parser_asou_mo, parser_bashgmu, \
    parser_cchgeu, parser_donstu, parser_ggtu, parser_gubkin, parser_kai, parser_kbsu, \
    parser_kurskmed, parser_mgppu, parser_mgpu, parser_mrsu, parser_narfu, parser_pimunn, \
    parser_rosnou, parser_tsuab, parser_tyuiu, parser_volsu, parser_vstu, parser_mpgu, \
    parser_bsuedu, parser_mpei, parser_sfu_kras, parser_timacad


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
            if not conference["conf_date_begin"]:
                conference["conf_date_begin"] = '2023-01-01'
            Conference.objects.create(
                generate_conf_id=False,
                conf_id=conference["conf_id"],
                hash=conference["hash"][:450],
                un_name=conference["un_name"][:450],
                local=conference["local"],
                reg_date_begin=datetime.strptime(conference["reg_date_begin"], '%Y-%m-%d') \
                if conference["reg_date_begin"] is not None else None,
                reg_date_end=datetime.strptime(conference["reg_date_end"], '%Y-%m-%d') \
                if conference["reg_date_end"] is not None else None,
                conf_date_begin=datetime.strptime(conference["conf_date_begin"], '%Y-%m-%d') \
                if conference["conf_date_begin"] is not None else None,
                conf_date_end=datetime.strptime(conference["conf_date_end"], '%Y-%m-%d') \
                if conference["conf_date_end"] is not None else None,
                conf_card_href=conference["conf_card_href"][:450],
                reg_href=conference["reg_href"][:450],
                conf_name=conference["conf_name"],
                conf_s_desc=conference["conf_s_desc"],
                conf_desc=conference["conf_desc"],
                org_name=conference["org_name"],
                themes=conference["themes"],
                online=conference["online"],
                conf_href=conference["conf_href"][:450],
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
    parser23.apply_async()


@shared_task
def parser23():
    run_parser(parser_asou_mo.parser_asou_mo(
        'asou_mo', 'https://asou-mo.ru/events/announce/',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser24.apply_async()


@shared_task
def parser24():
    run_parser(parser_bashgmu.parser_bashgmu(
        'bashgmu', 'https://bashgmu.ru/science_and_innovation/konferentsii/',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser25.apply_async()


@shared_task
def parser25():
    run_parser(parser_cchgeu.parser_cchgeu(
        'cchgeu', 'https://cchgeu.ru/science/info/konferentsii',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser26.apply_async()


@shared_task
def parser26():
    run_parser(parser_donstu.parser_donstu(
        'donstu', 'https://donstu.ru/events/',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser27.apply_async()


@shared_task
def parser27():
    run_parser(parser_ggtu.parser_ggtu(
        'ggtu', ['https://www.ggtu.ru/index.php?option=com_content&view=article&id=9230&Itemid=810'],
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser28.apply_async()


@shared_task
def parser28():
    run_parser(parser_gubkin.parser_gubkin(
        'gubkin', 'https://conf.gubkin.ru/conferences/',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser29.apply_async()


@shared_task
def parser29():
    run_parser(parser_kai.parser_kai(
        'kai', 'https://kai.ru/science/events',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser30.apply_async()


@shared_task
def parser30():
    run_parser(parser_kbsu.parser_kbsu(
        'kbsu', ['https://kbsu.ru/nauchnye-konferencii/'],
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser31.apply_async()


@shared_task
def parser31():
    run_parser(parser_kurskmed.parser_kurskmed(
        'kurskmed', ['https://kurskmed.com/department/KSMU_announcements_events/news'],
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser32.apply_async()


@shared_task
def parser32():
    run_parser(parser_mgppu.parser_mgppu(
        'mgppu', 'https://mgppu.ru/events',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser33.apply_async()


@shared_task
def parser33():
    run_parser(parser_mgpu.parser_mgpu(
        'mgpu', 'https://www.mgpu.ru/calendar/',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser34.apply_async()


@shared_task
def parser34():
    run_parser(parser_mrsu.parser_mrsu(
        'mrsu', 'https://mrsu.ru/ru/sci/conferences/',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser35.apply_async()


@shared_task
def parser35():
    run_parser(parser_narfu.parser_narfu(
        'narfu', 'https://narfu.ru/science/nauchnye-meropriyatiya/',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser36.apply_async()


@shared_task
def parser36():
    run_parser(parser_pimunn.parser_pimunn(
        'pimunn', 'https://feeds.tildacdn.com/api/getfeed/',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser37.apply_async()


@shared_task
def parser37():
    run_parser(parser_rosnou.parser_rosnou(
        'rosnou', 'https://rosnou.ru/nauka/conferences/',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser38.apply_async()


@shared_task
def parser38():
    run_parser(parser_tsuab.parser_tsuab(
        'tsuab', 'https://tsuab.ru/events/?SECTION_ID=264',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser39.apply_async()


@shared_task
def parser39():
    run_parser(parser_tyuiu.parser_tyuiu(
        'tyuiu', ['https://www.tyuiu.ru/1028-2/konferentsii-2/'],
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser40.apply_async()


@shared_task
def parser40():
    run_parser(parser_volsu.parser_volsu(
        'volsu', 'https://volsu.ru/archive_ad.php',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser41.apply_async()


@shared_task
def parser41():
    run_parser(parser_vstu.parser_vstu(
        'vstu', ['https://www.vstu.ru/nauka/konferentsii'],
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser42.apply_async()


@shared_task
def parser42():
    run_parser(parser_mpgu.parser_mpgu(
        'mpgu', 'http://mpgu.su/category/anonsyi',
        datetime.strptime('2023.01.01', '%Y.%m.%d'))
    )
    parser43.apply_async()


@shared_task
def parser43():
    run_parser(parser_bsuedu.parser_bsuedu('bsuedu', 'https://www.bsuedu.ru/bsu/science/meropr/',
                                           datetime.strptime('2023.01.01', '%Y.%m.%d')))
    parser44.apply_async()


@shared_task
def parser44():
    run_parser(parser_mpei.parser_mpei(
        'mpei', ['https://mpei.ru/Science/ScientificEvents/Pages/default.aspx'],
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser45.apply_async()


@shared_task
def parser45():
    run_parser(parser_sfu_kras.parser_sfu_kras(
        'sfu-kras', 'https://conf.sfu-kras.ru/',
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    parser46.apply_async()


@shared_task
def parser46():
    run_parser(parser_timacad.parser_timacad(
        'timacad', 'https://www.timacad.ru/science/konferentsii',
        datetime.strptime('2023.01.01', '%Y.%m.%d')
    ))
    # parser47.apply_async()

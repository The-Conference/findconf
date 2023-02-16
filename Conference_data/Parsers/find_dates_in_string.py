import datefinder


def normalise_str(string):
    string = ' '.join(string.split())
    return string.strip().replace('&nbsp;', ' ').replace('\xa0', ' ').replace('\r', ''). \
        replace('\n', '').replace('\t', '')


def find_date_in_string(str_):
    names = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    names2 = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
             'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
    nums = ['january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december']
    months = dict(zip(nums, names))
    months2 = dict(zip(nums, names2))
    str_ = str_.replace('–', '-')
    words = str_.split()
    # print(str_)
    # print(words)
    dates = False
    c_ = False
    place_ = -1
    if words[0].lower() == 'с':
        dates = True
        c_ = True
    for n, word in enumerate(words):
        if not dates and '-' in word:
            try:
                s = int(word[:word.find('-')])
                words[n] = words[n].replace('-', ' и ')
                place_ = n
                dates = True
            except:
                continue
        if word in months.values():
            words[n] = [key for key, value in months.items() if word in value][0]
        elif word in months2.values():
            words[n] = [key for key, value in months2.items() if word in value][0]
    words = ' '.join(words)
    # print(words, place_)
    # print(dates, c_)
    words = words.split()
    # print(words)
    if dates and not c_:
        try:
            words.insert(place_+1, words[place_+3])
            words.insert(place_ + 2, words[place_ + 5])
        except:
            # print('Нет месяца или года')
            words = words
    if dates and c_:
        try:
            words.insert(2, words[4])
            words.insert(3, words[6])
        except:
            # print('Нет месяца или года')
            words = words

    str_ = ' '.join(words)
    # print(str_)
    return list(datefinder.find_dates(str_.replace('-', ' и ')))

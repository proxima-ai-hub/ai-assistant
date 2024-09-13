import string

punctuation = string.punctuation.replace('-', '')

dict_glossary = {'лк': 'личный кабинет',
                 'бир': 'беременность и роды',
                 'зп': 'зарплата',
                 'ндфл': 'налог на доходы физических лиц',
                 'стд': 'срочный трудовой договор',
                 'тк': 'трудовая книжка',
                 'ао': 'авансовый отчет',
                 'sla': 'сроки',
                 'эцп': 'электронная цифровая подпись',
                 'кр': 'кадровый резерв',
                 'тк рф': 'трудовой кодекс',
                 'рф': 'российская федерация',
                 'мчд': 'машиночитаемая доверенность',
                 'ур': 'удалённая работа',
                 'дмс': 'добровольное медицинское страхование',
                 'дм': 'директор магазина',
                 'дмп': 'директор магазина партнёр',
                 'здм': 'заместитель директора магазина',
                 'адм': 'ассистент директора магазина',
                 'есп': 'единая система подбора',
                 'эп': 'электронная подпись',
                 'з/п': 'зарплата',
                 'дк': 'директор кластеров',
                 'мп': 'мобильное приложение',
                 'lk': 'личный кабинет',
                 'бл': 'больничный лист',
                 'бс': 'отпуск без содержания',
                 'укэп': 'усиленная квалифицированная электронная подпись',
                 'унэп': 'усиленная неквалифицированная электронная подпись',
                 'фл': 'физическое лицо'}

glossary = dict_glossary.keys()
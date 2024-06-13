import requests
import time
import json
import datetime
import concurrent.futures

bug_hunter = ''

def lsc_check(api_url, api_key, service, max_price, max_threads):

    print('params = ', api_url, api_key, service, max_price, max_threads)
    time.sleep(5)


    global bug_hunter

    API_URL = api_url
    API_KEY = api_key
    SERVICE = service
    MAX_PRICE = max_price
    log_file = f'LiveSmsChecker_Log_{datetime.datetime.now().strftime(".""(""%d""-""%m""-""%Y""(""%H""_""%M""_""%S"")"")")}.txt'
    MAX_THREADS = max_threads

    bug_hunter = ''

    # Словарь с названиями стран
    countries_dict = {
        0: "Россия",
        1: "Украина",
        2: "Казахстан",
        3: "Китай",
        4: "Филиппины",
        5: "Мьянма",
        6: "Индонезия",
        7: "Малайзия",
        8: "Кения",
        9: "Танзания",
        10: "Вьетнам",
        11: "Кыргызстан",
        12: "США (виртуальные)",
        13: "Израиль",
        14: "Гонконг",
        15: "Польша",
        16: "Англия",
        17: "Мадагаскар",
        18: "Дем. Конго",
        19: "Нигерия",
        20: "Макао",
        21: "Египет",
        22: "Индия",
        23: "Ирландия",
        24: "Камбоджа",
        25: "Лаос",
        26: "Гаити",
        27: "Котд'Ивуар",
        28: "Гамбия",
        29: "Сербия",
        30: "Йемен",
        31: "ЮАР",
        32: "Румыния",
        33: "Колумбия",
        34: "Эстония",
        35: "Азербайджан",
        36: "Канада",
        37: "Марокко",
        38: "Гана",
        39: "Аргентина",
        40: "Узбекистан",
        41: "Камерун",
        42: "Чад",
        43: "Германия",
        44: "Литва",
        45: "Хорватия",
        46: "Швеция",
        47: "Ирак",
        48: "Нидерланды",
        49: "Латвия",
        50: "Австрия",
        51: "Беларусь",
        52: "Таиланд",
        53: "Сауд.Аравия",
        54: "Мексика",
        55: "Тайвань",
        56: "Испания",
        57: "Иран",
        58: "Алжир",
        59: "Словения",
        60: "Бангладеш",
        61: "Сенегал",
        62: "Турция",
        63: "Чехия",
        64: "Шри-Ланка",
        65: "Перу",
        66: "Пакистан",
        67: "Новая Зеландия",
        68: "Гвинея",
        69: "Мали",
        70: "Венесуэла",
        71: "Эфиопия",
        72: "Монголия",
        73: "Бразилия",
        74: "Афганистан",
        75: "Уганда",
        76: "Ангола",
        77: "Кипр",
        78: "Франция",
        79: "Папуа-Новая Гвинея",
        80: "Мозамбик",
        81: "Непал",
        82: "Бельгия",
        83: "Болгария",
        84: "Венгрия",
        85: "Молдова",
        86: "Италия",
        87: "Парагвай",
        88: "Гондурас",
        89: "Тунис",
        90: "Никарагуа",
        91: "Тимор-Лесте",
        92: "Боливия",
        93: "Коста Рика",
        94: "Гватемала",
        95: "ОАЭ",
        96: "Зимбабве",
        97: "Пуэрто-Рико",
        98: "Судан",
        99: "Того",
        100: "Кувейт",
        101: "Сальвадор",
        102: "Ливия",
        103: "Ямайка",
        104: "Тринидад и Тобаго",
        105: "Эквадор",
        106: "Свазиленд",
        107: "Оман",
        108: "Босния и Герцеговина",
        109: "Доминиканская Республика",
        110: "Сирия",
        111: "Катар",
        112: "Панама",
        113: "Куба",
        114: "Мавритания",
        115: "Сьерра-Леоне",
        116: "Иордания",
        117: "Португалия",
        118: "Барбадос",
        119: "Бурунди",
        120: "Бенин",
        121: "Бруней",
        122: "Багамы",
        123: "Ботсвана",
        124: "Белиз",
        125: "ЦАР",
        126: "Доминика",
        127: "Гренада",
        128: "Грузия",
        129: "Греция",
        130: "Гвинея-Бисау",
        131: "Гайана",
        132: "Исландия",
        133: "Коморы",
        134: "Сент-Китс и Невис",
        135: "Либерия",
        136: "Лесото",
        137: "Малави",
        138: "Намибия",
        139: "Нигер",
        140: "Руанда",
        141: "Словакия",
        142: "Суринам",
        143: "Таджикистан",
        144: "Монако",
        145: "Бахрейн",
        146: "Реюньон",
        147: "Замбия",
        148: "Армения",
        149: "Сомали",
        150: "Конго",
        151: "Чили",
        152: "Буркина-Фасо",
        153: "Ливан",
        154: "Габон",
        155: "Албания",
        156: "Уругвай",
        157: "Маврикий",
        158: "Бутан",
        159: "Мальдивы",
        160: "Гваделупа",
        161: "Туркменистан",
        162: "Французская Гвиана",
        163: "Финляндия",
        164: "Сент-Люсия",
        165: "Люксембург",
        166: "Сент-Винсент и Гренадин",
        167: "Экваториальная Гвинея",
        168: "Джибути",
        169: "Антигуа и Барбуда",
        170: "Острова Кайман",
        171: "Черногория",
        172: "Дания",
        173: "Швейцария",
        174: "Норвегия",
        175: "Австралия",
        176: "Эритрея",
        177: "Южный Судан",
        178: "Сан-Томе и Принсипи",
        179: "Аруба",
        180: "Монтсеррат",
        181: "Ангилья",
        183: "Северная Македония",
        184: "Республика Сейшелы",
        185: "Новая Каледония",
        186: "Кабо-Верде",
        187: "США",
        189: "Фиджи",
        190: "Палестина",
        191: "Япония",
        192: "Южная Корея",
        193: "Мальта",
        194: "Науру",
        195: "Мартиника",
        196: "Сингапур",
        201: "Гибралтар"
    }

    def get_number(country):
        global bug_hunter
        params = {
            "api_key": API_KEY,
            "action": "getNumber",
            "service": SERVICE,
            "country": country,
            "maxPrice": MAX_PRICE
        }
        try:
            response = requests.get(API_URL, params=params)
            if response.status_code == 200:
                data = response.text.strip()
                if data.startswith("ACCESS_NUMBER"):
                    return country, data.split(":")[2]
                else:
                    print(f"Error response for country {country}: {data}")
                    bug_hunter += f"Error response for country {country}: {data}"
            else:
                print(f"Error status code for country {country}: {response.status_code}")
                bug_hunter += f"Error status code for country {country}: {response.status_code}"
        except requests.exceptions.RequestException as e:

            print(f"Error making request for country {country}: {e}")
            bug_hunter += f"Error making request for country {country}: {e}"

        return country, None

    def process_country(country):
        global bug_hunter
        numbers = []
        for _ in range(2):
            country, number = get_number(country)
            if number:
                numbers.append(number)
            time.sleep(1)
        if len(numbers) == 2:
            return country
        return None

    def deploy():
        global bug_hunter
        countries = range(1, 202)
        successful_countries = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = {executor.submit(process_country, country): country for country in countries}
            for future in concurrent.futures.as_completed(futures):
                country = futures[future]
                try:
                    result = future.result()
                    if result:
                        successful_countries.append(result)
                except Exception as e:
                    print(f"Error processing country {country}: {e}")
                    bug_hunter += f"Error processing country {country}: {e}"
                print(f"Processed country {country}")
                bug_hunter += f"Processed country {country}"

        if successful_countries:
            print(f'-----------------------------------------')
            for country in successful_countries:
                country_name = countries_dict.get(country, "Неизвестная страна")
                print(f'У этой страны есть номера: {country} ({country_name})')
                bug_hunter += f'У этой страны есть номера: {country} ({country_name})'
            print(f'-----------------------------------------')

            try:
                result = ''
                with open(log_file, "w") as file:
                    for country in successful_countries:
                        country_name = countries_dict.get(country, "Неизвестная страна")
                        file.write(f'У этой страны есть номера: {country} ({country_name})\n')
                        result += f'У этой страны есть номера: {country} ({country_name})\n'
                print(f"Скрипт завершен. Результаты сохранены в файле {log_file}.")
                return result + "Скрипт завершен. Результаты сохранены в файле", log_file
            except IOError as e:
                print(f"Ошибка при сохранении файла {log_file}: {e}")
                return None, None
        else:
            print("Скрипт завершен. Не удалось получить номера ни для одной страны.")
            return "Скрипт завершен. Не удалось получить номера ни для одной страны.", None


    r, f =  deploy()
    print(bug_hunter[:500])
    if 'BAD_SERVICE' in bug_hunter:
        return 'bad', 'bad'
    return r, f

import csv
from bs4 import BeautifulSoup
import requests


def _write_to_csv(filename, data, delimiter=","):
    with open(filename, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=delimiter)
        writer.writerows(data)


def _add_to_csv(filename, data, delimiter=","):
    with open(filename, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=delimiter)
        writer.writerows(data)


def _read_from_csv(filename):
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        data = []
        for row in reader:
            data.append(row)
        return data


def _try_to_find_info_used_auto(soup, params_first, params_second):
    try:
        return soup.find(**params_first).findNext(**params_second).text
    except AttributeError:
        return 'None'


def _try_to_find_info_new_auto(soup, params_first, params_second):
    try:
        return soup.find(**params_first).findNext(**params_second).text
    except AttributeError:
        return 'For more information contact the dealership'


def parse_page():
    response = requests.get('https://auto.ria.com/uk/legkovie/?page=1')
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    last_page = soup.findAll('a', class_='page-link')
    last_page = last_page[len(last_page) - 2].text.replace(' ', '')

    _write_to_csv('page.csv', [['last_page'], [last_page]])


def parse_id_announcements():
    _write_to_csv('id_announcement.csv', [['id_auto', 'page_url'], ])

    for page in range(int(_read_from_csv('page.csv')[1][0])):
        response = requests.get(f'https://auto.ria.com/uk/legkovie/?page={page + 1}')
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        announcements = soup.findAll('section', class_='ticket-item')
        if not announcements:
            break

        for announcement in announcements:
            if not announcement.find('i', class_='icon-sold-out'):
                id_auto = announcement.find("div", class_="hide").get("data-id")
                page_url = announcement.find("a", class_="m-link-ticket").get("href")
                _add_to_csv('id_announcement.csv', [[id_auto, page_url], ])


def _parse_used_auto(soup, link):
    model = soup.find('h1', class_='head').get('title')

    price = soup.find('div', class_='price_value').findNext('strong').text

    body_type = soup.find('div', class_='technical-info', id="description_v3") \
        .findNext('dd').text

    mileage = _try_to_find_info_used_auto(soup=soup,
                                          params_first={'name': 'span', 'class_': 'label', 'text': 'Пробіг'},
                                          params_second={'name': 'span', 'class_': 'argument'})

    engine = _try_to_find_info_used_auto(soup=soup,
                                         params_first={'name': 'span', 'class_': 'label', 'text': 'Двигун'},
                                         params_second={'name': 'span', 'class_': 'argument'})

    transmission = _try_to_find_info_used_auto(soup=soup,
                                               params_first={'name': 'span', 'class_': 'label',
                                                             'text': 'Коробка передач'},
                                               params_second={'name': 'span', 'class_': 'argument'})

    wheel_drive = _try_to_find_info_used_auto(soup=soup,
                                              params_first={'name': 'span', 'class_': 'label', 'text': 'Привід'},
                                              params_second={'name': 'span', 'class_': 'argument'})

    color = _try_to_find_info_used_auto(soup=soup,
                                        params_first={'name': 'span', 'class_': 'label', 'text': 'Колір'},
                                        params_second={'name': 'span', 'class_': 'argument'})

    description = _try_to_find_info_used_auto(soup=soup,
                                              params_first={'name': 'dd', 'class_': 'additional-data show-line'},
                                              params_second={'name': 'div', 'id': 'fore_info', 'class_': 'boxed'})

    traffic_accident = _try_to_find_info_used_auto(soup=soup,
                                                   params_first={'name': 'span', 'class_': 'label', 'title': 'Скрыть',
                                                                 'text': 'Участь в ДТП'},
                                                   params_second={'name': 'span', 'class_': 'argument'})

    paintwork = _try_to_find_info_used_auto(soup=soup,
                                            params_first={'name': 'span', 'class_': 'label', 'title': 'Скрыть',
                                                          'text': 'Лакофарбове покриття'},
                                            params_second={'name': 'span', 'class_': 'argument'})

    technical_condition = _try_to_find_info_used_auto(soup=soup,
                                                      params_first={'name': 'span', 'class_': 'label',
                                                                    'title': 'Скрыть',
                                                                    'text': 'Технічний стан'},
                                                      params_second={'name': 'span', 'class_': 'argument'})

    condition = _try_to_find_info_used_auto(soup=soup,
                                            params_first={'name': 'span', 'class_': 'label', 'title': 'Скрыть',
                                                          'text': 'Стан'},
                                            params_second={'name': 'span', 'class_': 'argument'})

    security = _try_to_find_info_used_auto(soup=soup,
                                           params_first={'name': 'span', 'class_': 'label', 'title': 'Скрыть',
                                                         'text': 'Безпека'},
                                           params_second={'name': 'span', 'class_': 'argument'})

    comfort = _try_to_find_info_used_auto(soup=soup,
                                          params_first={'name': 'span', 'class_': 'label', 'title': 'Скрыть',
                                                        'text': 'Комфорт'},
                                          params_second={'name': 'span', 'class_': 'argument'})

    multimedia = _try_to_find_info_used_auto(soup=soup,
                                             params_first={'name': 'span', 'class_': 'label', 'title': 'Скрыть',
                                                           'text': 'Мультимедіа'},
                                             params_second={'name': 'span', 'class_': 'argument'})

    other = _try_to_find_info_used_auto(soup=soup,
                                        params_first={'name': 'span', 'class_': 'label', 'title': 'Скрыть',
                                                      'text': 'Інше'},
                                        params_second={'name': 'span', 'class_': 'argument'})

    car_details = [model, price, body_type, mileage, engine, transmission, wheel_drive, color,
                   description, traffic_accident, paintwork, technical_condition, condition,
                   security, comfort, multimedia, other, link]

    return car_details


def _parse_new_auto(soup: BeautifulSoup, link):
    model = soup.find('h1', class_='auto-head_title bold mb-15').text

    price = _try_to_find_info_new_auto(soup=soup,
                                       params_first={'name': 'section', 'class_': 'price mb-15 mhide'},
                                       params_second={'name': 'div', 'title': 'Остаточну вартість уточнюйте у дилера'})

    body_type = soup.find('div', class_='mb-15').findNext('div', class_='mb-15') \
        .findNext('div', class_='mb-15').text

    mileage = '0'

    engine = _try_to_find_info_new_auto(soup=soup,
                                        params_first={'name': 'dl', 'class_': 'defines_list mb-15 unstyle'},
                                        params_second={'name': 'dd', 'class_': 'defines_list_value'})

    transmission = _try_to_find_info_new_auto(soup=soup,
                                              params_first={'name': 'dt', 'class_': 'defines_list_title',
                                                            'text': 'Коробка передач'},
                                              params_second={'name': 'dd', 'class_': 'defines_list_value'})

    wheel_drive = _try_to_find_info_new_auto(soup=soup,
                                             params_first={'name': 'dt', 'class_': 'defines_list_title',
                                                           'text': 'Привід'},
                                             params_second={'name': 'dd', 'class_': 'defines_list_value'})

    color = _try_to_find_info_new_auto(soup=soup,
                                       params_first={'name': 'dt', 'class_': 'defines_list_title color',
                                                     'text': 'Колір кузова'},
                                       params_second={'name': 'dd', 'class_': 'defines_list_value color'})

    description = _try_to_find_info_new_auto(soup=soup,
                                             params_first={'name': 'dt', 'class_': 'defines_list_title',
                                                           'text': 'Коментар автосалону'},
                                             params_second={'name': 'dd', 'class_': 'defines_list_value comment'})

    traffic_accident = 'No'

    paintwork = 'New'

    technical_condition = 'New'

    condition = 'New'

    security = 'For more information contact the dealership'

    comfort = 'For more information contact the dealership'

    multimedia = 'For more information contact the dealership'

    other = 'For more information contact the dealership'

    car_details = [model, price, body_type, mileage, engine, transmission, wheel_drive, color,
                   description, traffic_accident, paintwork, technical_condition, condition,
                   security, comfort, multimedia, other, link]

    return car_details


def parse_detail_announcement():
    _write_to_csv('detail_announcement.csv',
                  [['model', 'price', 'body_type', 'mileage', 'engine', 'transmission', 'wheel_drive', 'color',
                    'description', 'traffic_accident', 'paintwork', 'technical_condition', 'condition',
                    'security', 'comfort', 'multimedia', 'other', 'link'], ])

    for announcement in _read_from_csv('id_announcement.csv')[1:]:
        responce = requests.get(announcement[1])
        responce.raise_for_status()
        soup = BeautifulSoup(responce.content, 'lxml')
        link = responce.url
        if link.find('https://auto.ria.com/uk/newauto/'):
            car_details = _parse_used_auto(soup, link)
        else:
            car_details = _parse_new_auto(soup, link)
        _add_to_csv('detail_announcement.csv', [car_details, ])


parse_page()
parse_id_announcements()
parse_detail_announcement()

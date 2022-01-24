import csv
from bs4 import BeautifulSoup
import requests


def write_to_csv(filename, data, delimiter=","):
    with open(filename, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=delimiter)
        writer.writerows(data)


def add_to_csv(filename, data, delimiter=","):
    with open(filename, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=delimiter)
        writer.writerows(data)


def read_from_csv(filename):
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        data = []
        for row in reader:
            data.append(row)
        return data


def parse_page():
    response = requests.get('https://auto.ria.com/uk/legkovie/?page=1')
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    last_page = soup.findAll('a', class_='page-link')
    last_page = last_page[len(last_page) - 2].text.replace(' ', '')

    write_to_csv('page.csv', [['last_page'], [last_page]])


def parse_id_announcements():
    write_to_csv('id_announcement.csv', [['id_auto', 'page_url'], ])

    for page in range(int(read_from_csv('page.csv')[1][0])):
        response = requests.get(f'https://auto.ria.com/uk/legkovie/?page={page + 1}')
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        announcements = soup.findAll('section', class_='ticket-item')
        if not announcements:
            break

        for announcement in announcements:
            id_auto = announcement.find("div", class_="hide").get("data-id")
            page_url = announcement.find("a", class_="m-link-ticket").get("href")
            add_to_csv('id_announcement.csv', [[id_auto, page_url], ])


def parse_used_auto(soup: BeautifulSoup, link):
    model = soup.find('h1', class_='head').get('title')

    price = soup.find('div', class_='price_value').findNext('strong').text

    body_type = soup.find('div', class_='technical-info', id="description_v3")\
        .findNext('dd').text

    try:
        mileage = soup.find('span', class_='label', text='Пробіг')\
            .findNext('span', class_='argument').text
    except AttributeError:
        mileage = 'None'

    try:
        engine = soup.find('span', class_='label', text='Двигун') \
            .findNext('span', class_='argument').text
    except AttributeError:
        engine = 'None'

    try:
        transmission = soup.find('span', class_='label', text='Коробка передач') \
            .findNext('span', class_='argument').text
    except AttributeError:
        transmission = 'None'

    try:
        wheel_drive = soup.find('span', class_='label', text='Привід') \
            .findNext('span', class_='argument').text
    except AttributeError:
        wheel_drive = 'None'

    try:
        color = soup.find('span', class_='label', text='Колір') \
            .findNext('span', class_='argument').text
    except AttributeError:
        color = 'None'

    try:
        description = soup.find('dd', class_='additional-data show-line') \
            .findNext('div', id='fore_info', class_='boxed').text
    except AttributeError:
        description = 'None'

    try:
        traffic_accident = soup.find('span', class_='label', title='Скрыть', text='Участь в ДТП') \
            .findNext('span', class_='argument').text
    except AttributeError:
        traffic_accident = 'None'

    try:
        paintwork = soup.find('span', class_='label', title='Скрыть', text='Лакофарбове покриття') \
            .findNext('span', class_='argument').text
    except AttributeError:
        paintwork = 'None'

    try:
        technical_condition = soup.find('span', class_='label', title='Скрыть', text='Технічний стан') \
            .findNext('span', class_='argument').text
    except AttributeError:
        technical_condition = 'None'

    try:
        condition = soup.find('span', class_='label', title='Скрыть', text='Стан') \
            .findNext('span', class_='argument').text
    except AttributeError:
        condition = 'None'

    try:
        security = soup.find('span', class_='label', title='Скрыть', text='Безпека') \
            .findNext('span', class_='argument').text
    except AttributeError:
        security = "None"

    try:
        comfort = soup.find('span', class_='label', title='Скрыть', text='Комфорт') \
            .findNext('span', class_='argument').text
    except AttributeError:
        comfort = 'None'

    try:
        multimedia = soup.find('span', class_='label', title='Скрыть', text='Мультимедіа') \
            .findNext('span', class_='argument').text
    except AttributeError:
        multimedia = 'None'

    try:
        other = soup.find('span', class_='label', title='Скрыть', text='Інше') \
            .findNext('span', class_='argument').text
    except AttributeError:
        other = "None"

    car_details = [model, price, body_type, mileage, engine, transmission, wheel_drive, color,
                   description, traffic_accident, paintwork, technical_condition, condition,
                   security, comfort, multimedia, other, link]

    return car_details


def parse_new_auto(soup: BeautifulSoup, link):
    model = soup.find('h1', class_='auto-head_title bold mb-15').text

    price = soup.find('div', title='Остаточну вартість уточнюйте у дилера').text

    body_type = soup.find('div', class_='mb-15').findNext('div', class_='mb-15') \
        .findNext('div', class_='mb-15').text

    mileage = '0'

    engine = soup.find('dl', class_='defines_list mb-15 unstyle') \
        .findNext('dd', class_='defines_list_value').text

    transmission = soup.find('dt', class_='defines_list_title', text='Коробка передач') \
        .findNext('dd', class_='defines_list_value').text

    try:
        wheel_drive = soup.find('dt', class_='defines_list_title', text='Привід') \
            .findNext('dd', class_='defines_list_value').text
    except AttributeError:
        wheel_drive = 'For more information contact the dealership'

    try:
        color = soup.find('dt', class_='defines_list_title color', text='Колір кузова')\
            .findNext('dd', class_='defines_list_value color').text
    except AttributeError:
        color = 'For change color contact the dealership'

    try:
        description = soup.find('dd', class_='defines_list_value comment').text
    except AttributeError:
        description = 'For more information contact the dealership'

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
    write_to_csv('detail_announcement.csv',
                 [['model', 'price', 'body_type', 'mileage', 'engine', 'transmission', 'wheel_drive', 'color',
                   'description', 'traffic_accident', 'paintwork', 'technical_condition', 'condition',
                   'security', 'comfort', 'multimedia', 'other', 'link'], ])

    for announcement in read_from_csv('id_announcement.csv')[1:]:
        responce = requests.get(announcement[1])
        responce.raise_for_status()
        soup = BeautifulSoup(responce.content, 'lxml')
        link = responce.url
        if link.find('https://auto.ria.com/uk/newauto/'):
            car_details = parse_used_auto(soup, link)
        else:
            car_details = parse_new_auto(soup, link)
        print(link)
        add_to_csv('detail_announcement.csv', [car_details, ])


parse_page()
parse_id_announcements()
parse_detail_announcement()

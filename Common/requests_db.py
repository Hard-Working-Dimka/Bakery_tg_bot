import requests


def request_db_is_ready_cakes():
    response = requests.get('http://217.114.15.72:8000/api/cakes')
    response.raise_for_status()
    return response.json()


def request_db_to_post_users_data(payload_users_data):
    url = 'http://217.114.15.72:8000/api/customusers/'
    response = requests.post(url, json=payload_users_data)
    response.raise_for_status()


def request_db_to_post_order_list(payload_order):
    url = 'http://217.114.15.72:8000/api/orders/'
    response = requests.post(url, data=payload_order)
    print(response.status_code,response.text)
    response.raise_for_status()


def get_modifications_cake():
    for cake in request_db_is_ready_cakes():
        if cake['name'] == 'Кастомный':
            return cake['modifications']


def get_levels_cake():
    levels = {}
    for modification in get_modifications_cake():
        if modification['modification'] == 'Количество уровней':
            for variable in modification["variables_of_modification"]:
                levels[variable["tier"]] = variable["price"]
            return levels


def get_shapes_cake():
    shapes = {}
    for modification in get_modifications_cake():
        if modification['modification'] == 'Форма':
            for variable in modification["variables_of_modification"]:
                shapes[variable["tier"]] = variable["price"]
            return shapes


def get_decor_cake():
    decor = {}
    for modification in get_modifications_cake():
        if modification['modification'] == 'Декор':
            for variable in modification["variables_of_modification"]:
                decor[variable["tier"]] = variable["price"]
            return decor


def get_inscription_cake():
    inscription = {}
    for modification in get_modifications_cake():
        if modification['modification'] == 'Надпись':
            for variable in modification["variables_of_modification"]:
                inscription[variable["tier"]] = variable["price"]
            return inscription


def get_berries_cake():
    berries = {}
    for modification in get_modifications_cake():
        if modification['modification'] == 'Ягоды':
            for variable in modification["variables_of_modification"]:
                berries[variable["tier"]] = variable["price"]
            return berries


def get_toppings_cake():
    toppings = {}
    for modification in get_modifications_cake():
        if modification['modification'] == 'Топпинг':
            for variable in modification["variables_of_modification"]:
                toppings[variable["tier"]] = variable["price"]
            return toppings

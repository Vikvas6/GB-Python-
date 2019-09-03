from .controllers import date_controller, get_human_date

actionmapping = [
    {'action': 'date', 'controller': date_controller},
    {'action': 'humandate', 'controller': get_human_date}
]
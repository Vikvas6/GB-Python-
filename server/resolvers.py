from functools import reduce

from settings import INSTALLED_APPS

def get_server_action():
    application = reduce(
        lambda value, item: value + [__import__(f'{item}.routes')],
        INSTALLED_APPS,
        []
    )
    routes = reduce(
        lambda value, item: value + [getattr(item, 'routes', None)],
        application,
        []
    )
    return reduce(
        lambda value, item: value + getattr(item, 'actionmapping', None),
        routes,
        []
    )

def resolve(action):
    actionmapping = {
        item.get('action'): item.get('controller')
        for item in get_server_action()
        if item
    }
    return actionmapping.get(action)

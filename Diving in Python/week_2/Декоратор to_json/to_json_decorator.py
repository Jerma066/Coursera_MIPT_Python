import json
import functools

def to_json(func):
    @functools.wraps(func)   #функция к которой применяется декоратор не меняет своегоименени
    def wrapped(*args, **kwargs):
        result = json.dumps(func(*args, **kwargs))
        return result

    return wrapped


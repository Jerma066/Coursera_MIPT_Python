import tempfile
import argparse
import json
import os

def get_data(file_path, key):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            data = f.read().strip()
            d = json.loads(data)
            return d[key]


def write_data(file_path, key, value):
    d = {}
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            data = f.read().strip()
            d = json.loads(data)

    if key in d:
        d[key].append(value)
    else:
        d[key] = [value]

    with open(file_path, 'w') as f:
        f.write(json.dumps(d))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-k', '--key',      help='Ключ словаря по которому нужно вернуть или записать значение.')
    parser.add_argument('-v', '--value',    help='Значение для записи в файл для конкретного ключа.')

    args = parser.parse_args()

    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

    if args.value is None:
        answer = get_data(storage_path, args.key)
        print(answer, sep=', ')
    else:
        write_data(storage_path, args.key, args.value)
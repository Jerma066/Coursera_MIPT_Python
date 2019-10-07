import os
import csv

class BaseCar:
    """Базовый класс с общими методами и атрибутами"""

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying

    def __str__(self):
        return(f'{self.brand}, {self.carrying}')

    def get_photo_file_ext(self):
        file_extension = os.path.splitext(self.photo_file_name)
        return file_extension


class Car(BaseCar):
    """Класс легковой автомобиль"""

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        self.car_type = 'car'
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)

class Truck(BaseCar):
    """Класс грузовой автомобиль"""

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        self.car_type = 'truck'
        super().__init__(brand, photo_file_name, carrying)
        # размеры кузова

        if len(body_whl) > 0:
            self.body_width = float(body_whl.split('x')[0])
            self.body_height = float(body_whl.split('x')[1])
            self.body_length = float(body_whl.split('x')[2])
        else:
            self.body_width = 0
            self.body_height = 0
            self.body_length = 0

    def get_body_volume(self):
        volume = self.body_width*self.body_height*self.body_length
        return volume


class SpecMachine(BaseCar):
    """Класс спецтехника"""

    def __init__(self, brand, photo_file_name, carrying, extra):
        self.car_type = 'spec_machine'
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

def get_car_list(csv_filename):
    car_list = []

    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            if len(row) == 7:
                car_type, brand, passenger_seats_count, photo_file_name, body_whl, carrying, extra = row
                if car_type == 'car':
                    car_list.append(Car(brand, photo_file_name, carrying, passenger_seats_count))
                elif car_type == 'truck':
                    car_list.append(Truck(brand, photo_file_name, carrying, body_whl))
                elif car_type == 'spec_machine':
                    car_list.append(SpecMachine(brand, photo_file_name, carrying, extra))

    return car_list


if __name__ == '__main__':
    c_l = get_car_list("coursera_week3_cars.csv")

    for car in c_l:
        print(car)


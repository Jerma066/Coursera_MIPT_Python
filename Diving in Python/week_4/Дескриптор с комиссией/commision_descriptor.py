class Value:
    def __init__(self):
        self.value = None

    @staticmethod
    def _prepare_value(obj, value):
        return value*(1 - obj.commission)

    def __set__(self, obj, value):
        self.value = self._prepare_value(obj, value)

    def __get__(self, obj, obj_type):
        return self.value

class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


if __name__ == '__main__':
    new_acc = Account(0.1)
    new_acc.amount = 100
    print(new_acc.amount)
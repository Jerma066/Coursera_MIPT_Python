import tempfile as tmp
import os

class File:
    def __init__(self, file_path):
        self.file_path = file_path
        self.current = 0

    def __str__(self):
        return self.file_path

    #-- Реализация итерабильности-------------------------------------
    def __iter__(self):
        return self

    def __next__(self):
        with open(self.file_path, 'r', encoding='utf8') as f:
            lines = f.readlines()
            if self.current >= len(lines):
                raise StopIteration
            result = lines[self.current]
            self.current += 1
            return result
    #-----------------------------------------------------------------

    def __add__(self, obj):
        new_path = os.path.join(tmp.gettempdir(), 'sum_of_files.txt')
        answer_file_class = File(new_path)
        answer_file_text = self.read() + obj.read()
        answer_file_class.write(answer_file_text)
        return answer_file_class

    def read(self):
        buffer = ''
        # используется наша итерабильность
        for str in self:
            buffer += str
        return buffer

    def write(self, text):
        with open(self.file_path, 'w') as f:
            f.write(text)


if __name__ == '__main__':
    file_first = File('file_first.txt')
    file_first.write("Hello\nworld\n")
    file_second = File('file_second.txt')
    file_second.write("Glory to the U-Force\n")

    file_first + file_second


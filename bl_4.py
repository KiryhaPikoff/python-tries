import math
import random
import time
import docx2txt

class BlumFilter:
    bit_array = []
    hash_funcs = []

    def __init__(self, bit_arr_size: int, hash_funcs_count: int):
        self.bit_array = [False] * bit_arr_size
        self.hash_funcs = []
        for i in range(0, hash_funcs_count):
            self.hash_funcs.append(self.GetHashFunc(bit_arr_size))
        return

    def GetHashFunc(self, size: int):
        rand = random.randint(0, size)

        def hashLambda(string: str):
            newhash = rand
            for char in string:
                newhash *= ord(char)
            return newhash % size

        return hashLambda

    def find_word(self, word: str):
        for hash_func in self.hash_funcs:
            if not self.bit_array[hash_func(word)]:
                return False
        return True

    def add_word(self, word: str):
        if not self.find_word(word):
            for func in self.hash_funcs:
                self.bit_array[func(word)] = True;
        return

find_word = "вдуцз"
filters = [
    BlumFilter(bit_arr_size=229102, hash_funcs_count=3)
]

textFrom = docx2txt.process("dost.docx")

words_dict = {}
for word in textFrom.split(' '):
    if word not in words_dict:
        words_dict[word] = 1

words = len(words_dict)
p = 0.1
bit_arr_size = int(-words * math.log(p) / (math.log(2) * math.log(2)))
hash_func_count = round(math.log(2) * bit_arr_size / words)

print(f'Optimal bit array size={bit_arr_size}')
print(f'Optimal hashes count={hash_func_count}')

for filter in filters:
    start_time = time.perf_counter_ns()
    for word in textFrom.split():
        filter.add_word(word)
    print(f'Время добавления слов в фильтр: {(time.perf_counter_ns() - start_time)}')

start_time = time.perf_counter_ns()
for word in textFrom.split():
    if word == find_word:
        print(word)
        print(f'Поиск перебором слов занял: {(time.perf_counter_ns() - start_time)}')
        break

print()

for filter in filters:
    start_time = time.perf_counter_ns()
    print(f'Слово найдено фильром блума = {filter.find_word(find_word)}')
    print(f'Поиск фильтром блума занял: {(time.perf_counter_ns() - start_time)}')
    print()


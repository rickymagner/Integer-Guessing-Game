import random as random

import requests

# number = random.randint(1,330000)

def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

class OEISFetcher:
    def __init__(self):
        self.id = 4         # corresponding to zero sequence
        self.url = 'https://oeis.org/A' + str(id)
        self.texturl = self.url + '/b' + str(id) + '.txt'
        self.sequence = []

    def fetch_sequence(self, id):
        self.id = id
        self.url = 'https://oeis.org/A' + str(id)
        self.texturl = self.url + '/b' + str(id) + '.txt'
        txt = requests.get(self.texturl)
        lines = txt.content
        lines = str(lines, 'utf-8')
        lines = lines.splitlines()
        del lines[0]

        str_lines = [x.split(' ')[1] for x in lines]
        self.sequence = [int(x) for x in str_lines]
        return self.sequence

    def get_random_sequence(self):
        id = random.randint(1,330000)
        try:
            seq = self.fetch_sequence(id)
        except:
            self.get_random_sequence()
        else:
            self.sequence = seq
        return self.sequence


# seq = OEISFetcher(number)
# print(number)
# print(seq.sequence)
# print(seq.url)
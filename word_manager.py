import csv
import random
from difficulty import Level
class WordManager:
    def __init__(self,filename="words.csv"):
        self.filename=filename
        self.words=self.load_words()
        self.level_pools={}
        self.prepare_pools()
    def load_words(self):
        with open(self.filename,"r",encoding="utf-8")as file:
            reader=csv.DictReader(file)
            return list(reader)
    def prepare_pools(self):
        for level in Level:
            self.level_pools[level]=[]

        for row in self.words:
            frequency=float(row["frequency"])

            for level, data in Level.items():
                if(data["min_frequency"]<=frequency<=data["max_frequency"]):
                    self.level_pools[level].append(row)
                    break
        for level in self.level_pools:
            random.shuffle(self.level_pools[level])

    def get_random_word(self,level):
        pool=self.level_pools[level]

        if not pool:
            self.refill_pool(level)
        return pool.pop()
    def refill_pool(self,level):
        for row in self.words:
            frequency=float(row["frequency"])
            data=Level[level]
            if(data["min_frequency"]<=frequency<=data["max_frequency"]):
                self.level_pools[level].append(row)

        random.shuffle(self.level_pools[level])
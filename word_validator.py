import csv

class WordValidator:
    def __init__(self,filename="words.csv"):
        self.filename=filename
        self.valid_words=self.load_words()
    def load_words(self):
        with open(self.filename,"r",encoding="utf-8") as file:
            reader = csv.DictReader(file)

            return{
                row["word"].strip().lower()
                for row in reader
            }
    def is_valid(self,word,secret_length):
        word=word.strip().lower()
        if len(word)!=secret_length:
            return False
        return word in self.valid_words
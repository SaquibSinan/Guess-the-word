import csv
from wordfreq import iter_wordlist,zipf_frequency

MIN_LENGTH=3
MAX_LENGTH=12
MIN_FRQ=1

AllWords=iter_wordlist("en")
Words=set()

for word in AllWords:
    word.lower()
    if not word.isalpha():
        continue
    if len(word)<MIN_LENGTH or len(word)>MAX_LENGTH:
        continue
    frequency=zipf_frequency(word,"en")
    if frequency<MIN_FRQ:
        continue
    Words.add(word)


with open("words.csv","w",newline="",encoding="utf-8")as WordFile:
    WordWriter=csv.writer(WordFile)
    WordWriter.writerow(["word","frequency","Length"])

    for word in Words:
        frequency=zipf_frequency(word,"en")
        WordWriter.writerow([word,frequency,len(word)])
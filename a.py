import lki

for word, unstressed in lki.words.get_word_pairs(lki.words.get_words()):
    print(word)
'''
Вывод самого частого слова
'''

def get_words(file):
    with open(file) as file:
        text = file.read()
    text = text.replace(',','\n')\
                .replace(' ,','\n')\
                .replace(', ','\n')\
                .replace(' ','-')
    text = text.strip('\n')
    words = text.split()
    return words

def get_words_dict(words):
    words_dict = dict()
    for word in words:
        if word in words_dict:
            words_dict[word] = words_dict[word] + 1
        else:
            words_dict[word] = 1
    return words_dict

def main():
    d=[]
    filename = 'input.txt'
    words = get_words(filename)
    words_dict = get_words_dict(words)
    for word in words_dict:
        d.append([word,words_dict[word]])
    d=sorted(d,key=lambda k: k[1])
    print(str(d[-1][0]).replace('-',' '))

main()

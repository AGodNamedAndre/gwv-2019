import pandas as pd
from random import randrange

def parse_file(path):
    post = {} # posterior from word
    
    with open(path, 'r') as text:
        text = '<start>\n' + text.read().replace("\n\n", "\n<end>\n<start>\n") + '\n<end>'
        text = text.split()
        
        for i in range(len(text)-1):
            w = text[i]
            post_w = text[i+1]

            if w in post.keys():
                if post_w in post[w].keys():
                    post[w][post_w] += 1
                else:
                    post[w][post_w] = 1
            else:
                post[w] = {post_w: 1}

    return post


def draw(post, query):
    probs = post[f'{query}']
    s = sum(probs.values())
    r = randrange(1, s) if s > 1 else 1
    sum_of_probs = 0
    for w in probs.keys():
        sum_of_probs += probs[w]
        if sum_of_probs >= r:
            return w
        
        
def generate_sentence(start_word='', count_words=-1):
    w = '<start>' if start_word =='' else start_word
    satz = ''
    i = 0
    while w != '<end>' or count_words != -1:
        if i == count_words:
            break
        w = draw(post, w)
        satz += w + ' ' if not w in ['<start>', '<end>'] else ''
        i += 1

    return satz

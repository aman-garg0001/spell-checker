import re
from nltk.tokenize import word_tokenize
import nltk
from collections import Counter

#Tokenise words using regex
def words(document):
    return re.findall(r'\w+', document.lower())
    
file = open("spell_dataset.txt", "r")
input = file.read()
#outputs word : no. of its instances
all_words = Counter(words(input))

#function for producing all edits that are one edit away from the word
def edits_one(word):
    alphabets    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [left + right[1:] for left, right in splits if right]
    inserts    = [left + c + right for left, right in splits for c in alphabets]
    replaces   = [left + c + right[1:] for left, right in splits if right for c in alphabets]
    transposes = [left + right[1] + right[0] + right[2:] for left, right in splits if len(right)>1]
    return set(deletes + inserts + replaces + transposes)
    
#function for producing all words with edit distance = 2
def edits_two(word):
    return (e2 for e1 in edits_one(word) for e2 in edits_one(e1))
    
#creates list of all valid words
def known(words):
    return set(word for word in words if word in all_words)
    
#returns word if word is valid or if it isn't then all edits on the word
def possible_corrections(word):
    return (known([word]) or known(edits_one(word)) or known(edits_two(word)) or [word])    
    
#Probability of a word = Number of appearances of word / total number of tokens
def prob(word, N=sum(all_words.values())): 
    return all_words[word] / N
    
#Print the most probable spelling correction for word out of all the possible_corrections
def spell_check(word):
    correct_word = max(possible_corrections(word), key=prob)
    if correct_word != word:
        return "Correct Spelling of '" + word + "' is '" + correct_word + "'"
    else:
        return "Spelling of '" + word + "' is correct"
        
file_inp = open('input.txt', 'r')
inp = file_inp.read()
file_inp.close()
file_out = open('output.txt', 'w')
file_out.write(spell_check(inp))
file_out.close()  

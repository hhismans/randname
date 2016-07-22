"""
personal project that make no sense.
trying to genereate random name by analysis sequence of letter in a lot of name
"""

#IMPORT
import unicodedata
import time
import re
import random
from random import randint
#FUNCTION

def iterate(iterable):
    iterator = iter(iterable)
    item = iterator.next()

    for next_item in iterator:
        yield item, next_item
        item = next_item

    yield item, None

#reading file
def readAndParseFile(path):
	"""	return value : tab of word [word, word]
		word structure : [name, type, region, frequency]"""
	f = open(path, 'r')
	words = f.readlines()
	f.close()

	for word, index in zip(words, xrange(len(words))):
		words[index] = re.split('\t', word)
	return words

def getByRegion(words, region):
	ret = []
	if (region == 'any'):
		return words
	for word in words:
		if (word[2] in region):
			ret.append(word)
	return ret;


def getData(words):
	ret = {}
	for word in words:
		for letter, nextletter in zip(word[0], word[0][1:]):
			if (letter.isalpha() and nextletter.isalpha()):
				if(not ret.has_key(letter)):
					ret[letter] = {};
				if(not ret[letter].has_key(nextletter)):
					ret[letter][nextletter] = 0;
				ret[letter][nextletter] += 1
	return ret

def normalize(data):
# exemple of data in input : {'a': {'c': 9, 'b': 5, 'e': 2, 'd': 8, 'g': 1, 'i': 26,...}, 'b': ...}:
	for mainLetter, objectLetter in data.iteritems():
		sum = 0;
		for letter, frequency in objectLetter.iteritems():
			sum += frequency
		for letter, frequency in objectLetter.iteritems():
			data[mainLetter][letter] = frequency * 1000 / sum
		sum = 0;
		for letter, frequency in objectLetter.iteritems():
			sum += frequency
	return data

def addThem(normalizedData):
	""" add all normalized like this
		normalized : {a: {a:1, b:2, c:3}}
		after add : {a : {a : 1, b: 3(a+b), c: (b+c)}
		then take a random number between 0 and max, and stop explore when randNumber > value"""
	for mainLetter, objectLetter in normalizedData.iteritems():
		prev = 0;
		for letter, nextOne in iterate(objectLetter.iteritems()):
			if (nextOne):
				if (prev == 0):
					normalizedData[mainLetter][nextOne[0]] += letter[1]
				else :
					normalizedData[mainLetter][nextOne[0]] += prev
				prev = normalizedData[mainLetter][nextOne[0]]
	return normalizedData

def generateARandomName(finalData, size, startString):
	retWord = startString
	if (not startString[-1:]):
		retWord = random.choice('qwertyuiopasdfghjklzxcvbnm');
	currentletter = retWord[-1:]
	
	for i in xrange(size):
		rand = randint(10, 1000); #IMPRESSISION PSQ J"AI LA FLEM, mettre le nombre max a la normalisation
		for key, value in finalData[currentletter].iteritems():
			if (rand < value):
				retWord+= key
				currentletter = key;
				break;
	print '\t', retWord;




#####################
#      Main         #
#####################

numOfGen = 10
regions = ['french', 'spanish', 'any', 'english', 'arabic']
data = readAndParseFile('Prenoms.txt');
for region in regions:
	print region
	words = getByRegion(data, region); #word structure [name, type(f/m), region, frequency]
	for i in xrange(numOfGen):
		generateARandomName(addThem(normalize(getData(words))), randint(3,6), '');

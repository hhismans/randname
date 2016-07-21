"""
Some mickmath stuff

If you want to use with another dict:
change path line 25
check the "parsing words" part (line 27)
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
		if (word[2] == region):
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

def generateARandomName(finalData, size):
	currentletter = random.choice('qwertyuiopasdfghjklzxcvbnm');
	retWord = currentletter;
	for i in xrange(size):
		print finalData[currentletter];
		rand = randint(10, 1000); #IMPRESSISION PSQ J"AI LA FLEM, mettre le nombre max a la normalisation
		for key, value in finalData[currentletter].iteritems():
			if (rand < value):
				retWord+= key
				currentletter = key;
				break;
	print retWord;




#####################
#      Main         #
#####################

#start = int(input("Quelle annee voulez vous commencer le test : "))
#end   = int(input("Quelle annee voulez vous terminer le test : "))

words = getByRegion(readAndParseFile('Prenoms.txt'), 'french'); #word structure [name, type(f/m), region, frequency]
timeBegin = time.time()

generateARandomName(addThem(normalize(getData(words))), 8);

"""

#parsing words
evalList = []
for word in words:
	word = word[0:-1]
	_word = unicode(word, 'utf-8')
	_word = unicodedata.normalize('NFD', _word).encode('ascii', 'ignore')
	evalList.append((word, evalWord(_word)))

#init
total = 0
max = (0, -1) #(year, number of words found in this year)
nbrOfYearWithResult = 0

#seach in evalList
for year in xrange(start, end + 1):
	count = 0
	to_print=[]
	for tuple in evalList:
		if tuple[1] == year:
			to_print.append(str(tuple[0]));
			count +=1
	if count > 0:
		print "\n", year, ",", count, "words found:"
		printL(to_print)
		total += count
		nbrOfYearWithResult += 1
		if count > max[1]:
			max = (year,count)

#final result on stdout
print "\n", total, "words found between", start, "and", end
print nbrOfYearWithResult, "years have their words"
print max[0], "is the winner year with", max[1], "words !"
rint "time : ", time.time() - timeBegin, "s" """

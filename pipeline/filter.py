from pipeline import *

class FistSentenceLimiter:
	"""
	Limit the text, word boundaries and 
	sentence boundaries of a given document
	to the first sentence
	"""
	def run(self, document):
		first = document.sentences_boundaries[0]
		document.text = document.text[first[0]:first[1]]
		words_boundaries_new = []
		for word in document.words_boundaries:
			if word[1] <= first[1]:
				words_boundaries_new.append(word) 
		document.words_boundaries = words_boundaries_new 
		document.sentences_boundaries = [first]
		return document

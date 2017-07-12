from pipeline import *

class FistSentenceLimiter:
	"""
	Limit the text, word boundaries and 
	sentence boundaries of a given document
	to the first sentence
	"""
	def run(self, document):
		first = document.sentences_boundaries[0]
		document.sentences_boundaries = [first]
		document.text = document.text[first[0]:first[1]]
		document.words_boundaries = self.limitWordBoundaries(document.words_boundaries, first[1]) 
		document.entities = self.limitEntities(document.entities, first[1])
		document.triples = self.limitTriples(document.triples, first[1])
		return document

	def limitEntities(self, entities, maxi):
		entities_new = []
		for e in entities:
			if e.boundaries[1] <= maxi:
				entities_new.append(e)
		return entities_new

	def limitTriples(self, triples, maxi):
		triples_new = []
		for t in triples:
			if t.sentence_id == 0:
				triples_new.append(t)
		return triples_new

	def limitWordBoundaries(self, words_boundaries, maxi):
		words_boundaries_new = []
		for word in words_boundaries:
			if word[1] <= maxi:
				words_boundaries_new.append(word) 
		return words_boundaries_new

class MainEntityLimiter:
	"""
	Remove a document's content if the main entity is not aligned
	"""
	def run(self, document):
		if not document.docid in [i.uri for i in document.entities]:
			document = None
		return document


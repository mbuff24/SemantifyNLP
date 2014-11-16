#	Treebank Parser tag definitions
#	https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
#
#	Triplet Extraction paper
#	http://ailab.ijs.si/dunja/SiKDD2007/Papers/Rusu_Trippels.pdf

import json

ADJECTIVE_TYPES = ["JJ", "JJR", "JJS"]
NOUN_TYPES = ["NN", "NNP", "NNPS", "NNS"]
VERB_TYPES = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
ADVERB_TYPES = ["RB", "RBR", "RBS"]

def findFirstType(tag_type, tree):
	subtrees = []
	for t in tree:
		if type(t) is list:
			if t[1] in tag_type:
				return t[0]
		elif type(t) is dict:
			for key in t.keys():
				subtrees.extend(t[key])
		else:
			print("t isn't list or dict, wtfman")

	return findFirstType(tag_type, subtrees)

def findDeepestType_r(tag_type, tree, candidates):
	subtrees = []
	for t in tree:
		if type(t) is list:
			# TODO: add some pruning here
			# ie. Verbs are only in VPs
			if t[1] in tag_type:
				candidates.append(t[0])
		elif type(t) is dict:
			for key in t.keys():
				subtrees.extend(t[key])
		else:
			print("t isn't list or dict, wtfman")

	if len(subtrees) == 0:
		return candidates
	else:
		return findDeepestType_r(tag_type, subtrees, candidates)

def findDeepestType(tag_type, tree):
	verbs = findDeepestType_r(tag_type, tree, [])
	index = len(verbs)
	return verbs[index-1]

def findAllTreesOfType(tag_type, tree, acc):
	subtrees = []

	for t in tree:
		if type(t) is dict:
			for key in t.keys():
				if key in tag_type:
					acc.append(t)
				else:
					subtrees.extend(t[key])		

	if len(subtrees) == 0:
		return acc
	else:
		return findAllTreesOfType(tag_type, subtrees, acc)

# def extract_attributes(word):
# 	if isAdjective(word)
# 		# all RB siblings
# 		#result = 
# 	return word

def extract_subject(np):
	subject = None
	# subject = first noun found in NP_subtree
	subject = findFirstType(NOUN_TYPES, np)

	#extract attributes next..
	return subject

def extract_predicate(vp):
	verb = None

	# verb = the deepest verb in VP_subtree
	verb = findDeepestType(VERB_TYPES, vp)

	#extract attributes next..
	return verb


def extract_object(vp):
	# siblings = all NP, PP, ADJP siblings of vp
	types = ["NP", "PP", "ADJP"]
	siblings = findAllTreesOfType(types, vp, [])

	for sibling in siblings:
		for key in sibling.keys():
			if key == "NP":
				# obj = first noun in sibling
				return findFirstType(NOUN_TYPES, sibling["NP"])
			elif key == "PP":
				return findFirstType(NOUN_TYPES, sibling["PP"])
			elif key == "ADJP":
				# obj = first adjective in sibling
				return findFirstType(ADJECTIVE_TYPES, sibling["ADJP"])
			else:
				print("key isn't in [NP, PP, ADJP], wtfman")

	#extract attributes somewhere in here..
	return None

def extract_triplet(sent):
	for root in json:
		sent = root["S"]

		NP = None
		VP = None
		
		# S -> NP, VP
		for phrase in sent:
			if "NP" in phrase:
				NP = phrase["NP"]
			elif "VP" in phrase:
					VP = phrase["VP"]

		print extract_subject(NP)
		print extract_predicate(VP)
		print extract_object(VP)

# read json files!!
json = json.loads(open('./test.json').read())
extract_triplet(json)






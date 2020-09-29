"""
	Author: Isaac Riley
	Date:   September 2020

	To create graph of Wikipedia articles.
"""


import os
import re
import pickle
import json
import networkx as nx
import wikipediaapi
import wikipedia
#from nltk.parse.stanford import StanfordDependencyParser
##from nltk.parse.corenlp import CoreNLPDependencyParser
#from textblob import TextBlob

with open("config.json") as f:
    config = json.load(f)
print("*** Configurations ***")
for k,v in config.items():
	print("  {0:<20}{1}".format(k+':', v))


os.environ['STANFORD_PARSER'] = config["parser_path"]
os.environ['STANFORD_MODELS'] = config["model_path"]

#path_to_jar = '/usr/local/Cellar/stanford-parser/3.9.2_1/libexec/stanford-parser.jar'
#path_to_models = '/usr/local/Cellar/stanford-parser/3.9.2_1/libexec/stanford-parser-3.9.2-models.jar'

class WikiNet(object):
	def __init__(self, ROOT_PATH):
		self.digraph = nx.DiGraph()
		self.ROOT_PATH = ROOT_PATH
		with open(ROOT_PATH+'/data/lists_seed/root_categories.txt', 'r') as f:
			self.seed_categories =  f.read().split('\n')
		self.PEOPLE_PATH = 'data/lists_derived/thinkers.txt'
		self.people = {}
		# self.tag_set = set()
		#self.keywords = set()
		#self.agenda = []
		#self.record = set()
		self.wiki = wikipediaapi.Wikipedia('en')
		self.root_category = ''
		#self.subcats = set()
		#self.dependency_parser = StanfordDependencyParser(path_to_jar=config["path_to_jar"],
		#											 path_to_models_jar=config["path_to_models_jar"])
		# dependency_parser = CoreNLPDependencyParser()
		# self.norms =

	def add_from_seeds_fw(self, depth):
		"""

		:param depth: int
		:return: none
		"""
		for s in seeds:
			self.digraph.add_node(s)
			self.record.add(s)
			self.agenda.add(s)
			page  = self.wiki.page(s)
			links = page.links
			cats  = page.categories

	def add_from_seeds_bw(self, depth):
		"""

		:param depth:
		:return:
		"""
		for s in seeds:
			self.digraph.add_node(s)
			self.record.add(s)
			self.agenda.add(s)
			page  = self.wiki.page(s)
			links = page.backlinks

	def summarize(self):
		"""

		:return: None
		"""
		pass

	def get_people(self):
		"""

		:return:
		"""

		if os.path.exists(self.PEOPLE_PATH):
			with open(self.PEOPLE_PATH) as f:
				self.people = {k:{} for k in f.read().split('\n')}
		else:
			people_set = set()
			for cat in self.seed_categories:
				print('***Seed category***\n{}\n'.format(cat))
				people_set = people_set.union(self.people_in_category(cat))
			self.people.update({k:{} for k in list(people_set)})
			self.save_people_list(self.PEOPLE_PATH)
		print('Total number of thinkers:', len(self.people))

	def get_sections(self):
		self.sectiondict = {}
		count = 0
		self.fails = []
		for l in self.people.keys():
			if count%10==0:
				print(count)
			try:
				p = self.wiki.page(l)
				sections = [s.title for s in p.sections]
				for s in sections:
					if s in self.sectiondict:
						self.sectiondict[s] = self.sectiondict[s] + 1
					else:
						self.sectiondict.update({s: 1})
			except:
				self.fails.append(l)
			count += 1
		#for k, v in self.sectiondict.items():
		#	print("{0:<30}{1:>5}".format(k, v))

	def create_full_network(self, min_thresh):
		"""
		Keep pages linking to or from each thinker that have at
		  least min_thresh links to any thinker.
		:return:
		"""
		if os.path.exists(self.ROOT_PATH+'/data/lists_derived/linkdict.pickle') and \
			os.path.exists(self.ROOT_PATH+'/data/lists_derived/linkset.pickle'):
			with open('data/lists_derived/linkdict.pickle', 'rb') as f:
				linkdict = pickle.load(f)
			print("opened")
			with open('data/lists_derived/linkset.pickle', 'rb') as f:
				linkset = pickle.load(f)
			print("opened")
			total = len(linkset)
		else:
			linkdict = {k:{'from' : set(), 'to':set()} for k in self.people.keys()}
			linkset = set()
			fails = []
			for k in linkdict.keys():
				try:
					p = self.wiki.page(k)
					from_ = set(p.links.keys())
					to_ = set(p.backlinks.keys())
					linkdict[k]['from'] = from_
					linkdict[k]['to'] = to_
					linkset = linkset.union(from_)
					linkset = linkset.union(to_)
					print("{} -> {} -> {}".format(len(to_), k, len(from_)))
				except:
					fails.append(k)
			while fails:
				f = fails.pop()
				try:
					p = self.wiki.page(f)
					from_ = set(p.links.keys())
					to_ = set(p.backlinks.keys())
					linkdict[k]['from'] = from_
					linkdict[k]['to'] = to_
					linkset = linkset.union(from_)
					linkset = linkset.union(to_)
					print("{} -> {} -> {}".format(len(to_), f, len(from_)))
				except:
					fails.append(k)
					print("Failed again: {}".format(k))
			total = len(linkset)
			with open(self.ROOT_PATH+'/data/lists_derived/linkdict.pickle', 'wb') as f:
				pickle.dump(linkdict, f)
			print('linkdict saved.')
			with open(self.ROOT_PATH+'/data/lists_derived/linkset.pickle', 'wb') as f:
				pickle.dump(linkset, f)
			print('linkset saved.')
			print("Total links: {}".format(total))

		if os.path.exists(self.ROOT_PATH + '/data/lists_derived/link_count_dict.pickle'):
			with open(self.ROOT_PATH + '/data/lists_derived/link_count_dict.pickle', 'rb') as f:
				counts = pickle.load(f)
		else:
			counts = {l: 0 for l in list(linkset)}
			for l in list(linkset):
				for v in linkdict.values():
					if l in v['from']:
						counts[l] += 1
					if l in v['to']:
						counts[l] += 1
			with open(self.ROOT_PATH + '/data/lists_derived/link_count_dict.pickle', 'wb') as f:
				pickle.dump(counts, f)

		print("Highest counts: {}".format(sorted(counts.values())[:20]))
		print("Median counts: {}".format(sorted(counts.values())[int(total/2)-10:int(total/2)+10]))
		print("Lowest counts: {}".format(sorted(counts.values())[-20:]))

		occs = list(counts.values())
		for n in range(1, 101):
			print("{} occurrences of {}".format(occs.count(n), n))

		keepers = [k for k, v in counts.items() if v >= min_thresh]
		to_add = [x for x in keepers if x not in self.people.keys()]
		print("{} removed.".format(len(counts)-len(keepers)))
		print("{} thinkers linked.".format(len(keepers)-len(to_add)))
		self.digraph.add_nodes_from(to_add, attr={'type': 'other'})
		to_add = set(to_add)
		for u,val in linkdict.items():
			for v in list(val['from']):
				if v in to_add:
					self.digraph.add_edge(u, v, attr={"weight" : 0})
			for v in list(val['to']):
				if v in to_add:
					self.digraph.add_edge(v, u, attr={"weight" : 0})

	def save_people_list(self, write_path):
		"""
		Used to save list of thinkers as file.
		:return:
		"""
		with open(write_path, 'w') as f:
			f.write('\n'.join(sorted(self.people.keys())))
		print('Successfully saved at: {}'.format(write_path))

	def save_people_text(self): # as txt files
		"""

		:return:
		"""
		count = 0
		for k in self.people.keys():
			if count%50==0:
				print(k)
			if not os.path.exists('data/text_thinkers/{}.txt'.format(k)):
				text = self.wiki.page(k).text
				with open('data/text_thinkers/{}.txt'.format(k), 'w') as f:
					f.write(text)
			count += 1

	def save_people_html(self): # as txt files
		"""

		:return:
		"""
		fails = []
		for k in self.people.keys():
			k_ = k.replace(" ", "_")
			try:
				h = wikipedia.page(k).html()
				with open("data/html_thinkers/{}.html".format(k_), "w") as f:
					f.write(h)
				print("{} saved.".format(k_))
			except:
				fails.append(k)
		print("***************************")
		for f in fails:
			print(f)
		print("***************************")


	def save_people_outlinks(self): # as json
		"""

		:return:
		"""

	def save_people_inlinks(self): # as json
		"""

		:return:
		"""

	def save_people_categories(self): # as json
		"""

		:return:
		"""

	def save_people_sections(self): # as json
		"""

		:return:
		"""

	def get_ngrams(self): # as txt files (for each n)
		"""

		:return:
		"""

	def get_ngram_importance(self): # as txt files (for each n)
		"""

		:return:
		"""

	def choose_ngrams(self): # as csv
		"""

		:return:
		"""

	def extract_anchors(self): # as json (for each thinker?)
		"""


		:return:
		"""
		with open("data/lists_derived/linkdict.pickle", "rb") as f:
			linkdict = pickle.load(f)
		for k in list(self.people.keys())[100:115]:
			print("***************************")
			print(k)
			print("***************************")
			k_ = k.replace(" ", "_")
			with open("data/html_thinkers/{}.html".format(k_), "r") as f:
				raw = f.read().rsplit("</h2", 1)[0].split("<h2", 1)[-1]
				#print(raw)
			for l in list(linkdict[k]["from"])[10:15]:
				l_ = l.replace(" ", "_")
				print("---------------------------")
				print("LINK:", l)
				print("---------------------------")
				pattern1 = re.compile('[^\.\?\!\n]+?<a href="/wiki/{}" title="{}">.+?</a>.+?[\.\?\!]'.format(l_, l))
				#pattern1 = re.compile('(?<=<p>).+?<a href="/wiki/{}" title="{}">.+?</a>.+?(?=</p>)'.format(l_, l), re.S)
				pattern2 = re.compile('\<a href="/wiki/{}" title="{}">.+?</a>'.format(l_, l))
				s = re.search(pattern1, raw)
				if s:
					large = s.group()
					anchor = re.sub(pattern2, "LINK", large)
					anchor = re.sub("<.+?>", "", anchor)
					anchor = re.sub("&#91;.*?&#93;", "", anchor)
					print("ANCHOR:"" anchor)
				else:
					print("No match found for {} in {}.".format(l, k))
				# need to decide how to save links



	def people2graph(self):
		"""

		:return:
		"""
		self.digraph.add_nodes_from(list(self.people.keys()), attr={'type' : 'thinker'})

	def dep_parse(self, anchor, entity):
		"""
		Uses NLTK with Stanford CoreNLP to generate a dependency parse.
		:return:
		"""
		result = dependency_parser.raw_parse(anchor)
		parse = list(next(result).triples())
		return parse

	def get_opinion(self, anchor, string):
		"""

		:return:
		"""
		blob = TextBlob(anchor)



	def people_in_category(self, category):
		"""
		:string category: wiki identifier for category page
		:return: list of pages in category
		"""
		page = self.wiki.page(category)
		pages = set([k for k in page.categorymembers if not (('Category:' in k) or ('List of' in k))])
		#list_pages = [k for k in page.categorymembers if 'List of' in k]
		#if list_pages:
		#	for l in list_pages:
		#
		return pages

	def get_subcats_all(self):
		"""
		Collects all categories in the hierarchy under a given root category.
		"""
		subcats_past = set([self.root_category])
		agenda = [self.root_category]
		subcats = set()
		while agenda:
			a = agenda.pop()
			print(a)
			newcats = self.get_subcats_imm(a)
			subcats_past.add(a)
			agenda.extend(list(newcats.difference(subcats_past)))
			subcats = subcats.union(newcats)
			print(len(subcats))
			print(len(subcats_past))
			print(len(newcats))
			print(len(agenda))
		self.subcats = subcats


	def get_subcats_imm(self, root_cat):
		"""
		Collects all subcategories for a given category page.
		"""
		subcats = set()
		page = self.wiki.page(root_cat)
		members = page.categorymembers.keys()
		for m in members:
			if 'Category:' in m:
				subcats.add(m)
		return subcats


						




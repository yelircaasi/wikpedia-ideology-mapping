"""
	Author: Isaac Riley
	Date:   September 2020

	To create graph of Wikipedia articles.
"""


import networkx as nx
import wikipediaapi


class WikiNet(object):
	def __init__(self, SEED_CATEGORIES_FILE):
		self.digraph = nx.DiGraph()
		with open(SEED_CATEGORIES_FILE, 'r') as f:
			self.seed_categories =  f.read().split('\n')
		self.people = {}
		# self.tag_set = set()
		#self.keywords = set()
		#self.agenda = []
		#self.record = set()
		self.wiki = wikipediaapi.Wikipedia('en')
		self.root_category = ''
		#self.subcats = set()

	def add_from_seeds_fw(self, depth):
		for s in seeds:
			self.digraph.add_node(s)
			self.record.add(s)
			self.agenda.add(s)
			page  = self.wiki.page(s)
			links = page.links
			cats  = page.categories


	def add_from_seeds_bw(self, depth):
		for s in seeds:
			self.digraph.add_node(s)
			self.record.add(s)
			self.agenda.add(s)
			page  = self.wiki.page(s)
			links = page.backlinks

	def summarize(self):
		pass

	def get_people(self):
		"""

		:return:
		"""
		people_set = set()
		for cat in self.seed_categories:
			print('***Seed category***\n{}\n'.format(cat))
			people_set = people_set.union(self.people_in_category(cat))
		self.people.update({k:{} for k in list(people_set)})
		print('Total number of thinkers:', len(self.people))

	def select_links(self, min_thresh):
		"""
		Keep pages linking to or from each thinker that have at
		  least min_thresh links to any thinker.
		:return:
		"""
		linkdict = {k:{'from':[], 'to':[]} for k in self.people.keys()}
		for k in linkdict.keys():
			linkdict[k]['from'] = list(self.wiki.page(k).links.keys())
			linkdict[k]['to'  ] = list(self.wiki.page(k).backlinks.keys())




	def save_people_text(self): # as txt files
		pass

	def save_people_outlinks(self): # as json
		pass

	def save_people_inlinks(self): # as json
		pass

	def save_people_categories(self): # as json
		pass

	def save_people_sections(self): # as json
		pass

	def get_ngrams(self): # as txt files (for each n)
		pass

	def get_ngram_importance(self): # as txt files (for each n)
		pass

	def choose_ngrams(self): # as csv
		pass

	def save_anchor_text(self): # as json (for each thinker?)
		pass

	def people2graph(self):
		self.digraph.add_nodes_from(list(self.people.keys()), attr={'type' : 'thinker'})

	def join_people(self):
		pass



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


						




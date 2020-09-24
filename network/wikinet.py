"""
	Author: Isaac Riley
	Date:   September 2020

	To create graph of Wikipedia articles.
"""


import networkx as nx
import wikipediaapi


class WikiNet(object):
	def __init__(self, root_category):
		self.digraph   = nx.DiGraph()
		self.tag_set   = 
		self.seed_list = 
		self.keywords  = 
		self.agenda    = 
		self.record    = set()
		self.wiki      = wikipediaapi.Wikipedia('en')
		self.root_cat  = ''
		self.subcats   = set()

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

	def get_subcats_rec(self, root_category):
		"""
		Collects all categories in the hierarchy under a given root category.
		"""
		subcats_past = set([root_category])
		agenda = [root_category]
		subcats = set()
		while agenda:
			a = agenda.pop()
			newcats = self.get_subcategories(a)
			subcats_past.add(a)
			agenda.extend(list(newcats.difference(subcats_past)))
			subcats.add(newcats)
		self.subcats = subcats


	def get_subcategories(self, root_cat):
		"""
		Collects all subcategories for a given category page.
		"""
		subcats = set()
		page = self.wiki.page(root_page)
		members = page.categorymembers.keys()
		for m in members:
			if 'Category:' in m:
				subcats.add(m)
		return subcats


						




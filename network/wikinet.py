"""
	Author: Isaac Riley
	Date:   September 2020

	To create graph of Wikipedia articles.
"""


import os
import pickle
import networkx as nx
import wikipediaapi


class WikiNet(object):
	def __init__(self, ROOT_PATH):
		self.digraph = nx.DiGraph()
		self.ROOT_PATH = ROOT_PATH
		with open(ROOT_PATH+'/data/lists_seed/root_categories.txt', 'r') as f:
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
		PEOPLE_PATH = self.ROOT_PATH+'/data/lists_derived/thinkers.txt'
		if os.path.exists(PEOPLE_PATH):
			with open(PEOPLE_PATH) as f:
				self.people = {k:{} for k in f.read().split('\n')}
		else:
			people_set = set()
			for cat in self.seed_categories:
				print('***Seed category***\n{}\n'.format(cat))
				people_set = people_set.union(self.people_in_category(cat))
			self.people.update({k:{} for k in list(people_set)})
			self.save_people_list(PEOPLE_PATH)
		print('Total number of thinkers:', len(self.people))

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

	def save_people_html(self): # as txt files
		"""

		:return:
		"""

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

	def save_anchor_text(self): # as json (for each thinker?)
		"""


		:return:
		"""

	def people2graph(self):
		"""

		:return:
		"""
		self.digraph.add_nodes_from(list(self.people.keys()), attr={'type' : 'thinker'})

	def join_people(self):
		"""

		:return:
		"""



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


						




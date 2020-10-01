"""
	Author: Isaac Riley
	Date:   September 2020

	To create and analyze a graph of Wikipedia articles.
"""


import os
import re
import numpy as np
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
print("******* Configurations *******")
for k,v in config.items():
	print("  {0:<20}{1}".format(k+':', v))
print("******************************")


class WikiNet(object):
	def __init__(self, config_dict):
		self.config = config_dict
		self.primary_graph = nx.DiGraph()
		self.secondary_graph = nx.DiGraph()
		self.primary = []
		self.secondary = []
		self.primary_set = set()
		self.secondary_set = set()
		self.secondary_counts = {}
		self.matrices = {}
		self.wiki = wikipediaapi.Wikipedia('en')
		self.wiki2 = wikipedia
		self.filter_re = re.compile("#|mw-redirect|Category:|Wikipedia:|" +
									"Wikipedia_talk:|Help:|Special:|" +
									"User:|_(identifier)|View_this|" +
									"Portal:|_Library|SNAC|Wayback|Discuss_this" +
									"WorldCat|Biblioteca_Nacional|" +
									"Bibsys|^Trove")
		self.filter_link = lambda x: bool(re.search(self.filter_re, x))
		self.link_re = re.compile("<a href=\"/wiki/.+?\" title=\".+?\">.+?</a>")
		#self.dependency_parser = StanfordDependencyParser(path_to_jar=config["path_to_jar"],
		#								     path_to_models_jar=config["path_to_models_jar"])
		# dependency_parser = CoreNLPDependencyParser()
		#os.environ['STANFORD_PARSER'] = self.config["PARSER_PATH"]
		#os.environ['STANFORD_MODELS'] = self.config["MODEL_PATH"]
		# self.norms = self.open_norms_as_dict()

	def save_txt(self, text, path=None, key=None):
		"""
		Simple utility function to save a .txt file.
		:param path: str
		:param key: str key mapped to file path in self.config
		:return: None
		"""
		if key:
			path = self.config[key]
		with open(path, "w") as f:
			f.write(text)

	def open_txt(self, path=None, key=None):
		"""
		Simple utility function to open a .txt file.
		:param path: str
		:param key: str key mapped to file path in self.config
		:return text: str
		"""
		if key:
			path = self.config[key]
		f = open(path, "r")
		return f.read()

	def save_pickle(self, my_object, path=None, key=None):
		"""
		Simple utility function to save a .pickle file.
		:param my_object: object
		:param path: str
		:param key: str key mapped to file path in self.config
		:return: None
		"""
		if key:
			path = self.config[key]
		with open(path, "wb") as f:
			pickle.dump(my_object, f)

	def open_pickle(self, path=None, key=None):
		"""
		Simple utility function to open a .pickle file.
		:param path: str
		:param key: str key mapped to file path in self.config
		:return my_object: obj
		"""
		if key:
			path = self.config[key]
		f = open(path, "rb")
		return pickle.load(f)

	def save_json(self, my_dict, path=None, key=None):
		"""
		Simple utility to save a dictionary as a .json file.
		:param my_dict: dict
		:param path: str
		:param key: str key mapped to file path in self.config
		:return: None
		"""
		if key:
			path = self.config[key]
		with open(path, "w") as f:
			json.dump(my_dict, f, ensure_ascii=False)

	def open_json(self, path=None, key=None):
		"""
		Simple utility to save a .json file as a dictionary.
		:param path: str
		:param key: str key mapped to file path in self.config
		:return my_dict: dict
		"""
		if key:
			path = self.config[key]
		f = open(path, "r")
		return json.load(f)

	def get_primary(self):
		"""
		Opens up list of ideologies and adds it to the WikiNet class.
		:return: None
		"""
		self.primary = self.open_txt(key="PRIMARY_LIST").split('\n')
		self.primary_set = set(self.primary)

	def get_secondary(self):
		"""
		Opens up list of linked pages (if already created and saved)
			and adds it to the WikiNet class.
		:return: None
		"""
		self.secondary = self.open_txt(key="SECONDARY_LIST").split('\n')
		self.secondary_set = set(self.secondary)

	def make_primary_graph(self):
		"""
		Populates primary graph with ideologies.
		:return:
		"""
		self.primary_graph.add_nodes_from(self.primary, attr={'type': 'primary'})

	def summarize_graph(self, my_graph):
		"""
		Displays some key characteristics of the graph.
		:return:
		"""
		print()
		print("Triangles:")
		print(triangles(my_graph))
		print("Transitivity:")
		print(transitivity(my_graph))
		print("Average clustering:")
		print(average_clustering(my_graph))
		print("Square clustering:")
		print(square_clustering(my_graph))
		print("Generalized degree:")
		print(generalized_degree(my_graph))

	def save_html(self, page_id, save_path):
		"""
		Given a list of pages, saves their html in the folder indicated.
		:param page_id:
		:return:
		"""
		try:
			page = page_id.replace("_", " ")
			html = wikipedia.page(page).html()
			file_path = save_path+"/"+page_id+".html"
			if not os.path.exists(file_path):
				self.save_txt(html, path=file_path)
		except:
			print("Page \"{}\" not found.".format(page_id))

	def get_html_primary(self):
		"""
		Saves all the html files for the list of ideologies.
		:return:
		"""
		location = self.config["HTML_FOLDER_PRIMARY"]
		count = 0
		for page in self.primary:
			if count % 25 == 0:
				print("#{0:<5}: {1}".format(count, page))
			self.save_html(page, path=location)
			count += 1

	def get_html_secondary(self):
		"""
		Saves all the html files of the pages that are
			linked to from the list of ideologies.
		:return:
		"""
		location = self.config["HTML_FOLDER_SECONDARY"]
		count = 0
		for page in self.secondary:
			if count % 25 == 0:
				print("#{0:<5}: {1}".format(count, page))
			self.save_html(page, path=location)
			count += 1

	def get_secondary(self, min_threshold=4):
		"""
		From the saved html pages for the ideologies, extracts links embedded in the text
		:return:
		"""
		temp_dict = {}
		count = 0
		folder = self.config["HTML_FOLDER_PRIMARY"]
		for file in [f for f in os.listdir(folder) if f.endswith(".html")]:
			if count % 10 == 0:
				print(count)
			count += 1
			page = file.rsplit(".", 1)[0]
			path = self.config["HTML_FOLDER_PRIMARY"] + "/" + file
			raw = self.open_txt(path).rsplit("</h\d", 1)[0].split("<h\d", 1)[-1]
			to_replace = re.findall("<table.*?</table", raw, re.S)
			for trash in to_replace:
				raw = raw.replace(trash, "")
			to_replace = re.findall("<li>.+?</li>", raw, re.S)
			for trash in to_replace:
				raw = raw.replace(trash, "")
			to_replace = re.findall("&#91;.*?&#93;", raw, re.S)
			for trash in to_replace:
				raw = raw.replace(trash, "")
			#print(raw)
			links_raw = self.raw_links_from_html(raw)
			anchor_dict = self.anchors_from_links(raw, links_raw)
			temp_dict.update({page: anchor_dict})
		count_dict = {}
		for val in temp_dict.values():
			for key in val.keys():
				count_dict[key] = count_dict.get(key, 0) + 1
		self.save_json(count_dict, key="COUNT_DICT")
		good_links = {k1: {k2: v2 for k2,v2 in val.items() if
						   count_dict[k2]>=min_threshold} for
					  k1,val in temp_dict.items()}
		self.save_json(good_links, key="ANCHOR_FROM_PRIMARY")
		anchor_list = []
		for k1, v1 in good_links.items():
			for k2, v2 in v1.items():
				anchor_list.append(k1 + "\t" + k2 + "\t" + v2)
		anchor_string = "\n".join(anchor_list)
		self.save_txt(anchor_string, key="ANCHOR_FROM_PRIMARY_TXT")

	def raw_links_from_html(self, html_page):
		"""
		Takes an html page and finds all links embedded in the text.
		:param html_page: str
		:return links: list
		"""
		raw_links = re.findall(self.link_re, html_page)
		return [l for l in raw_links if not self.filter_link(l)]

	def anchors_from_links(self, html_page, raw_links):
		"""
		Takes a list of links found in the html and extracts anchor_text.
		:param html_page:
		:param link_list:
		:return: dict
		"""
		link_dict = {}
		for raw_link in raw_links:
			link = raw_link.split("title=\"")[-1].split("\">")[0].replace(" ", "_")
			splits = html_page.split(raw_link, 1)
			anchor = re.split("[.?!] |\n", splits[0])[-1] + "PAGELINK" + re.split("[.?!\n]", splits[1])[0]
			anchor = re.sub("<.*?>", "", anchor)
			anchor = re.sub("^.*?>|<.*?$", "", anchor)
			anchor = re.sub("\s*PAGELINK\s*", " PAGELINK ", anchor)
			if anchor != ' PAGELINK ':
				link_dict.update({link: anchor})
		return link_dict

	def make_secondary_graph(self, min_degree=4, alter_list=True):
		"""
		Makes the secondary graph, which includes the ideologies and all
			the (non-utility) pages they link to from their text,
			provided they have at least a specified number of links with
			the ideology nodes.
		:param min_degree: int
		:param alter_list: bool
		:return:
		"""
		pass #TODO: move from other file

	def clust_coeffs(self, graph, k=50):
		"""
		Prints the clustering coefficients for each
			the k nodes with the highest coefficients.
		:return:
		"""
		clust = nx.clustering(graph)
		top = sorted(clust.keys(), key=lambda x: clust[x], reverse=True)[:k]
		bottom = sorted(clust.keys(), key=lambda x: clust[x])[-k:]
		print("*********************\n{} highest:\n*********************".format(k))
		for node in top:
			print("{0:<20}{1:>20}".format(node, clust[node]))
		print("*********************\n{} lowest:\n*********************".format(k))
		for node in bottom:
			print("{0:<20}{1:>20}".format(node, clust[node]))

	def get_k_important_nodes(self, graph, k=50):
		"""
		Prints a list of the k nodes with the highest degree.
		:param graph: nx.DiGraph()
		:return k_top: list
		"""
		k_top = sorted(graph.nodes.keys(), key=lambda x: graph.degree[x])[k]
		return k_top

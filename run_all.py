"""
   Executes the methods of WikiNet() to create and analyze
    and ideological graph.

   Author: Isaac Riley
   Date:   September, 2020
"""


import os
import json
from wikinet import WikiNet

# set project directory
#PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.getcwd()

# read in project configurations
with open(PROJECT_ROOT + "/config.json") as f:
    config = json.load(f)
config.update({"PROJECT_ROOT": PROJECT_ROOT})
print(32 * "*" + " CONFIGURATIONS " + 32 * "*")
for k,v in config.items():
	print("  {0:<25}{1}".format(k+':', v))
print(80 * "*")

# initialize WikiNet object
wn = WikiNet(config)

# read in list of ideologies
wn.get_primary()

# populate the basic network
wn.make_primary_graph()

# summarize basic network
wn.summarize_graph(wn.primary_graph)

# get and save the page html
wn.get_html_primary()

# extract links, filtering out Wikipedia functional links
#   or links in tables, headers, footers
wn.get_secondary()

# create expanded network by adding secondary nodes
wn.make_secondary_graph(min_degree=4, alter_list=True)

# summarize expanded network
wn.summarize_graph(wn.secondary_graph)

# extract anchor text from primary articles to primary and secondary articles
wn.get_anchors(wn.primary) # saves json and csv

# get clustering coefficient for nodes in basic graph
wn.clust_coeffs(wn.primary_graph)

# get clustering coefficient for nodes in expanded graph
wn.clust_coeffs(wn.primary_graph)

# shared nearest neighbor clustering on basic graph
wn.snn(wn.primary_graph)

# shared nearest neighbor clustering on expanded graph
#wn.snn(secondary_graph)

# vertex betweenness clustering on basic graph
#wn.vbc(wn.primary_graph)
#wn.ebc_show(name="primary")

# vertex betweenness clustering on expanded graph
#wn.vbc(wn.secondary_graph)
#wn.vbc_show(name="secondary")

# edge betweenness clustering on basic graph
#wn.ebc(wn.primary_graph, name="primary")
#wn.ebc_show(name="primary")

# edge betweenness clustering on expanded graph
#wn.ebc(wn.secondary_graph, name="secondary")
#wn.ebc_show(name="secondary")

# select the k most important nodes from the expanded graph
wn.get_k_important_nodes()

# read in human evaluations of opinion from links
#wn.read_opinion_file()

# populate k most important lists with available links
#wn.make_ideology_matrices()

# impute_by_regression() #TODO
wn.impute_by_regression()

# impute by similarity #TODO (but lower priority)
wn.impute_by_similarity(k=5)
wn.impute_by_similarity(k=10)

# perform PCA on ideology matrices to identify key dimensions
wn.pca()

# display PCA, including which pages are most highly correlated with each factor
wn.pca_show()
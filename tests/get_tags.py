"""
	Author: Isaac Riley
	Date:   September 2020

	Contains code to run the entire process.
"""


from wikinet import WikiNet

wn = WikiNet("data/lists_seed/root_categories.txt")
wn.root_category = 'Category:Writers_from_Michigan'
wn.get_subcats_all()

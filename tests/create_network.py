"""
	Author: Isaac Riley
	Date:   September 2020

	Contains code to obtain full list of thinkers.
"""

import os
from wikinet import WikiNet

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# PROJECT_ROOT = os.getcwd()
#SEED_CATEGORIES_PATH = PROJECT_ROOT + '/data/lists_seed/root_categories.txt'

wn = WikiNet(PROJECT_ROOT)
wn.get_people()
wn.people2graph()
wn.create_full_network(100)

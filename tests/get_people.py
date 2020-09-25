"""
	Author: Isaac Riley
	Date:   September 2020

	Contains code to obtain full list of thinkers.
"""

#import sys
import os
from network.wikinet import WikiNet

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# define global variables
SEED_CATEGORIES_PATH = PROJECT_ROOT + '/data/lists_seed/root_categories.txt'


wn = WikiNet(SEED_CATEGORIES_PATH)
wn.get_people()
print(wn.people)
print(len(wn.people))

#wn.add_from_seeds_fw(SCRAPE_DEPTH) # add all links linked to seed pages
#wn.summarize()
#wn.add_from_seeds_bw(SCRAPE_DEPTH) # add all links that link to seed pages
#wn.summarize()


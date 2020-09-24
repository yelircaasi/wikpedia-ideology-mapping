"""
	Author: Isaac Riley
	Date:   September 21, 2020

	Contains code to run the entire process.
"""

import sys
from ../network/wikinet import WikiNet

# define global variables
TAG_SET_PATH, SEED_LIST_PATH, KEYWORD_PATH = sys.argv[1:3]
SCRAPE_DEPTH = 4


wn = WikiNet(TAG_SET_PATH, SEED_LIST_PATH, KEYWORD_PATH)

wn.add_from_seeds_fw(SCRAPE_DEPTH) # add all links linked to seed pages
wn.summarize()
wn.add_from_seeds_bw(SCRAPE_DEPTH) # add all links that link to seed pages
wn.summarize()


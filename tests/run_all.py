"""


"""


import os
from network.wikinet import WikiNet

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#SEED_CATEGORIES_PATH = PROJECT_ROOT + '/data/lists_seed/root_categories.txt'

wn = WikiNet(PROJECT_ROOT)
wn.get_people()


